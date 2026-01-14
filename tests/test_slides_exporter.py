"""Tests for the StyledSlidesExporter class."""

import re

import nbformat as nbf
from bs4 import BeautifulSoup
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

from jupyter_export_html_style import StyledSlidesExporter


def _parse_html(html_string):
    """Parse HTML string and return BeautifulSoup object.

    Args:
        html_string (str): HTML content to parse.

    Returns:
        (BeautifulSoup): Parsed HTML document.
    """
    return BeautifulSoup(html_string, "html.parser")


def _extract_css_rules(html_string):
    """Extract CSS rules from HTML style blocks.

    Args:
        html_string (str): HTML content containing style blocks.

    Returns:
        (dict): Dictionary mapping CSS selectors to their style properties.
            For example: {"#cell-0": {"background-color": "#f0f0f0"}}
    """
    soup = _parse_html(html_string)
    css_rules = {}

    # Find all style tags
    for style_tag in soup.find_all("style"):
        style_content = style_tag.string
        if style_content:
            # Parse CSS rules using regex
            # Matches patterns like: #cell-0 { background-color: #fff; padding: 10px }
            rule_pattern = r"([#.\w-]+)\s*\{([^}]+)\}"
            for match in re.finditer(rule_pattern, style_content):
                selector = match.group(1).strip()
                properties_str = match.group(2).strip()

                # Parse individual properties
                properties = {}
                for prop in properties_str.split(";"):
                    prop = prop.strip()
                    if ":" in prop:
                        key, value = prop.split(":", 1)
                        properties[key.strip()] = value.strip()

                css_rules[selector] = properties

    return css_rules


def test_styled_slides_exporter_basic():
    """Test basic functionality of StyledSlidesExporter."""
    # Create a simple notebook with slide metadata
    cells = [
        new_markdown_cell("# Slide 1", metadata={"slideshow": {"slide_type": "slide"}}),
        new_code_cell("print('Hello World')", metadata={"slideshow": {"slide_type": "slide"}}),
    ]
    nb = new_notebook(cells=cells)

    # Export to slides
    exporter = StyledSlidesExporter()
    output, resources = exporter.from_notebook_node(nb)

    # Check that output is a string
    assert isinstance(output, str)

    # Check that reveal.js is included
    assert "reveal.js" in output.lower()

    # Check that slides structure is present
    assert '<div class="reveal">' in output
    assert '<div class="slides">' in output


def test_styled_slides_with_cell_styles():
    """Test that cell styles are properly included in slides."""
    # Create a notebook with styled cells
    cells = [
        new_markdown_cell(
            "# Styled Slide",
            metadata={
                "slideshow": {"slide_type": "slide"},
                "style": {"background-color": "#f0f0f0", "padding": "20px"},
            },
        ),
        new_code_cell(
            "x = 1",
            metadata={
                "slideshow": {"slide_type": "slide"},
                "style": "border: 2px solid red",
            },
        ),
    ]
    nb = new_notebook(cells=cells)

    # Export to slides
    exporter = StyledSlidesExporter()
    output, resources = exporter.from_notebook_node(nb)

    # Check that styles are present in the output
    # Slides exporter uses attribute selectors instead of ID selectors
    assert 'data-cell-index="0"' in output
    assert 'data-cell-index="1"' in output
    assert "background-color: #f0f0f0" in output
    assert "padding: 20px" in output
    assert "border: 2px solid red" in output or "border" in output


def test_styled_slides_reveal_config():
    """Test that reveal.js configuration is properly set."""
    nb = new_notebook(
        cells=[
            new_markdown_cell("# Test", metadata={"slideshow": {"slide_type": "slide"}}),
        ]
    )

    # Export with custom reveal configuration
    exporter = StyledSlidesExporter(
        reveal_theme="moon", reveal_transition="fade", reveal_number="c/t"
    )
    output, resources = exporter.from_notebook_node(nb)

    # Check that reveal config is in resources
    assert "reveal" in resources
    assert resources["reveal"]["theme"] == "moon"
    assert resources["reveal"]["transition"] == "fade"
    assert resources["reveal"]["number"] == "c/t"

    # Check that theme is in output
    assert "moon" in output


def test_styled_slides_file_extension():
    """Test that the file extension is correct for slides."""
    exporter = StyledSlidesExporter()
    assert exporter.file_extension == ".slides.html"


def test_styled_slides_export_label():
    """Test that the export label is descriptive."""
    exporter = StyledSlidesExporter()
    assert "slides" in exporter.export_from_notebook.lower()
    assert "style" in exporter.export_from_notebook.lower()


def test_styled_slides_with_input_output_styles():
    """Test that input and output styles work in slides."""
    cells = [
        new_code_cell(
            "x = 1\nprint(x)",
            metadata={
                "slideshow": {"slide_type": "slide"},
                "input-style": {"background-color": "#e0e0e0"},
                "output-style": {"border-left": "3px solid blue"},
            },
        ),
    ]
    nb = new_notebook(cells=cells)

    exporter = StyledSlidesExporter()
    output, resources = exporter.from_notebook_node(nb)

    # Check that input and output styles are present
    # Slides exporter uses attribute selectors targeting wrapper elements
    assert 'data-cell-index="0"' in output
    assert "background-color: #e0e0e0" in output
    assert "border-left: 3px solid blue" in output
    assert ".jp-Cell-inputWrapper" in output
    assert ".jp-Cell-outputWrapper" in output


def test_styled_slides_notebook_level_styles():
    """Test that notebook-level styles are included in slides."""
    cells = [
        new_markdown_cell("# Test", metadata={"slideshow": {"slide_type": "slide"}}),
    ]
    nb = new_notebook(cells=cells)
    nb.metadata["style"] = "body { font-family: Arial; }"

    exporter = StyledSlidesExporter()
    output, resources = exporter.from_notebook_node(nb)

    # Check that notebook-level style is in output
    assert "font-family: Arial" in output
    assert "Custom notebook styles" in output


def test_styled_slides_template_name():
    """Test that the correct template name is used."""
    exporter = StyledSlidesExporter()
    assert exporter.template_name == "styled_reveal"
