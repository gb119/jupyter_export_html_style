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
    assert exporter.export_from_notebook == "PDF via HTML (with styles)"


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


def test_styled_webpdf_html_includes_cell_styles():
    """Test that the HTML generated by StyledWebPDFExporter includes custom cell styles.

    This test verifies that the webpdf exporter generates HTML with:
    1. CSS rules for styled cells (#cell-0, #cell-0-input, #cell-0-output)
    2. HTML elements with matching id attributes
    This ensures that custom cell styles will be applied in the final PDF.
    """
    exporter = StyledWebPDFExporter()

    # Create notebook with various cell styles
    cell1 = new_code_cell("print('cell with style')")
    cell1.metadata["style"] = {"background-color": "#f0f0f0"}

    cell2 = new_code_cell("x = 1")
    cell2.metadata["input-style"] = {"color": "red"}

    cell3 = new_markdown_cell("# Markdown")
    cell3.metadata["style"] = {"padding": "10px"}

    nb = new_notebook(cells=[cell1, cell2, cell3])

    # Mock run_playwright to capture HTML
    html_captured = None

    def mock_run_playwright(html):
        nonlocal html_captured
        html_captured = html
        return b"fake pdf"

    exporter.run_playwright = mock_run_playwright

    # Export notebook
    output, resources = exporter.from_notebook_node(nb)

    # Verify HTML was captured
    assert html_captured is not None

    # Verify CSS rules are present
    assert "Custom cell styles" in html_captured
    assert "#cell-0 {" in html_captured
    assert "background-color: #f0f0f0" in html_captured
    assert "#cell-1-input {" in html_captured
    assert "color: red" in html_captured
    assert "#cell-2 {" in html_captured
    assert "padding: 10px" in html_captured

    # Verify HTML elements with matching IDs are present
    assert 'id="cell-0"' in html_captured
    assert 'id="cell-1"' in html_captured
    assert 'id="cell-1-input"' in html_captured
    assert 'id="cell-2"' in html_captured


@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not installed")
def test_styled_webpdf_uses_tagged_pdf():
    """Test that the exporter passes tagged=True to page.pdf().

    This test verifies that the StyledWebPDFExporter passes the tagged=True
    parameter to Playwright's page.pdf() method, ensuring the output PDFs
    are tagged for accessibility.
    """
    from unittest.mock import AsyncMock, MagicMock, patch

    exporter = StyledWebPDFExporter()

    # Create a simple notebook
    nb = new_notebook(cells=[new_code_cell("print('test')")])

    # Mock the playwright components
    mock_pdf_data = b"%PDF-1.4 fake pdf data"
    mock_page = AsyncMock()
    mock_page.pdf = AsyncMock(return_value=mock_pdf_data)
    mock_page.emulate_media = AsyncMock()
    mock_page.goto = AsyncMock()
    mock_page.wait_for_timeout = AsyncMock()
    mock_page.evaluate = AsyncMock(return_value={"width": 800, "height": 600})

    mock_browser = AsyncMock()
    mock_browser.new_page = AsyncMock(return_value=mock_page)
    mock_browser.close = AsyncMock()

    mock_chromium = MagicMock()
    mock_chromium.launch = AsyncMock(return_value=mock_browser)

    mock_playwright = AsyncMock()
    mock_playwright.chromium = mock_chromium
    mock_playwright.stop = AsyncMock()

    async def mock_async_playwright_start():
        return mock_playwright

    mock_async_playwright_instance = MagicMock()
    mock_async_playwright_instance.start = mock_async_playwright_start

    def mock_async_playwright():
        return mock_async_playwright_instance

    with patch(
        "playwright.async_api.async_playwright",
        mock_async_playwright,
    ):
        try:
            output, resources = exporter.from_notebook_node(nb)

            # Verify that page.pdf was called with tagged=True
            mock_page.pdf.assert_called_once()
            call_kwargs = mock_page.pdf.call_args.kwargs
            assert "tagged" in call_kwargs, "tagged parameter not passed to page.pdf()"
            assert call_kwargs["tagged"] is True, "tagged parameter is not True in page.pdf() call"
            assert call_kwargs["print_background"] is True, "print_background should be True"

            # Verify the output
            assert output == mock_pdf_data
            assert resources["output_extension"] == ".pdf"

        except RuntimeError as e:
            if "No suitable chromium executable" in str(e):
                pytest.skip("Chromium not installed")
            raise
