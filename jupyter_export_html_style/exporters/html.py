"""
Custom HTML exporter with style support.
"""

import base64
import mimetypes
import os

import bs4
from nbconvert.exporters import HTMLExporter
from traitlets import Unicode

from ..preprocessor import StylePreprocessor


class StyledHTMLExporter(HTMLExporter):
    """An HTML exporter that supports cell-level style customization.

    This exporter extends the standard HTMLExporter to include custom styles
    defined in cell metadata. It automatically registers the StylePreprocessor
    to handle style metadata extraction and generates appropriate CSS to apply
    the styles during HTML export.

    By default, this exporter embeds images as base64 data URIs in the HTML
    output, making the HTML file self-contained. This behavior can be disabled
    by passing `embed_images=False` to the constructor.

    Attributes:
        export_from_notebook (str): Label for the export option.
        template_name (Unicode): Name of the template to use. Defaults to
            "styled". Can be configured via traitlets config system.

    Notes:
        The exporter supports multiple types of styles:
        - Cell-level styles via 'style' metadata
        - Input-specific styles via 'input-style' metadata
        - Output-specific styles via 'output-style' metadata
        - Notebook-level inline styles via 'style' metadata
        - Notebook-level external stylesheets via 'stylesheet' metadata

        Style metadata can be provided as either:
        - A dictionary of CSS property-value pairs
        - A string containing CSS declarations

        Images in markdown cells are embedded as base64 data URIs by default,
        making the exported HTML self-contained without requiring external
        image files. Image embedding is performed on the final HTML output
        rather than during markdown rendering, which ensures that explicit
        HTML elements (such as <div> tags) in markdown cells are preserved
        correctly without having their content stripped.

    Examples:
        >>> from jupyter_export_html_style import StyledHTMLExporter
        >>> exporter = StyledHTMLExporter()
        >>> output, resources = exporter.from_notebook_node(notebook)

        >>> # Disable image embedding if needed
        >>> exporter = StyledHTMLExporter(embed_images=False)
    """

    export_from_notebook = "HTML (with styles)"

    # Custom template file (can be overridden)
    template_name = Unicode("styled", help="Name of the template to use").tag(config=True)

    def __init__(self, **kw):
        """Initialize the exporter and register the style preprocessor.

        Args:
            **kw (dict): Additional keyword arguments passed to the parent
                HTMLExporter class.
        """
        # Add custom template directory to the search path before initialization
        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
        if "extra_template_basedirs" in kw:
            if template_path not in kw["extra_template_basedirs"]:
                kw["extra_template_basedirs"].insert(0, template_path)
        else:
            kw["extra_template_basedirs"] = [template_path]

        # Enable image embedding by default unless explicitly set
        # Note: We'll handle embedding ourselves to avoid the bug
        if "embed_images" not in kw:
            kw["embed_images"] = True

        super().__init__(**kw)

        # Register the style preprocessor
        self.register_preprocessor(StylePreprocessor, enabled=True)

    def from_notebook_node(self, nb, resources=None, **kw):
        """Convert a notebook node to HTML with style support.

        This method processes the notebook and applies custom styles, handling
        both cell-level and notebook-level styling. It also respects the
        notebook metadata 'anchors' field to control header anchor links.

        Args:
            nb (NotebookNode): The notebook to convert.
            resources (dict, optional): Additional resources used in the conversion
                process. If None, an empty dictionary is created. Defaults to None.
            **kw (dict): Additional keyword arguments passed to the parent
                from_notebook_node method.

        Returns:
            (tuple): A tuple containing:
                - output (str): The HTML output with injected style blocks.
                - resources (dict): Updated resources dictionary.

        Notes:
            The notebook metadata 'anchors' field controls whether anchor links
            (¶) are added to headers in markdown cells. If set to False, anchor
            links are excluded. By default (or if set to True), anchor links are
            included. This setting is temporary and does not affect subsequent
            exports with the same exporter instance.
        """
        # Save original exclude_anchor_links setting
        original_exclude_anchor_links = self.exclude_anchor_links

        # Check notebook metadata for anchor links preference
        # If metadata.anchors is False, exclude anchor links
        # Default is to include anchor links (backward compatible)
        if "anchors" in nb.metadata:
            self.exclude_anchor_links = not nb.metadata["anchors"]

        # Save the user's embed_images preference
        should_embed = self.embed_images

        # Temporarily disable parent's embed_images to avoid the bug where
        # BeautifulSoup auto-closes incomplete HTML fragments during markdown rendering
        self.embed_images = False

        try:
            # Process the notebook with our preprocessor
            output, resources = super().from_notebook_node(nb, resources, **kw)
        finally:
            # Restore embed_images setting
            self.embed_images = should_embed
            # Restore original exclude_anchor_links setting
            self.exclude_anchor_links = original_exclude_anchor_links

        # Collect attachments from notebook cells for image embedding
        attachments = {}
        for cell in nb.cells:
            if hasattr(cell, "attachments") and cell.attachments:
                attachments.update(cell.attachments)

        # Embed images in the final HTML if image embedding is enabled
        # This processes the complete HTML document after all rendering is done,
        # which avoids issues with BeautifulSoup auto-closing incomplete HTML fragments
        if should_embed:
            output = self._embed_images_in_html(output, attachments, resources)

        # Prepare all custom style blocks to inject before </head>
        style_blocks = []

        # Add custom cell styling section if styles were collected
        if resources and "styles" in resources and resources["styles"]:
            style_block = self._generate_style_block(resources["styles"])
            if style_block:
                style_blocks.append(style_block)

        # Add notebook-level styles and stylesheets
        if resources and "notebook_styles" in resources:
            notebook_style_block = self._generate_notebook_style_block(
                resources["notebook_styles"], resources
            )
            if notebook_style_block:
                style_blocks.append(notebook_style_block)

        # Insert all style blocks into HTML (before </head>)
        if style_blocks and "</head>" in output:
            combined_styles = "".join(style_blocks)
            output = output.replace("</head>", f"{combined_styles}</head>")

        return output, resources

    def _generate_style_block(self, styles):
        """Generate a CSS style block from collected styles.

        Args:
            styles (dict): Dictionary mapping cell IDs to style definitions.
                Style definitions can be either dictionaries of CSS properties
                or strings containing CSS declarations.

        Returns:
            (str): CSS style block wrapped in HTML <style> tags. Returns empty
                string if no styles are provided.

        Examples:
            >>> exporter = StyledHTMLExporter()
            >>> styles = {"cell-0": {"color": "red"}, "cell-1": "padding: 10px"}
            >>> style_block = exporter._generate_style_block(styles)
        """
        css_rules = []
        for cell_id, style in styles.items():
            if isinstance(style, dict):
                # Convert style dict to CSS
                style_str = "; ".join(f"{k}: {v}" for k, v in style.items())
                css_rules.append(f"#{cell_id} {{ {style_str} }}")
            elif isinstance(style, str):
                # Direct CSS string
                css_rules.append(f"#{cell_id} {{ {style} }}")

        if css_rules:
            return "\n<style>\n/* Custom cell styles */\n" + "\n".join(css_rules) + "\n</style>\n"
        return ""

    def _generate_notebook_style_block(self, notebook_styles, resources=None):
        """Generate style and stylesheet blocks from notebook-level metadata.

        Local or relative stylesheet paths are embedded as inline <style> tags,
        while remote URLs (http/https) remain as <link> tags.

        Args:
            notebook_styles (dict): Dictionary containing 'style' and/or
                'stylesheet' keys. The 'style' key should contain inline CSS
                as a string. The 'stylesheet' key can be either a string URL
                or a list of string URLs to external or local stylesheets.
            resources (dict, optional): Resources dictionary containing metadata
                such as the base path for resolving relative file paths.
                Defaults to None.

        Returns:
            (str): HTML containing <style> and/or <link> elements. Returns empty
                string if no notebook styles are provided.

        Notes:
            Local stylesheet files (not starting with http:// or https://) are
            read and embedded as inline styles. Remote stylesheets remain as
            link tags. If a local file cannot be read, it falls back to a
            link tag.

        Examples:
            >>> exporter = StyledHTMLExporter()
            >>> notebook_styles = {
            ...     "style": "body { font-family: Arial; }",
            ...     "stylesheet": "https://example.com/style.css"
            ... }
            >>> html = exporter._generate_notebook_style_block(notebook_styles)
        """
        blocks = []

        # Get the base path from resources if available
        base_path = "."
        if resources:
            base_path = resources.get("metadata", {}).get("path", ".")

        # Add custom stylesheet link if provided
        if "stylesheet" in notebook_styles:
            stylesheet = notebook_styles["stylesheet"]
            stylesheets = [stylesheet] if isinstance(stylesheet, str) else stylesheet

            for ss in stylesheets:
                # Check if this is a local/relative file or a remote URL
                if ss.startswith(("http://", "https://")):
                    # Remote URL - keep as link tag
                    blocks.append(f'\n<link rel="stylesheet" href="{ss}">\n')
                else:
                    # Local/relative path - try to embed
                    try:
                        # Resolve the full path and validate it stays within base_path
                        file_path = os.path.abspath(os.path.join(base_path, ss))
                        base_path_abs = os.path.abspath(base_path)

                        # Security check: ensure the resolved path is within base_path
                        # Use os.path.commonpath for robust cross-platform validation
                        try:
                            common = os.path.commonpath([base_path_abs, file_path])
                            if common != base_path_abs:
                                # Path traversal attempt detected, fallback to link tag
                                blocks.append(f'\n<link rel="stylesheet" href="{ss}">\n')
                                continue
                        except ValueError:
                            # Different drives on Windows, definitely outside base path
                            blocks.append(f'\n<link rel="stylesheet" href="{ss}">\n')
                            continue

                        if os.path.isfile(file_path):
                            with open(file_path, encoding="utf-8") as f:
                                css_content = f.read()
                                blocks.append(
                                    f"\n<style>\n/* Embedded stylesheet: {ss} */\n{css_content}\n</style>\n"
                                )
                        else:
                            # File doesn't exist, fallback to link tag
                            blocks.append(f'\n<link rel="stylesheet" href="{ss}">\n')
                    except (OSError, UnicodeDecodeError, PermissionError):
                        # If embedding fails due to file access issues, fallback to link tag
                        blocks.append(f'\n<link rel="stylesheet" href="{ss}">\n')

        # Add custom inline styles if provided
        if "style" in notebook_styles:
            style = notebook_styles["style"]
            if isinstance(style, str) and style.strip():
                blocks.append(f"\n<style>\n/* Custom notebook styles */\n{style}\n</style>\n")

        return "".join(blocks)

    def _embed_images_in_html(self, html, attachments, resources):
        """Embed images in the final HTML output.

        This method processes the complete HTML document after all rendering is done,
        replacing image src attributes with base64 data URIs. This approach avoids
        the issue where BeautifulSoup auto-closes incomplete HTML fragments when
        processing individual block_html tokens during markdown rendering.

        Args:
            html (str): Complete HTML document.
            attachments (dict): Dictionary of attachments from notebook cells.
            resources (dict): Resources dictionary from the conversion process.

        Returns:
            (str): HTML with embedded images.

        Notes:
            This method handles:
            - File path references (e.g., src="image.png")
            - Attachment references (e.g., src="attachment:image.png")
            - Already embedded data URIs (skipped)
            - HTTP/HTTPS URLs (skipped for security and performance)
        """
        try:
            soup = bs4.BeautifulSoup(html, features="html.parser")
            imgs = soup.find_all("img")

            # Get the base path from resources if available
            base_path = resources.get("metadata", {}).get("path", ".")

            for img in imgs:
                src = img.attrs.get("src")
                if src is None or not src:
                    continue

                # Skip already embedded data URIs
                if src.startswith("data:"):
                    continue

                # Skip HTTP/HTTPS URLs
                if src.startswith(("http://", "https://")):
                    continue

                try:
                    # Handle attachment: URLs
                    if src.startswith("attachment:"):
                        img_name = src[len("attachment:") :]
                        if img_name in attachments:
                            # Attachments can have multiple mime types, pick the first available
                            attachment_data = attachments[img_name]
                            for mime_type, data in attachment_data.items():
                                # Data is already base64 encoded in attachments
                                img.attrs["src"] = f"data:{mime_type};base64,{data}"
                                break
                    # Handle file path references
                    else:
                        file_path = os.path.join(base_path, src)
                        if os.path.isfile(file_path):
                            with open(file_path, "rb") as f:
                                file_data = f.read()
                                # Guess MIME type from file extension
                                mime_type, _ = mimetypes.guess_type(file_path)
                                if mime_type is None:
                                    # Default to png if we can't determine type
                                    mime_type = "image/png"
                                b64_data = base64.b64encode(file_data).decode("utf-8")
                                img.attrs["src"] = f"data:{mime_type};base64,{b64_data}"
                except Exception:
                    # If embedding fails for any reason, leave the src unchanged
                    # This ensures that individual image failures don't break the entire export
                    pass

            return str(soup)
        except Exception:
            # If HTML parsing fails, return the original HTML unchanged
            return html
