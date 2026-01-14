"""WebPDF exporter with style support."""

import asyncio
import concurrent.futures
import os
import subprocess
import sys
import tempfile
from importlib import util as importlib_util

from traitlets import Bool, default

from .html import StyledHTMLExporter

PLAYWRIGHT_INSTALLED = importlib_util.find_spec("playwright") is not None
IS_WINDOWS = os.name == "nt"


class StyledWebPDFExporter(StyledHTMLExporter):
    """Writer designed to write to PDF files with style support.

    This inherits from :class:`StyledHTMLExporter`. It creates the HTML using the
    StyledHTMLExporter (which includes custom styles and embedded images), and then
    runs playwright to create a pdf.

    This exporter extends the standard WebPDFExporter to use StyledHTMLExporter
    instead of the basic HTMLExporter, allowing cell-level styles and embedded
    images to be included in the PDF output.

    Attributes:
        export_from_notebook (str): Label for the export option.
        allow_chromium_download (Bool): Whether to allow downloading Chromium
            if no suitable version is found on the system.
        paginate (Bool): Split generated notebook into multiple pages. If False,
            a PDF with one long page will be generated.
        disable_sandbox (Bool): Disable chromium security sandbox when converting
            to PDF. WARNING: This could cause arbitrary code execution in specific
            circumstances. This is required for webpdf to work inside most
            container environments.

    Examples:
        >>> from jupyter_export_html_style import StyledWebPDFExporter
        >>> exporter = StyledWebPDFExporter()
        >>> output, resources = exporter.from_notebook_node(notebook)
    """

    export_from_notebook = "PDF via HTML (with styles)"

    allow_chromium_download = Bool(
        False,
        help="Whether to allow downloading Chromium if no suitable version is found on the system.",
    ).tag(config=True)

    paginate = Bool(
        True,
        help="""
        Split generated notebook into multiple pages.

        If False, a PDF with one long page will be generated.

        Set to True to match behavior of LaTeX based PDF generator
        """,
    ).tag(config=True)

    @default("file_extension")
    def _file_extension_default(self):
        return ".html"

    @default("template_name")
    def _template_name_default(self):
        return "webpdf"

    disable_sandbox = Bool(
        False,
        help="""
        Disable chromium security sandbox when converting to PDF.

        WARNING: This could cause arbitrary code execution in specific circumstances,
        where JS in your notebook can execute serverside code! Please use with
        caution.

        ``https://github.com/puppeteer/puppeteer/blob/main@%7B2020-12-14T17:22:24Z%7D/docs/troubleshooting.md#setting-up-chrome-linux-sandbox``
        has more information.

        This is required for webpdf to work inside most container environments.
        """,
    ).tag(config=True)

    def run_playwright(self, html):
        """Run playwright to convert HTML to PDF.

        Args:
            html (str): The HTML content to convert to PDF.

        Returns:
            (bytes): PDF data.

        Raises:
            RuntimeError: If playwright is not installed or no suitable
                chromium executable is found.
        """

        async def main(temp_file):
            """Run main playwright script."""
            args = ["--no-sandbox"] if self.disable_sandbox else []
            try:
                from playwright.async_api import async_playwright  # type: ignore[import-not-found]
            except ModuleNotFoundError as e:
                msg = (
                    "Playwright is not installed to support Web PDF conversion. "
                    "Please install `nbconvert[webpdf]` to enable."
                )
                raise RuntimeError(msg) from e

            if self.allow_chromium_download:
                cmd = [sys.executable, "-m", "playwright", "install", "chromium"]
                subprocess.check_call(cmd)  # noqa: S603

            playwright = await async_playwright().start()
            chromium = playwright.chromium

            try:
                browser = await chromium.launch(
                    handle_sigint=False, handle_sigterm=False, handle_sighup=False, args=args
                )
            except Exception as e:
                msg = (
                    "No suitable chromium executable found on the system. "
                    "Please use 'allow_chromium_download=True' to allow downloading one, "
                    "or install it using `playwright install chromium`."
                )
                await playwright.stop()
                raise RuntimeError(msg) from e

            page = await browser.new_page()
            await page.emulate_media(media="print")
            await page.wait_for_timeout(100)
            await page.goto(f"file://{temp_file.name}", wait_until="networkidle")
            await page.wait_for_timeout(100)

            pdf_params = {"print_background": True, "tagged": True}
            if not self.paginate:
                # Floating point precision errors cause the printed
                # PDF from spilling over a new page by a pixel fraction.
                dimensions = await page.evaluate(
                    """() => {
                    const rect = document.body.getBoundingClientRect();
                    return {
                    width: Math.ceil(rect.width) + 1,
                    height: Math.ceil(rect.height) + 1,
                    }
                }"""
                )
                width = dimensions["width"]
                height = dimensions["height"]
                # 200 inches is the maximum size for Adobe Acrobat Reader.
                pdf_params.update(
                    {
                        "width": min(width, 200 * 72),
                        "height": min(height, 200 * 72),
                    }
                )
            pdf_data = await page.pdf(**pdf_params)

            await browser.close()
            await playwright.stop()
            return pdf_data

        pool = concurrent.futures.ThreadPoolExecutor()
        # Create a temporary file to pass the HTML code to Chromium:
        # Unfortunately, tempfile on Windows does not allow for an already open
        # file to be opened by a separate process. So we must close it first
        # before calling Chromium. We also specify delete=False to ensure the
        # file is not deleted after closing (the default behavior).
        temp_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        with temp_file:
            temp_file.write(html.encode("utf-8"))
        try:

            def run_coroutine(coro):
                """Run an internal coroutine."""
                if IS_WINDOWS:
                    # For Windows, explicitly set WindowsProactorEventLoopPolicy for subprocess support
                    # This is required when running asyncio in a thread pool on Windows
                    # See: https://docs.python.org/3/library/asyncio-platforms.html#windows
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                    loop = asyncio.new_event_loop()
                else:
                    loop = asyncio.new_event_loop()

                asyncio.set_event_loop(loop)
                return loop.run_until_complete(coro)

            pdf_data = pool.submit(run_coroutine, main(temp_file)).result()
        finally:
            # Ensure the file is deleted even if playwright raises an exception
            os.unlink(temp_file.name)
        return pdf_data

    def from_notebook_node(self, nb, resources=None, **kw):
        """Convert from a notebook node to PDF with styles.

        Args:
            nb (NotebookNode): The notebook to convert.
            resources (dict, optional): Additional resources used in the conversion
                process. If None, an empty dictionary is created. Defaults to None.
            **kw (dict): Additional keyword arguments passed to the parent
                from_notebook_node method.

        Returns:
            (tuple): A tuple containing:
                - pdf_data (bytes): The PDF output.
                - resources (dict): Updated resources dictionary with
                    output_extension set to ".pdf".
        """
        # Use the parent StyledHTMLExporter to generate HTML with styles
        html, resources = super().from_notebook_node(nb, resources=resources, **kw)

        self.log.info("Building PDF with styles")
        pdf_data = self.run_playwright(html)
        self.log.info("PDF successfully created")

        # convert output extension to pdf
        # the writer above required it to be html
        resources["output_extension"] = ".pdf"

        return pdf_data, resources
