"""
Preprocessor for handling cell style metadata in notebooks.
"""

from nbconvert.preprocessors import Preprocessor
from traitlets import Unicode


class StylePreprocessor(Preprocessor):
    """
    A preprocessor that extracts and processes style metadata from notebook cells.

    This preprocessor looks for style-related metadata in cells and prepares
    them for use in HTML export.
    """

    style_metadata_key = Unicode("style", help="The metadata key to look for cell styles").tag(
        config=True
    )

    def preprocess(self, nb, resources):
        """
        Preprocess the entire notebook.

        Parameters
        ----------
        nb : NotebookNode
            The notebook to preprocess
        resources : dict
            Additional resources used in the conversion process

        Returns
        -------
        nb : NotebookNode
            The processed notebook
        resources : dict
            Updated resources
        """
        # Initialize style collection in resources
        if "styles" not in resources:
            resources["styles"] = {}

        # Process each cell
        nb, resources = super().preprocess(nb, resources)

        return nb, resources

    def preprocess_cell(self, cell, resources, index):
        """
        Preprocess a single cell.

        Parameters
        ----------
        cell : NotebookNode
            The cell to preprocess
        resources : dict
            Additional resources used in the conversion process
        index : int
            The index of the cell in the notebook

        Returns
        -------
        cell : NotebookNode
            The processed cell
        resources : dict
            Updated resources
        """
        # Check if cell has style metadata
        if "metadata" in cell and self.style_metadata_key in cell.metadata:
            style = cell.metadata[self.style_metadata_key]

            # Store style in cell metadata for template access
            cell.metadata["cell_style"] = style

            # Also collect in resources for global style processing
            cell_id = f"cell-{index}"
            resources["styles"][cell_id] = style

        return cell, resources
