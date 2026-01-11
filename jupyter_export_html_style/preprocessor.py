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
        - URL with javascript: protocol
        - Import statements
        
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
        # Remove javascript: urls
        style = re.sub(r'javascript\s*:', '', style, flags=re.IGNORECASE)
        
        # Remove expression() (IE specific)
        style = re.sub(r'expression\s*\([^)]*\)', '', style, flags=re.IGNORECASE)
        
        # Remove behavior property (IE specific)
        style = re.sub(r'behavior\s*:', '', style, flags=re.IGNORECASE)
        
        # Remove -moz-binding (Firefox specific)
        style = re.sub(r'-moz-binding\s*:', '', style, flags=re.IGNORECASE)
        
        # Remove @import
        style = re.sub(r'@import', '', style, flags=re.IGNORECASE)
        
        # Remove any remaining HTML/script tags if they somehow got in
        style = re.sub(r'<[^>]*>', '', style)
        
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
