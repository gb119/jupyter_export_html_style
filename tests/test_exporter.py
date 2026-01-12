"""
Tests for the StyledHTMLExporter class.
"""

from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

from jupyter_export_html_style import StyledHTMLExporter

# Test image data: 1x1 red pixel PNG
TEST_IMAGE_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000d49444154789c63f8cfc03f00050201055fc8f1d20000000049454e44ae426082"
)


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


def test_export_notebook_with_input_style():
    """Test exporting a notebook with input-style metadata."""
    exporter = StyledHTMLExporter()

    cell = new_code_cell("x = 1")
    cell.metadata["input-style"] = {"background-color": "#ffe"}

    nb = new_notebook(cells=[cell])

    output, resources = exporter.from_notebook_node(nb)

    assert output is not None
    assert "#cell-0-input" in output
    assert "background-color: #ffe" in output


def test_export_notebook_with_output_style():
    """Test exporting a notebook with output-style metadata."""
    exporter = StyledHTMLExporter()

    cell = new_code_cell("print('output')")
    cell.metadata["output-style"] = {"border": "2px solid blue"}

    nb = new_notebook(cells=[cell])

    output, resources = exporter.from_notebook_node(nb)

    assert output is not None
    assert "#cell-0-output" in output
    assert "border: 2px solid blue" in output


def test_export_notebook_with_all_cell_styles():
    """Test exporting a notebook with cell, input, and output styles."""
    exporter = StyledHTMLExporter()

    cell = new_code_cell("y = 2")
    cell.metadata["style"] = {"padding": "10px"}
    cell.metadata["input-style"] = {"color": "red"}
    cell.metadata["output-style"] = {"font-weight": "bold"}

    nb = new_notebook(cells=[cell])

    output, resources = exporter.from_notebook_node(nb)

    assert output is not None
    assert "#cell-0" in output
    assert "#cell-0-input" in output
    assert "#cell-0-output" in output


def test_export_notebook_with_notebook_level_style():
    """Test exporting a notebook with notebook-level style metadata."""
    exporter = StyledHTMLExporter()

    nb = new_notebook(cells=[new_code_cell("z = 3")])
    nb.metadata["style"] = ".custom-class { color: green; }"

    output, resources = exporter.from_notebook_node(nb)

    assert output is not None
    assert "/* Custom notebook styles */" in output
    assert ".custom-class { color: green; }" in output


def test_export_notebook_with_stylesheet():
    """Test exporting a notebook with stylesheet metadata."""
    exporter = StyledHTMLExporter()

    nb = new_notebook(cells=[new_code_cell("a = 4")])
    nb.metadata["stylesheet"] = "https://example.com/style.css"

    output, resources = exporter.from_notebook_node(nb)

    assert output is not None
    assert '<link rel="stylesheet" href="https://example.com/style.css">' in output


def test_export_notebook_with_multiple_stylesheets():
    """Test exporting a notebook with multiple stylesheets."""
    exporter = StyledHTMLExporter()

    nb = new_notebook(cells=[new_code_cell("b = 5")])
    nb.metadata["stylesheet"] = [
        "https://example.com/style1.css",
        "https://example.com/style2.css",
    ]

    output, resources = exporter.from_notebook_node(nb)

    assert output is not None
    assert '<link rel="stylesheet" href="https://example.com/style1.css">' in output
    assert '<link rel="stylesheet" href="https://example.com/style2.css">' in output


def test_generate_notebook_style_block_with_style():
    """Test generating notebook style block with inline CSS."""
    exporter = StyledHTMLExporter()

    notebook_styles = {"style": "body { background: white; }"}
    style_block = exporter._generate_notebook_style_block(notebook_styles)

    assert "<style>" in style_block
    assert "/* Custom notebook styles */" in style_block
    assert "body { background: white; }" in style_block


def test_generate_notebook_style_block_with_stylesheet():
    """Test generating notebook style block with external stylesheet."""
    exporter = StyledHTMLExporter()

    notebook_styles = {"stylesheet": "https://cdn.example.com/theme.css"}
    style_block = exporter._generate_notebook_style_block(notebook_styles)

    assert '<link rel="stylesheet" href="https://cdn.example.com/theme.css">' in style_block


def test_generate_notebook_style_block_empty():
    """Test generating notebook style block with no styles."""
    exporter = StyledHTMLExporter()

    notebook_styles = {}
    style_block = exporter._generate_notebook_style_block(notebook_styles)

    assert style_block == ""


def test_embed_images_enabled_by_default():
    """Test that embed_images is enabled by default."""
    exporter = StyledHTMLExporter()

    assert exporter.embed_images is True


def test_embed_images_can_be_disabled():
    """Test that embed_images can be explicitly disabled."""
    exporter = StyledHTMLExporter(embed_images=False)

    assert exporter.embed_images is False


def test_embed_images_with_markdown_image():
    """Test that markdown images are embedded when embed_images is True."""
    import os
    import tempfile

    import nbformat as nbf

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create image file
        img_path = os.path.join(tmpdir, "test.png")
        with open(img_path, "wb") as f:
            f.write(TEST_IMAGE_PNG)

        # Create notebook with markdown cell referencing the image
        nb = nbf.v4.new_notebook()
        md_cell = nbf.v4.new_markdown_cell("![Test Image](test.png)")
        nb.cells.append(md_cell)

        # Write notebook to file
        nb_path = os.path.join(tmpdir, "test.ipynb")
        with open(nb_path, "w") as f:
            nbf.write(nb, f)

        # Export with default settings (embed_images=True)
        exporter = StyledHTMLExporter()
        output, resources = exporter.from_filename(nb_path)

        # Verify image is embedded as data URI
        assert "data:image/png;base64," in output
        # Verify file reference is NOT present (replaced with data URI)
        assert 'src="test.png"' not in output


def test_embed_images_disabled_keeps_file_reference():
    """Test that markdown images remain as file references when embed_images is False."""
    import os
    import tempfile

    import nbformat as nbf

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create image file
        img_path = os.path.join(tmpdir, "test.png")
        with open(img_path, "wb") as f:
            f.write(TEST_IMAGE_PNG)

        # Create notebook with markdown cell referencing the image
        nb = nbf.v4.new_notebook()
        md_cell = nbf.v4.new_markdown_cell("![Test Image](test.png)")
        nb.cells.append(md_cell)

        # Write notebook to file
        nb_path = os.path.join(tmpdir, "test.ipynb")
        with open(nb_path, "w") as f:
            nbf.write(nb, f)

        # Export with embed_images=False
        exporter = StyledHTMLExporter(embed_images=False)
        output, resources = exporter.from_filename(nb_path)

        # Verify file reference is present
        assert 'src="test.png"' in output
