"""
Preprocessor to extract style metadata from cells.
"""

from nbconvert.preprocessors import Preprocessor


class StyleMetadataPreprocessor(Preprocessor):
    """
    Preprocessor that extracts 'style' from cell metadata and makes it 
    available for the template rendering.
    
    This preprocessor looks for a 'style' key in cell metadata and ensures
    it's accessible during template rendering.
    """
    
    def preprocess_cell(self, cell, resources, index):
        """
        Extract style metadata from a cell.
        
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
        # Extract style from metadata if it exists
        if 'metadata' in cell and 'style' in cell.metadata:
            # Store the style in the cell metadata for template access
            cell.metadata['style'] = cell.metadata.get('style', '')
        else:
            # Ensure style key exists even if empty
            if 'metadata' not in cell:
                cell['metadata'] = {}
            cell.metadata['style'] = ''
        
        return cell, resources
