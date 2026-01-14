"""
Preprocessor for handling cell style metadata in notebooks.
"""

from nbconvert.preprocessors import Preprocessor
from traitlets import Unicode


class StylePreprocessor(Preprocessor):
    """A preprocessor that extracts and processes style metadata from notebook cells.

    This preprocessor looks for style-related metadata in cells and prepares
    them for use in HTML export. It processes cell-level styles (general, input-
    specific, and output-specific), custom CSS classes, as well as notebook-level
    styles.

    Attributes:
        style_metadata_key (Unicode): The metadata key to look for cell styles.
            Defaults to "style". Can be configured via traitlets config system.

    Notes:
        The preprocessor collects styles and classes from multiple sources:
        - Cell-level 'style' metadata: Applied to the entire cell container
        - Cell-level 'input-style' metadata: Applied to the input area
        - Cell-level 'output-style' metadata: Applied to the output area
        - Cell-level 'class' metadata: Custom CSS classes added to the cell div
        - Cell-level 'input-class' metadata: Custom CSS classes added to the input area
        - Cell-level 'output-class' metadata: Custom CSS classes added to the output area
        - Notebook-level 'style' and 'stylesheet' metadata: Applied globally

    Examples:
        >>> from jupyter_export_html_style import StylePreprocessor
        >>> preprocessor = StylePreprocessor()
        >>> preprocessor.style_metadata_key = "custom_style"
        >>> nb, resources = preprocessor.preprocess(notebook, {})
    """

    style_metadata_key = Unicode("style", help="The metadata key to look for cell styles").tag(
        config=True
    )

    def preprocess(self, nb, resources):
        """Preprocess the entire notebook.

        Args:
            nb (NotebookNode): The notebook to preprocess.
            resources (dict): Additional resources used in the conversion process.

        Returns:
            (tuple): A tuple containing:
                - nb (NotebookNode): The processed notebook.
                - resources (dict): Updated resources with collected styles and
                    notebook-level style information.
        """
        # Initialize style collection in resources
        if "styles" not in resources:
            resources["styles"] = {}
        if "notebook_styles" not in resources:
            resources["notebook_styles"] = {}

        # Extract notebook-level style and stylesheet metadata
        if hasattr(nb, "metadata"):
            if "style" in nb.metadata:
                resources["notebook_styles"]["style"] = nb.metadata["style"]
            if "stylesheet" in nb.metadata:
                resources["notebook_styles"]["stylesheet"] = nb.metadata["stylesheet"]

        # Process each cell
        nb, resources = super().preprocess(nb, resources)

        return nb, resources

    def preprocess_cell(self, cell, resources, index):
        """Preprocess a single cell.

        Args:
            cell (NotebookNode): The cell to preprocess.
            resources (dict): Additional resources used in the conversion process.
            index (int): The index of the cell in the notebook.

        Returns:
            (tuple): A tuple containing:
                - cell (NotebookNode): The processed cell with style metadata
                    stored in cell_style, input_cell_style, and output_cell_style
                    attributes, and custom CSS classes in cell_class,
                    input_cell_class, and output_cell_class attributes.
                - resources (dict): Updated resources with collected cell styles
                    indexed by cell-{index}, cell-{index}-input, and
                    cell-{index}-output keys.
        """
        cell_id = f"cell-{index}"

        # Check if cell has style metadata
        if "metadata" in cell and self.style_metadata_key in cell.metadata:
            style = cell.metadata[self.style_metadata_key]

            # Store style in cell metadata for template access
            cell.metadata["cell_style"] = style

            # Also collect in resources for global style processing
            resources["styles"][cell_id] = style

        # Check for input-style metadata
        if "metadata" in cell and "input-style" in cell.metadata:
            input_style = cell.metadata["input-style"]
            cell.metadata["input_cell_style"] = input_style

            # Collect in resources for CSS generation
            input_id = f"{cell_id}-input"
            resources["styles"][input_id] = input_style

        # Check for output-style metadata
        if "metadata" in cell and "output-style" in cell.metadata:
            output_style = cell.metadata["output-style"]
            cell.metadata["output_cell_style"] = output_style

            # Collect in resources for CSS generation
            output_id = f"{cell_id}-output"
            resources["styles"][output_id] = output_style

        # Check for custom class metadata
        if "metadata" in cell and "class" in cell.metadata:
            custom_class = cell.metadata["class"]
            cell.metadata["cell_class"] = custom_class

        # Check for input-class metadata
        if "metadata" in cell and "input-class" in cell.metadata:
            input_class = cell.metadata["input-class"]
            cell.metadata["input_cell_class"] = input_class

        # Check for output-class metadata
        if "metadata" in cell and "output-class" in cell.metadata:
            output_class = cell.metadata["output-class"]
            cell.metadata["output_cell_class"] = output_class

        return cell, resources
