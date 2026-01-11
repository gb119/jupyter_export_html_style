"""
Tests for the StylePreprocessor class.
"""

from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

from jupyter_export_html_style import StylePreprocessor


def test_style_preprocessor_initialization():
    """Test that StylePreprocessor can be initialized."""
    preprocessor = StylePreprocessor()
    assert preprocessor.style_metadata_key == "style"


def test_style_preprocessor_custom_key():
    """Test StylePreprocessor with custom metadata key."""
    preprocessor = StylePreprocessor()
    preprocessor.style_metadata_key = "custom_style"
    assert preprocessor.style_metadata_key == "custom_style"


def test_preprocess_notebook_without_styles():
    """Test preprocessing a notebook without style metadata."""
    preprocessor = StylePreprocessor()
    nb = new_notebook(cells=[new_code_cell("print('hello')"), new_markdown_cell("# Title")])

    processed_nb, resources = preprocessor.preprocess(nb, {})

    assert processed_nb is not None
    assert "styles" in resources
    assert len(resources["styles"]) == 0


def test_preprocess_notebook_with_styles():
    """Test preprocessing a notebook with style metadata."""
    preprocessor = StylePreprocessor()

    # Create a cell with style metadata
    cell = new_code_cell("print('styled')")
    cell.metadata["style"] = {"background-color": "#f0f0f0"}

    nb = new_notebook(cells=[cell])

    processed_nb, resources = preprocessor.preprocess(nb, {})

    assert "styles" in resources
    assert len(resources["styles"]) == 1
    assert "cell-0" in resources["styles"]
    assert resources["styles"]["cell-0"] == {"background-color": "#f0f0f0"}


def test_preprocess_cell_with_dict_style():
    """Test preprocessing a cell with dictionary style metadata."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("x = 1")
    cell.metadata["style"] = {"background-color": "#fff", "border": "1px solid #000"}

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 0)

    assert "cell_style" in processed_cell.metadata
    assert processed_cell.metadata["cell_style"]["background-color"] == "#fff"


def test_preprocess_cell_with_string_style():
    """Test preprocessing a cell with string style metadata."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("y = 2")
    cell.metadata["style"] = "background-color: #eee; padding: 10px;"

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 1)

    assert "cell_style" in processed_cell.metadata
    assert processed_cell.metadata["cell_style"] == "background-color: #eee; padding: 10px;"


def test_preprocess_multiple_cells_with_styles():
    """Test preprocessing multiple cells with different styles."""
    preprocessor = StylePreprocessor()

    cells = [
        new_code_cell("a = 1"),
        new_code_cell("b = 2"),
        new_code_cell("c = 3"),
    ]

    cells[0].metadata["style"] = {"color": "red"}
    cells[2].metadata["style"] = {"color": "blue"}

    nb = new_notebook(cells=cells)
    processed_nb, resources = preprocessor.preprocess(nb, {})

    assert len(resources["styles"]) == 2
    assert "cell-0" in resources["styles"]
    assert "cell-2" in resources["styles"]
    assert "cell-1" not in resources["styles"]
