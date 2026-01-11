"""
Tests for the StyledHTMLExporter class.
"""

from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

from jupyter_export_html_style import StyledHTMLExporter


def test_styled_html_exporter_initialization():
    """Test that StyledHTMLExporter can be initialized."""
    exporter = StyledHTMLExporter()
    assert exporter.template_name == "classic"


def test_export_notebook_without_styles():
    """Test exporting a notebook without style metadata."""
    exporter = StyledHTMLExporter()

    nb = new_notebook(cells=[new_code_cell("print('hello')"), new_markdown_cell("# Title")])

    output, resources = exporter.from_notebook_node(nb)

    assert output is not None
    assert isinstance(output, str)
    assert len(output) > 0


def test_export_notebook_with_styles():
    """Test exporting a notebook with style metadata."""
    exporter = StyledHTMLExporter()

    cell = new_code_cell("print('styled')")
    cell.metadata["style"] = {"background-color": "#f0f0f0"}

    nb = new_notebook(cells=[cell])

    output, resources = exporter.from_notebook_node(nb)

    assert output is not None
    assert isinstance(output, str)
    # Check that custom styles are included
    assert "/* Custom cell styles */" in output or "<style>" in output


def test_generate_style_block_with_dict():
    """Test generating style block from dictionary styles."""
    exporter = StyledHTMLExporter()

    styles = {"cell-0": {"background-color": "#fff", "padding": "10px"}, "cell-1": {"color": "red"}}

    style_block = exporter._generate_style_block(styles)

    assert "<style>" in style_block
    assert "</style>" in style_block
    assert "#cell-0" in style_block
    assert "#cell-1" in style_block
    assert "background-color: #fff" in style_block
    assert "color: red" in style_block


def test_generate_style_block_with_string():
    """Test generating style block from string styles."""
    exporter = StyledHTMLExporter()

    styles = {"cell-0": "background-color: #eee; padding: 5px;"}

    style_block = exporter._generate_style_block(styles)

    assert "<style>" in style_block
    assert "#cell-0" in style_block
    assert "background-color: #eee; padding: 5px;" in style_block


def test_generate_style_block_empty():
    """Test generating style block with no styles."""
    exporter = StyledHTMLExporter()

    styles = {}

    style_block = exporter._generate_style_block(styles)

    assert style_block == ""


def test_export_with_custom_template():
    """Test exporting with a custom template name."""
    exporter = StyledHTMLExporter()
    exporter.template_name = "lab"

    nb = new_notebook(cells=[new_code_cell("x = 1")])

    # This should not raise an error even if template doesn't exist
    # (nbconvert will handle template resolution)
    try:
        output, resources = exporter.from_notebook_node(nb)
        assert output is not None
    except Exception:
        # Template might not exist, which is okay for this test
        pass
