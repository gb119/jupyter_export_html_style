"""
Preprocessor to extract style metadata from cells.
"""

from nbconvert.preprocessors import Preprocessor
import re


class StyleMetadataPreprocessor(Preprocessor):
    """
    Preprocessor that extracts 'style' from cell metadata and makes it 
    available for the template rendering.
    
    This preprocessor looks for a 'style' key in cell metadata, sanitizes it
    to prevent XSS attacks, and ensures it's accessible during template rendering.
    """
    
    def _sanitize_style(self, style):
        """
        Sanitize CSS style to prevent XSS attacks.
        
        Removes potentially dangerous patterns like:
        - JavaScript execution (expression, behavior, -moz-binding)
        - URL with javascript: protocol (with whitespace obfuscation handling)
        - Import statements
        - Data URLs that could contain scripts
        
        Parameters
        ----------
        style : str
            The CSS style string to sanitize
            
        Returns
        -------
        str
            The sanitized CSS style string
        """
        if not style or not isinstance(style, str):
            return ''
        
        # Remove potentially dangerous CSS patterns
        # Remove javascript: urls (including whitespace obfuscation)
        style = re.sub(r'j\s*a\s*v\s*a\s*s\s*c\s*r\s*i\s*p\s*t\s*:', '', style, flags=re.IGNORECASE)
        
        # Remove expression() (IE specific) - including whitespace variants
        style = re.sub(r'e\s*x\s*p\s*r\s*e\s*s\s*s\s*i\s*o\s*n\s*\([^)]*\)', '', style, flags=re.IGNORECASE)
        
        # Remove behavior property (IE specific)
        style = re.sub(r'b\s*e\s*h\s*a\s*v\s*i\s*o\s*r\s*:', '', style, flags=re.IGNORECASE)
        
        # Remove -moz-binding (Firefox specific)
        style = re.sub(r'-\s*m\s*o\s*z\s*-\s*b\s*i\s*n\s*d\s*i\s*n\s*g\s*:', '', style, flags=re.IGNORECASE)
        
        # Remove @import statements (including full statement)
        style = re.sub(r'@\s*i\s*m\s*p\s*o\s*r\s*t[^;]*;?', '', style, flags=re.IGNORECASE)
        
        # Remove data: URLs as they could contain SVG with scripts
        style = re.sub(r'data\s*:', '', style, flags=re.IGNORECASE)
        
        # Remove any HTML/script tags if they somehow got in
        style = re.sub(r'<[^>]*>', '', style)
        
        # Remove quotes to prevent attribute breaking
        style = style.replace('"', "'")
        
        return style.strip()
    
    def preprocess_cell(self, cell, resources, index):
        """
        Extract and sanitize style metadata from a cell.
        
        Parameters
        ----------
        cell : NotebookNode
            The cell to process
        resources : dict
            Additional resources used in the conversion process
        index : int
            The index of the cell being processed
            
        Returns
        -------
        cell : NotebookNode
            The processed cell
        resources : dict
            The resources dictionary
        """
        # Ensure metadata exists
        if 'metadata' not in cell:
            cell['metadata'] = {}
        
        # Extract and sanitize style from metadata if it exists
        if 'style' in cell.metadata:
            cell.metadata['style'] = self._sanitize_style(cell.metadata.get('style', ''))
        else:
            # Ensure style key exists even if empty
            cell.metadata['style'] = ''
        
        return cell, resources
