"""
Custom HTML Exporter with style metadata support.
"""

from nbconvert.exporters import HTMLExporter
from traitlets import default
from .preprocessor import StyleMetadataPreprocessor
import os


class HTMLStyleExporter(HTMLExporter):
    """
    HTML Exporter that:
    1. Embeds images by default
    2. Extracts style metadata from cells using StyleMetadataPreprocessor
    3. Uses a custom cell template to apply styles to cell divs
    """
    
    @default('embed_images')
    def _embed_images_default(self):
        """
        Default to embedding images in the HTML output.
        """
        return True
    
    def __init__(self, **kw):
        """
        Initialize the exporter with custom preprocessor and template.
        """
        super().__init__(**kw)
        
        # Add our custom preprocessor
        self.register_preprocessor(StyleMetadataPreprocessor, enabled=True)
    
    @default('template_name')
    def _template_name_default(self):
        """
        Use custom template that includes style support.
        """
        return 'html_style'
    
    @property
    def template_paths(self):
        """
        Return the paths to look for templates.
        """
        paths = super().template_paths
        # Add our custom template directory
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        paths.insert(0, template_dir)
        return paths
