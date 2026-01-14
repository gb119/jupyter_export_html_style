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


def test_preprocess_cell_with_input_style():
    """Test preprocessing a cell with input-style metadata."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("x = 1")
    cell.metadata["input-style"] = {"background-color": "#f5f5f5", "padding": "5px"}

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 0)

    assert "input_cell_style" in processed_cell.metadata
    assert processed_cell.metadata["input_cell_style"]["background-color"] == "#f5f5f5"
    assert "cell-0-input" in resources["styles"]


def test_preprocess_cell_with_output_style():
    """Test preprocessing a cell with output-style metadata."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("print('test')")
    cell.metadata["output-style"] = {"border": "1px solid #ccc"}

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 0)

    assert "output_cell_style" in processed_cell.metadata
    assert processed_cell.metadata["output_cell_style"]["border"] == "1px solid #ccc"
    assert "cell-0-output" in resources["styles"]


def test_preprocess_cell_with_all_styles():
    """Test preprocessing a cell with cell, input, and output styles."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("x = 42")
    cell.metadata["style"] = {"margin": "10px"}
    cell.metadata["input-style"] = {"background-color": "#e0e0e0"}
    cell.metadata["output-style"] = {"color": "#333"}

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 1)

    assert "cell_style" in processed_cell.metadata
    assert "input_cell_style" in processed_cell.metadata
    assert "output_cell_style" in processed_cell.metadata
    assert "cell-1" in resources["styles"]
    assert "cell-1-input" in resources["styles"]
    assert "cell-1-output" in resources["styles"]


def test_preprocess_notebook_with_notebook_level_style():
    """Test preprocessing a notebook with notebook-level style metadata."""
    preprocessor = StylePreprocessor()

    nb = new_notebook(cells=[new_code_cell("print('hello')")])
    nb.metadata["style"] = "body { font-family: Arial; }"

    processed_nb, resources = preprocessor.preprocess(nb, {})

    assert "notebook_styles" in resources
    assert "style" in resources["notebook_styles"]
    assert resources["notebook_styles"]["style"] == "body { font-family: Arial; }"


def test_preprocess_notebook_with_stylesheet():
    """Test preprocessing a notebook with stylesheet metadata."""
    preprocessor = StylePreprocessor()

    nb = new_notebook(cells=[new_code_cell("x = 1")])
    nb.metadata["stylesheet"] = "https://example.com/custom.css"

    processed_nb, resources = preprocessor.preprocess(nb, {})

    assert "notebook_styles" in resources
    assert "stylesheet" in resources["notebook_styles"]
    assert resources["notebook_styles"]["stylesheet"] == "https://example.com/custom.css"


def test_preprocess_notebook_with_multiple_stylesheets():
    """Test preprocessing a notebook with multiple stylesheets."""
    preprocessor = StylePreprocessor()

    nb = new_notebook(cells=[new_code_cell("y = 2")])
    nb.metadata["stylesheet"] = [
        "https://example.com/style1.css",
        "https://example.com/style2.css",
    ]

    processed_nb, resources = preprocessor.preprocess(nb, {})

    assert "notebook_styles" in resources
    assert "stylesheet" in resources["notebook_styles"]
    assert len(resources["notebook_styles"]["stylesheet"]) == 2


def test_preprocess_cell_with_class_metadata():
    """Test preprocessing a cell with custom class metadata."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("x = 1")
    cell.metadata["class"] = "my-custom-class"

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 0)

    assert "cell_class" in processed_cell.metadata
    assert processed_cell.metadata["cell_class"] == "my-custom-class"


def test_preprocess_cell_with_input_class():
    """Test preprocessing a cell with input-class metadata."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("x = 1")
    cell.metadata["input-class"] = "custom-input-class"

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 0)

    assert "input_cell_class" in processed_cell.metadata
    assert processed_cell.metadata["input_cell_class"] == "custom-input-class"


def test_preprocess_cell_with_output_class():
    """Test preprocessing a cell with output-class metadata."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("print('test')")
    cell.metadata["output-class"] = "custom-output-class"

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 0)

    assert "output_cell_class" in processed_cell.metadata
    assert processed_cell.metadata["output_cell_class"] == "custom-output-class"


def test_preprocess_cell_with_all_classes():
    """Test preprocessing a cell with cell, input, and output class metadata."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("x = 42")
    cell.metadata["class"] = "custom-cell"
    cell.metadata["input-class"] = "custom-input"
    cell.metadata["output-class"] = "custom-output"

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 1)

    assert "cell_class" in processed_cell.metadata
    assert processed_cell.metadata["cell_class"] == "custom-cell"
    assert "input_cell_class" in processed_cell.metadata
    assert processed_cell.metadata["input_cell_class"] == "custom-input"
    assert "output_cell_class" in processed_cell.metadata
    assert processed_cell.metadata["output_cell_class"] == "custom-output"


def test_preprocess_cell_with_multiple_classes():
    """Test preprocessing a cell with multiple CSS classes."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("y = 2")
    cell.metadata["class"] = "class1 class2 class3"

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 0)

    assert "cell_class" in processed_cell.metadata
    assert processed_cell.metadata["cell_class"] == "class1 class2 class3"


def test_preprocess_cell_with_classes_and_styles():
    """Test preprocessing a cell with both classes and styles."""
    preprocessor = StylePreprocessor()

    cell = new_code_cell("z = 3")
    cell.metadata["class"] = "highlight"
    cell.metadata["style"] = {"background-color": "#ffff00"}
    cell.metadata["input-class"] = "code-highlight"
    cell.metadata["input-style"] = {"border": "2px solid red"}

    processed_cell, resources = preprocessor.preprocess_cell(cell, {"styles": {}}, 0)

    assert "cell_class" in processed_cell.metadata
    assert processed_cell.metadata["cell_class"] == "highlight"
    assert "cell_style" in processed_cell.metadata
    assert processed_cell.metadata["cell_style"]["background-color"] == "#ffff00"
    assert "input_cell_class" in processed_cell.metadata
    assert processed_cell.metadata["input_cell_class"] == "code-highlight"
    assert "input_cell_style" in processed_cell.metadata
    assert "cell-0-input" in resources["styles"]
