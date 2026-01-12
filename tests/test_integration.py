"""
Integration tests for jupyter_export_html_style.
"""

from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

from jupyter_export_html_style import StyledHTMLExporter, StylePreprocessor


def test_full_export_pipeline():
    """Test the complete export pipeline from notebook to HTML."""
    # Create a notebook with styled cells
    cells = [
        new_markdown_cell("# Test Notebook"),
        new_code_cell("print('hello')"),
        new_code_cell("print('world')"),
    ]

    # Add styles to cells
    cells[1].metadata["style"] = {"background-color": "#f0f0f0"}
    cells[2].metadata["style"] = "border: 2px solid red;"

    nb = new_notebook(cells=cells)

    # Export with StyledHTMLExporter
    exporter = StyledHTMLExporter()
    output, resources = exporter.from_notebook_node(nb)

    # Verify output
    assert output is not None
    assert isinstance(output, str)
    assert len(output) > 0

    # Verify styles are present
    assert resources is not None
    assert "styles" in resources


def test_preprocessor_exporter_integration():
    """Test that preprocessor correctly feeds data to exporter."""
    # Create notebook
    cell = new_code_cell("x = 42")
    cell.metadata["style"] = {"color": "blue", "font-weight": "bold"}

    nb = new_notebook(cells=[cell])

    # First, test preprocessor alone
    preprocessor = StylePreprocessor()
    processed_nb, resources = preprocessor.preprocess(nb, {})

    assert "styles" in resources
    assert len(resources["styles"]) == 1

    # Then test full export
    exporter = StyledHTMLExporter()
    output, final_resources = exporter.from_notebook_node(nb)

    assert output is not None
    assert "styles" in final_resources


def test_multiple_cells_with_mixed_styles():
    """Test exporting notebook with various style formats."""
    cells = [
        new_code_cell("a = 1"),
        new_code_cell("b = 2"),
        new_code_cell("c = 3"),
        new_markdown_cell("## Summary"),
    ]

    # Different style formats
    cells[0].metadata["style"] = {"background-color": "#fff"}
    cells[1].metadata["style"] = "padding: 10px;"
    cells[2].metadata["style"] = {"border": "1px solid #000", "margin": "5px"}
    # cells[3] has no style

    nb = new_notebook(cells=cells)

    exporter = StyledHTMLExporter()
    output, resources = exporter.from_notebook_node(nb)

    assert output is not None
    assert "styles" in resources
    assert len(resources["styles"]) == 3


def test_custom_style_metadata_key():
    """Test using a custom metadata key for styles."""
    preprocessor = StylePreprocessor()
    preprocessor.style_metadata_key = "custom_style"

    cell = new_code_cell("y = 10")
    cell.metadata["custom_style"] = {"color": "green"}

    nb = new_notebook(cells=[cell])

    processed_nb, resources = preprocessor.preprocess(nb, {})

    assert "styles" in resources
    assert len(resources["styles"]) == 1
    assert resources["styles"]["cell-0"]["color"] == "green"


def test_integration_input_output_styles():
    """Test full integration with input-style and output-style metadata."""
    cells = [
        new_code_cell("x = 1"),
        new_code_cell("print('output')"),
    ]

    # Add input and output styles
    cells[0].metadata["input-style"] = {"background-color": "#f9f9f9"}
    cells[1].metadata["output-style"] = {"border": "1px dashed #999"}

    nb = new_notebook(cells=cells)

    exporter = StyledHTMLExporter()
    output, resources = exporter.from_notebook_node(nb)

    # Verify styles are present in output
    assert "#cell-0-input" in output
    assert "background-color: #f9f9f9" in output
    assert "#cell-1-output" in output
    assert "border: 1px dashed #999" in output


def test_integration_notebook_level_styles():
    """Test full integration with notebook-level style and stylesheet."""
    nb = new_notebook(cells=[new_code_cell("a = 1"), new_markdown_cell("# Title")])

    # Add notebook-level metadata
    nb.metadata["style"] = ".jp-Cell { border-radius: 5px; }"
    nb.metadata["stylesheet"] = "https://cdn.example.com/custom.css"

    exporter = StyledHTMLExporter()
    output, resources = exporter.from_notebook_node(nb)

    # Verify notebook styles are present
    assert "/* Custom notebook styles */" in output
    assert ".jp-Cell { border-radius: 5px; }" in output
    assert '<link rel="stylesheet" href="https://cdn.example.com/custom.css">' in output


def test_integration_all_style_types():
    """Test full integration with all style types together."""
    cells = [
        new_code_cell("x = 1"),
        new_code_cell("y = 2"),
    ]

    # Add all types of styles
    cells[0].metadata["style"] = {"margin": "10px"}
    cells[0].metadata["input-style"] = {"color": "#333"}
    cells[0].metadata["output-style"] = {"font-family": "monospace"}

    nb = new_notebook(cells=cells)
    nb.metadata["style"] = "body { max-width: 1200px; }"
    nb.metadata["stylesheet"] = ["style1.css", "style2.css"]

    exporter = StyledHTMLExporter()
    output, resources = exporter.from_notebook_node(nb)

    # Verify all styles are present
    assert "#cell-0" in output
    assert "margin: 10px" in output
    assert "#cell-0-input" in output
    assert "color: #333" in output
    assert "#cell-0-output" in output
    assert "font-family: monospace" in output
    assert "body { max-width: 1200px; }" in output
    assert '<link rel="stylesheet" href="style1.css">' in output
    assert '<link rel="stylesheet" href="style2.css">' in output
