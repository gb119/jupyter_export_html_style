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
        """
        Convert a notebook node to HTML with style support.

        Parameters
        ----------
        nb : NotebookNode
            The notebook to convert
        resources : dict, optional
            Additional resources used in the conversion process
        **kw : dict
            Additional keyword arguments

        Returns
        -------
        output : str
            The HTML output
        resources : dict
            Updated resources
        """
        # Process the notebook with our preprocessor
        output, resources = super().from_notebook_node(nb, resources, **kw)

        # Add custom styling section if styles were collected
        if resources and "styles" in resources and resources["styles"]:
            style_block = self._generate_style_block(resources["styles"])
            # Insert style block into HTML (before </head>)
            if "</head>" in output:
                output = output.replace("</head>", f"{style_block}</head>")

        return output, resources

    def _generate_style_block(self, styles):
        """
        Generate a CSS style block from collected styles.

        Parameters
        ----------
        styles : dict
            Dictionary mapping cell IDs to style definitions

        Returns
        -------
        str
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
