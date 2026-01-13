"""
Tests for the StyledWebPDFExporter class.

These tests verify that the StyledWebPDFExporter correctly extends
WebPDFExporter functionality to use StyledHTMLExporter for HTML generation,
ensuring that cell styles and embedded images are included in the PDF output.
"""

from importlib import util as importlib_util

import pytest
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

from jupyter_export_html_style import StyledWebPDFExporter

# Check if playwright is available
PLAYWRIGHT_AVAILABLE = importlib_util.find_spec("playwright") is not None


def test_styled_webpdf_exporter_initialization():
    """Test that StyledWebPDFExporter can be initialized."""
    exporter = StyledWebPDFExporter()
    assert exporter.template_name == "webpdf"
    assert exporter.export_from_notebook == "Styled PDF via HTML"


def test_styled_webpdf_exporter_inherits_from_styled_html():
    """Test that StyledWebPDFExporter inherits from StyledHTMLExporter."""
    from jupyter_export_html_style import StyledHTMLExporter

    exporter = StyledWebPDFExporter()
    assert isinstance(exporter, StyledHTMLExporter)


def test_styled_webpdf_exporter_has_pdf_settings():
    """Test that StyledWebPDFExporter has the expected PDF-related settings."""
    exporter = StyledWebPDFExporter()

    # Check default values
    assert hasattr(exporter, "allow_chromium_download")
    assert exporter.allow_chromium_download is False

    assert hasattr(exporter, "paginate")
    assert exporter.paginate is True

    assert hasattr(exporter, "disable_sandbox")
    assert exporter.disable_sandbox is False


def test_styled_webpdf_exporter_pdf_settings_configurable():
    """Test that PDF settings can be configured."""
    exporter = StyledWebPDFExporter(
        allow_chromium_download=True, paginate=False, disable_sandbox=True
    )

    assert exporter.allow_chromium_download is True
    assert exporter.paginate is False
    assert exporter.disable_sandbox is True


def test_styled_webpdf_file_extension():
    """Test that the file extension defaults to .html during processing."""
    exporter = StyledWebPDFExporter()
    # file_extension is used internally during HTML generation
    assert exporter.file_extension == ".html"


@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not installed")
def test_styled_webpdf_export_simple_notebook():
    """Test exporting a simple notebook to PDF (requires playwright).

    This test verifies that the exporter can generate PDF output and that
    the output_extension is correctly set to .pdf.
    """
    exporter = StyledWebPDFExporter()

    nb = new_notebook(cells=[new_code_cell("print('hello')"), new_markdown_cell("# Title")])

    try:
        output, resources = exporter.from_notebook_node(nb)

        # Verify output is binary (PDF data)
        assert output is not None
        assert isinstance(output, bytes)
        assert len(output) > 0

        # Verify output extension is set to .pdf
        assert resources["output_extension"] == ".pdf"

        # Verify it looks like a PDF (starts with PDF magic bytes)
        assert output.startswith(b"%PDF-")
    except RuntimeError as e:
        # If chromium is not installed, skip the test
        if "No suitable chromium executable" in str(e):
            pytest.skip("Chromium not installed")
        raise


@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not installed")
def test_styled_webpdf_export_with_styles():
    """Test exporting a notebook with styles to PDF (requires playwright).

    This test verifies that the StyledWebPDFExporter uses StyledHTMLExporter
    to include cell styles in the HTML before converting to PDF.
    """
    exporter = StyledWebPDFExporter()

    cell = new_code_cell("print('styled')")
    cell.metadata["style"] = {"background-color": "#f0f0f0"}

    nb = new_notebook(cells=[cell])

    try:
        output, resources = exporter.from_notebook_node(nb)

        # Verify output is binary (PDF data)
        assert output is not None
        assert isinstance(output, bytes)
        assert len(output) > 0

        # Verify output extension is set to .pdf
        assert resources["output_extension"] == ".pdf"

        # Verify it looks like a PDF
        assert output.startswith(b"%PDF-")

        # Note: We can't easily verify that styles are actually applied in the PDF
        # without parsing the PDF, but we can verify that the exporter runs
        # successfully with styled notebooks
    except RuntimeError as e:
        # If chromium is not installed, skip the test
        if "No suitable chromium executable" in str(e):
            pytest.skip("Chromium not installed")
        raise


def test_styled_webpdf_run_playwright_raises_without_playwright():
    """Test that run_playwright raises RuntimeError if playwright is not installed."""
    if PLAYWRIGHT_AVAILABLE:
        pytest.skip("Playwright is installed, test not applicable")

    exporter = StyledWebPDFExporter()
    html = "<html><body>Test</body></html>"

    with pytest.raises(RuntimeError, match="Playwright is not installed"):
        exporter.run_playwright(html)
