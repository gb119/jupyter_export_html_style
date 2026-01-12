"""
Custom HTML exporter with style support.
"""

import os
import threading

import bs4
from nbconvert.exporters import HTMLExporter
from nbconvert.filters import markdown_mistune
from traitlets import Unicode

from .preprocessor import StylePreprocessor

# Module-level lock for thread-safe patching
_patch_lock = threading.Lock()
_is_patched = False


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
        image files.

    Examples:
        >>> from jupyter_export_html_style import StyledHTMLExporter
        >>> exporter = StyledHTMLExporter()
        >>> output, resources = exporter.from_notebook_node(notebook)

        >>> # Disable image embedding if needed
        >>> exporter = StyledHTMLExporter(embed_images=False)
    """

    export_from_notebook = "Styled HTML Export"

    # Custom template file (can be overridden)
    template_name = Unicode("styled", help="Name of the template to use").tag(config=True)

    def __init__(self, **kw):
        """Initialize the exporter and register the style preprocessor.

        Args:
            **kw (dict): Additional keyword arguments passed to the parent
                HTMLExporter class.
        """
        # Enable image embedding by default unless explicitly set
        # Note: **kw creates a new dict, so this doesn't modify caller's data
        if "embed_images" not in kw:
            kw["embed_images"] = True

        # Add custom template directory to the search path before initialization
        template_path = os.path.join(os.path.dirname(__file__), "templates")
        if "extra_template_basedirs" in kw:
            if template_path not in kw["extra_template_basedirs"]:
                kw["extra_template_basedirs"].insert(0, template_path)
        else:
            kw["extra_template_basedirs"] = [template_path]

        super().__init__(**kw)

        # Register the style preprocessor
        self.register_preprocessor(StylePreprocessor, enabled=True)

        # Patch nbconvert's markdown filter to handle attachment: URLs in img tags
        # This fixes a bug where <img src="attachment:..."> tags are not embedded
        # even when embed_images=True
        self._patch_markdown_filter()

    def from_notebook_node(self, nb, resources=None, **kw):
        """Convert a notebook node to HTML with style support.

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
        """
        # Process the notebook with our preprocessor
        output, resources = super().from_notebook_node(nb, resources, **kw)

        # Prepare all custom style blocks to inject before </head>
        style_blocks = []

        # Add custom cell styling section if styles were collected
        if resources and "styles" in resources and resources["styles"]:
            style_block = self._generate_style_block(resources["styles"])
            if style_block:
                style_blocks.append(style_block)

        # Add notebook-level styles and stylesheets
        if resources and "notebook_styles" in resources:
            notebook_style_block = self._generate_notebook_style_block(resources["notebook_styles"])
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

    def _generate_notebook_style_block(self, notebook_styles):
        """Generate style and stylesheet blocks from notebook-level metadata.

        Args:
            notebook_styles (dict): Dictionary containing 'style' and/or
                'stylesheet' keys. The 'style' key should contain inline CSS
                as a string. The 'stylesheet' key can be either a string URL
                or a list of string URLs to external stylesheets.

        Returns:
            (str): HTML containing <style> and/or <link> elements. Returns empty
                string if no notebook styles are provided.

        Examples:
            >>> exporter = StyledHTMLExporter()
            >>> notebook_styles = {
            ...     "style": "body { font-family: Arial; }",
            ...     "stylesheet": "https://example.com/style.css"
            ... }
            >>> html = exporter._generate_notebook_style_block(notebook_styles)
        """
        blocks = []

        # Add custom stylesheet link if provided
        if "stylesheet" in notebook_styles:
            stylesheet = notebook_styles["stylesheet"]
            if isinstance(stylesheet, str):
                blocks.append(f'\n<link rel="stylesheet" href="{stylesheet}">\n')
            elif isinstance(stylesheet, list):
                # Support multiple stylesheets
                for ss in stylesheet:
                    blocks.append(f'\n<link rel="stylesheet" href="{ss}">\n')

        # Add custom inline styles if provided
        if "style" in notebook_styles:
            style = notebook_styles["style"]
            if isinstance(style, str) and style.strip():
                blocks.append(f"\n<style>\n/* Custom notebook styles */\n{style}\n</style>\n")

        return "".join(blocks)

    def _patch_markdown_filter(self):
        """Patch nbconvert's markdown filter to handle attachment: URLs in img tags.

        This method patches the IPythonRenderer._html_embed_images method to properly
        handle attachment: URLs in HTML img tags when embed_images is enabled.

        Notes:
            This is a workaround for a bug in nbconvert where <img src="attachment:...">
            tags are not embedded even when embed_images=True. The standard nbconvert
            _html_embed_images method only calls _src_to_base64() which handles file
            paths, but doesn't handle attachment: URLs. This patch makes it use
            _embed_image_or_attachment() instead, which handles both cases.

            The patch is applied globally to nbconvert's IPythonRenderer class and is
            thread-safe using a module-level lock. Once applied, it affects all
            subsequent uses of nbconvert's markdown renderer.
        """
        global _is_patched

        # Use a lock to ensure thread-safe patching
        with _patch_lock:
            if _is_patched:
                return

            def patched_html_embed_images(self, html: str) -> str:
                """Patched version that handles attachment: URLs in img tags.

                Args:
                    html (str): HTML string containing img tags.

                Returns:
                    (str): HTML string with img src attributes converted to data URIs
                        for both attachment: URLs and file paths.
                """
                parsed_html = bs4.BeautifulSoup(html, features="html.parser")
                imgs = parsed_html.find_all("img")

                # Replace img tags's sources by base64 dataurls
                for img in imgs:
                    src = img.attrs.get("src")
                    if src is None:
                        continue

                    # Use _embed_image_or_attachment which handles both attachments and file paths
                    embedded_src = self._embed_image_or_attachment(img.attrs["src"])
                    if embedded_src != img.attrs["src"]:  # If it was converted
                        img.attrs["src"] = embedded_src

                return str(parsed_html)

            # Apply the patch
            markdown_mistune.IPythonRenderer._html_embed_images = patched_html_embed_images
            _is_patched = True
