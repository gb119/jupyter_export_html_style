"""Reveal.js slides exporter with style support."""

from traitlets import Bool, Unicode, default

from .html import StyledHTMLExporter


class StyledSlidesExporter(StyledHTMLExporter):
    """Exports HTML slides with reveal.js and custom cell styles.

    This exporter extends the StyledHTMLExporter to create reveal.js slide
    presentations with custom cell-level styles. It combines the functionality
    of nbconvert's SlidesExporter with the style customization features of
    StyledHTMLExporter.

    The exporter supports all the style features from StyledHTMLExporter:
    - Cell-level styles via 'style' metadata
    - Input-specific styles via 'input-style' metadata
    - Output-specific styles via 'output-style' metadata
    - Notebook-level inline styles via 'style' metadata
    - Notebook-level external stylesheets via 'stylesheet' metadata

    It also includes reveal.js configuration options for customizing the
    slide presentation appearance and behavior.

    Attributes:
        export_from_notebook (str): Label for the export option.
        template_name (Unicode): Name of the template to use. Defaults to
            "styled_reveal". Can be configured via traitlets config system.
        reveal_url_prefix (Unicode): URL prefix for reveal.js library.
        reveal_theme (Unicode): Name of the reveal.js theme to use.
        reveal_transition (Unicode): Name of the reveal.js transition effect.
        reveal_scroll (Bool): Enable scrolling within each slide.
        reveal_number (Unicode): Slide number format (e.g. 'c/t').
        reveal_width (Unicode): Presentation width for aspect ratio.
        reveal_height (Unicode): Presentation height for aspect ratio.
        font_awesome_url (Unicode): URL to load Font Awesome from.

    Examples:
        >>> from jupyter_export_html_style import StyledSlidesExporter
        >>> exporter = StyledSlidesExporter()
        >>> output, resources = exporter.from_notebook_node(notebook)

        >>> # Customize reveal.js theme
        >>> exporter = StyledSlidesExporter(reveal_theme="moon")
    """

    export_from_notebook = "Reveal.js slides (with styles)"

    # Override template name to use styled_reveal
    template_name = Unicode("styled_reveal", help="Name of the template to use").tag(config=True)

    @default("file_extension")
    def _file_extension_default(self):
        """Set default file extension for slides.

        Returns:
            (str): Default file extension ".slides.html".
        """
        return ".slides.html"

    @default("template_extension")
    def _template_extension_default(self):
        """Set default template extension.

        Returns:
            (str): Default template extension ".html.j2".
        """
        return ".html.j2"

    # Reveal.js configuration options
    # These match the options from nbconvert's SlidesExporter
    reveal_url_prefix = Unicode(
        help="""The URL prefix for reveal.js.
        This defaults to the reveal CDN, but can be any url pointing to a copy
        of reveal.js.

        For speaker notes to work, this must be a relative path to a local
        copy of reveal.js: e.g., "reveal.js".

        If a relative path is given, it must be a subdirectory of the
        current directory (from which the server is run).

        See the usage documentation
        (https://nbconvert.readthedocs.io/en/latest/usage.html#reveal-js-html-slideshow)
        for more details.
        """
    ).tag(config=True)

    @default("reveal_url_prefix")
    def _reveal_url_prefix_default(self):
        """Set default reveal.js URL prefix.

        Returns:
            (str): Default reveal.js CDN URL.
        """
        return "https://unpkg.com/reveal.js@4.0.2"

    reveal_theme = Unicode(
        "simple",
        help="""
        Name of the reveal.js theme to use.

        We look for a file with this name under
        ``reveal_url_prefix``/css/theme/``reveal_theme``.css.

        https://github.com/hakimel/reveal.js/tree/master/css/theme has
        list of themes that ship by default with reveal.js.
        """,
    ).tag(config=True)

    reveal_transition = Unicode(
        "slide",
        help="""
        Name of the reveal.js transition to use.

        The list of transitions that ships by default with reveal.js are:
        none, fade, slide, convex, concave and zoom.
        """,
    ).tag(config=True)

    reveal_scroll = Bool(
        False,
        help="""
        If True, enable scrolling within each slide
        """,
    ).tag(config=True)

    reveal_number = Unicode(
        "",
        help="""
        slide number format (e.g. 'c/t'). Choose from:
        'c': current, 't': total, 'h': horizontal, 'v': vertical
        """,
    ).tag(config=True)

    reveal_width = Unicode(
        "",
        help="""
        width used to determine the aspect ratio of your presentation.
        Use the horizontal pixels available on your intended presentation
        equipment.
        """,
    ).tag(config=True)

    reveal_height = Unicode(
        "",
        help="""
        height used to determine the aspect ratio of your presentation.
        Use the horizontal pixels available on your intended presentation
        equipment.
        """,
    ).tag(config=True)

    font_awesome_url = Unicode(
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css",
        help="""
        URL to load font awesome from.

        Defaults to loading from cdnjs.
        """,
    ).tag(config=True)

    def _init_resources(self, resources):
        """Initialize resources with reveal.js configuration.

        This method adds reveal.js configuration to the resources dictionary
        so it can be used by the templates.

        Args:
            resources (dict): Resources dictionary.

        Returns:
            (dict): Updated resources dictionary with reveal.js configuration.
        """
        resources = super()._init_resources(resources)
        if "reveal" not in resources:
            resources["reveal"] = {}
        resources["reveal"]["url_prefix"] = self.reveal_url_prefix
        resources["reveal"]["theme"] = self.reveal_theme
        resources["reveal"]["transition"] = self.reveal_transition
        resources["reveal"]["scroll"] = self.reveal_scroll
        resources["reveal"]["number"] = self.reveal_number
        resources["reveal"]["height"] = self.reveal_height
        resources["reveal"]["width"] = self.reveal_width
        resources["reveal"]["font_awesome_url"] = self.font_awesome_url
        return resources

    def from_notebook_node(self, nb, resources=None, **kw):
        """Convert a notebook node to reveal.js slides with style support.

        This method overrides the parent's from_notebook_node to prevent
        duplicate style injection. The styled_reveal template handles style
        injection in the html_head_css block, so we don't need the post-
        processing style injection from StyledHTMLExporter.

        Args:
            nb (NotebookNode): The notebook to convert.
            resources (dict, optional): Additional resources used in the conversion
                process. If None, an empty dictionary is created. Defaults to None.
            **kw (dict): Additional keyword arguments passed to the parent
                from_notebook_node method.

        Returns:
            (tuple): A tuple containing:
                - output (str): The HTML slides output with styles.
                - resources (dict): Updated resources dictionary.
        """
        # Save the user's embed_images preference
        should_embed = self.embed_images

        # Temporarily disable parent's embed_images to avoid the bug where
        # BeautifulSoup auto-closes incomplete HTML fragments during markdown rendering
        self.embed_images = False

        try:
            # Process the notebook with our preprocessor
            # Use HTMLExporter's from_notebook_node to skip StyledHTMLExporter's
            # post-processing since the template handles it
            from nbconvert.exporters import HTMLExporter

            output, resources = HTMLExporter.from_notebook_node(self, nb, resources, **kw)
        finally:
            # Restore embed_images setting
            self.embed_images = should_embed

        # Collect attachments from notebook cells for image embedding
        attachments = {}
        for cell in nb.cells:
            if hasattr(cell, "attachments") and cell.attachments:
                attachments.update(cell.attachments)

        # Embed images in the final HTML if image embedding is enabled
        if should_embed:
            output = self._embed_images_in_html(output, attachments, resources)

        # Add notebook-level styles (the template doesn't handle these)
        if resources and "notebook_styles" in resources:
            notebook_style_block = self._generate_notebook_style_block(
                resources["notebook_styles"], resources
            )
            if notebook_style_block and "</head>" in output:
                output = output.replace("</head>", f"{notebook_style_block}</head>")

        return output, resources
