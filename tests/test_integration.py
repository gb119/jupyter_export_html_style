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
