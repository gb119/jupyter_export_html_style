"""
Jupyter Export HTML Style
==========================

A JupyterLab extension and nbconvert preprocessor/exporter that allows
cell style metadata overrides when exporting notebooks to HTML.

This package provides:
- A custom nbconvert preprocessor to handle style metadata
- A custom HTML exporter with style support
- A custom WebPDF exporter with style support
- Integration with JupyterLab for enhanced HTML export
"""

__version__ = "0.0.2rc3"

from .exporter import StyledHTMLExporter
from .preprocessor import StylePreprocessor
from .webpdf_exporter import StyledWebPDFExporter

__all__ = ["StylePreprocessor", "StyledHTMLExporter", "StyledWebPDFExporter", "__version__"]
