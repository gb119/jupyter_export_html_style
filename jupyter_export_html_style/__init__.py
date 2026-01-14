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

__version__ = "0.1.1"

from .exporters import StyledHTMLExporter, StyledSlidesExporter, StyledWebPDFExporter
from .preprocessor import StylePreprocessor

__all__ = [
    "StylePreprocessor",
    "StyledHTMLExporter",
    "StyledSlidesExporter",
    "StyledWebPDFExporter",
    "__version__",
]
