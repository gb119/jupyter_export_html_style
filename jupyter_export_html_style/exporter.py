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
    
    @default('template_name')
    def _template_name_default(self):
        """
        Use custom template that includes style support.
        """
        return 'html_style'
    
    def __init__(self, **kw):
        """
        Initialize the exporter with custom preprocessor and template.
        """
        # Set extra_template_basedirs before calling super().__init__
        if 'extra_template_basedirs' not in kw:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            kw['extra_template_basedirs'] = [template_dir]
        
        super().__init__(**kw)
        
        # Add our custom preprocessor
        self.register_preprocessor(StyleMetadataPreprocessor, enabled=True)
