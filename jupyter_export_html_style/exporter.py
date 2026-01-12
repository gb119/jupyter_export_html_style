"""
Custom HTML exporter with style support.
"""

from nbconvert.exporters import HTMLExporter
from traitlets import Unicode

from .preprocessor import StylePreprocessor


class StyledHTMLExporter(HTMLExporter):
    """
    An HTML exporter that supports cell-level style customization.

    This exporter extends the standard HTMLExporter to include
    custom styles defined in cell metadata.
    """

    export_from_notebook = "Styled HTML Export"

    # Custom template file (can be overridden)
    template_name = Unicode("classic", help="Name of the template to use").tag(config=True)

    def __init__(self, **kw):
        """Initialize the exporter."""
        super().__init__(**kw)

        # Register the style preprocessor
        self.register_preprocessor(StylePreprocessor, enabled=True)

    def from_notebook_node(self, nb, resources=None, **kw):
        """Convert a notebook node to HTML with style support.

        Args:
            nb (NotebookNode):
                The notebook to convert
            resources (dict, optional):
                Additional resources used in the conversion process
            **kw (dict):
                Additional keyword arguments

        Returns:
            output (str):
                The HTML output
            resources (dict):
                Updated resources
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
            notebook_style_block = self._generate_notebook_style_block(
                resources["notebook_styles"]
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
            styles (dict):
                Dictionary mapping cell IDs to style definitions

        Returns:
            str:
                CSS style block
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
            notebook_styles (dict):
                Dictionary containing 'style' and/or 'stylesheet' keys

        Returns:
            str:
                HTML containing style and/or link elements
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
