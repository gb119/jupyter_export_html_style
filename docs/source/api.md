# API Reference

## Module: jupyter_export_html_style

The main module providing nbconvert integration for styled HTML export.

### Classes

## StylePreprocessor

```{eval-rst}
.. class:: StylePreprocessor

   A nbconvert preprocessor that extracts and processes style metadata from notebook cells.
   
   This preprocessor examines each cell in a notebook for style-related metadata and
   prepares it for use in HTML export. Styles can be specified as either dictionaries
   or CSS strings.

   .. attribute:: style_metadata_key
      :type: str
      :value: "style"
      
      The metadata key to look for cell styles. Default is "style".
      Can be configured via nbconvert configuration.

   .. method:: preprocess(nb, resources)
   
      Preprocess the entire notebook.
      
      Extracts notebook-level style metadata (``style`` and ``stylesheet``) from the 
      notebook metadata and stores them in resources for later use in HTML generation.
      
      :param nb: The notebook to preprocess
      :type nb: NotebookNode
      :param resources: Additional resources used in the conversion process
      :type resources: dict
      :return: Tuple of processed notebook and updated resources
      :rtype: tuple(NotebookNode, dict)

   .. method:: preprocess_cell(cell, resources, index)
   
      Preprocess a single cell.
      
      Extracts style metadata from cells including:
      - ``style``: CSS styles for the entire cell container
      - ``input-style``: CSS styles for the cell's input area
      - ``output-style``: CSS styles for the cell's output area
      
      :param cell: The cell to preprocess
      :type cell: NotebookNode
      :param resources: Additional resources used in the conversion process
      :type resources: dict
      :param index: The index of the cell in the notebook
      :type index: int
      :return: Tuple of processed cell and updated resources
      :rtype: tuple(NotebookNode, dict)
```

## StyledHTMLExporter

```{eval-rst}
.. class:: StyledHTMLExporter

   An HTML exporter that supports cell-level and notebook-level style customization.
   
   This exporter extends the standard nbconvert HTMLExporter to include
   custom styles defined in cell and notebook metadata. It automatically registers
   the StylePreprocessor and injects collected styles into the output HTML.
   
   **Supported Features:**
   
   - Cell-level styles via ``style`` metadata
   - Input area styling via ``input-style`` metadata
   - Output area styling via ``output-style`` metadata
   - Notebook-level styles via notebook metadata ``style`` key
   - External stylesheets via notebook metadata ``stylesheet`` key

   .. attribute:: template_name
      :type: str
      :value: "classic"
      
      Name of the template to use for HTML generation. Default is "classic".

   .. method:: from_notebook_node(nb, resources=None, **kw)
   
      Convert a notebook node to HTML with style support.
      
      Processes the notebook with the StylePreprocessor and injects all collected
      styles (cell-level and notebook-level) into the HTML output before the 
      closing ``</head>`` tag.
      
      :param nb: The notebook to convert
      :type nb: NotebookNode
      :param resources: Additional resources used in the conversion process
      :type resources: dict, optional
      :param kw: Additional keyword arguments
      :type kw: dict
      :return: Tuple of HTML output and updated resources
      :rtype: tuple(str, dict)
   
   .. method:: _generate_style_block(styles)
   
      Generate a CSS style block from collected cell styles.
      
      Converts style dictionaries and strings into CSS rules that target specific
      cell, input, and output elements by their IDs.
      
      :param styles: Dictionary mapping cell IDs to style definitions
      :type styles: dict
      :return: CSS style block as HTML string
      :rtype: str

   .. method:: _generate_notebook_style_block(notebook_styles)
   
      Generate style and stylesheet blocks from notebook-level metadata.
      
      Creates HTML link tags for external stylesheets and inline style tags for
      custom CSS. Supports both single stylesheet strings and lists of stylesheets.
      
      :param notebook_styles: Dictionary containing 'style' and/or 'stylesheet' keys
      :type notebook_styles: dict
      :return: HTML containing style and/or link elements
      :rtype: str
```

## StyledWebPDFExporter

```{eval-rst}
.. class:: StyledWebPDFExporter

   A PDF exporter that supports cell-level and notebook-level style customization.
   
   This exporter extends StyledHTMLExporter to generate PDF files via HTML using
   Playwright and Chromium. It preserves all custom styles, embedded images, and
   formatting when converting to PDF.
   
   **Supported Features:**
   
   - All features from StyledHTMLExporter (cell styles, notebook styles, embedded images)
   - PDF generation with Playwright and Chromium
   - Configurable pagination
   - Single-page or multi-page output
   - Container-friendly operation

   .. attribute:: template_name
      :type: str
      :value: "webpdf"
      
      Name of the template to use for HTML generation before PDF conversion.

   .. attribute:: paginate
      :type: bool
      :value: True
      
      Split the notebook into multiple pages. Set to False for a single long page.

   .. attribute:: allow_chromium_download
      :type: bool
      :value: False
      
      Whether to allow downloading Chromium if no suitable version is found.

   .. attribute:: disable_sandbox
      :type: bool
      :value: False
      
      Disable Chromium security sandbox. Required for container environments but
      reduces security. Use with caution.

   .. method:: from_notebook_node(nb, resources=None, **kw)
   
      Convert a notebook node to PDF with style support.
      
      First generates HTML using StyledHTMLExporter (including all custom styles),
      then converts the HTML to PDF using Playwright and Chromium.
      
      :param nb: The notebook to convert
      :type nb: NotebookNode
      :param resources: Additional resources used in the conversion process
      :type resources: dict, optional
      :param kw: Additional keyword arguments
      :type kw: dict
      :return: Tuple of PDF data and updated resources
      :rtype: tuple(bytes, dict)
      :raises RuntimeError: If Playwright is not installed or Chromium is not found

   .. method:: run_playwright(html)
   
      Run Playwright to convert HTML to PDF.
      
      Launches Chromium, loads the HTML content, and generates a PDF with the
      specified settings (pagination, page size, etc.).
      
      :param html: The HTML content to convert to PDF
      :type html: str
      :return: PDF data as bytes
      :rtype: bytes
      :raises RuntimeError: If Playwright is not installed or Chromium is not found
```

## Module-Level Attributes

```{eval-rst}
.. data:: __version__
   :type: str
   :value: "0.1.0"
   
   The version of the jupyter_export_html_style package.
```

## Usage Examples

### Using StylePreprocessor Standalone

```python
from jupyter_export_html_style import StylePreprocessor
from nbformat import read

# Load a notebook
with open('notebook.ipynb', 'r') as f:
    nb = read(f, as_version=4)

# Create and configure preprocessor
preprocessor = StylePreprocessor()
preprocessor.style_metadata_key = "custom_style"

# Process the notebook
processed_nb, resources = preprocessor.preprocess(nb, {})
```

### Using StyledHTMLExporter

```python
from jupyter_export_html_style import StyledHTMLExporter

# Create exporter
exporter = StyledHTMLExporter()
exporter.template_name = "classic"

# Export notebook
(body, resources) = exporter.from_filename('notebook.ipynb')

# Save to file
with open('output.html', 'w') as f:
    f.write(body)
```

### Creating Notebooks with Input/Output Styles

```python
from jupyter_export_html_style import StyledHTMLExporter
from nbformat.v4 import new_code_cell, new_notebook
import nbformat

# Create cells with input and output styles
cells = []

cell1 = new_code_cell("x = 42\nprint(x)")
cell1.metadata['input-style'] = {
    'background-color': '#f5f5f5',
    'border-left': '4px solid #2196f3'
}
cell1.metadata['output-style'] = {
    'background-color': '#e8f5e9',
    'font-family': 'monospace'
}
cells.append(cell1)

# Create notebook
nb = new_notebook(cells=cells)

# Add notebook-level styles
nb.metadata['style'] = """
body {
    font-family: 'Segoe UI', sans-serif;
    max-width: 1200px;
}
"""
nb.metadata['stylesheet'] = 'https://fonts.googleapis.com/css2?family=Segoe+UI'

# Export
exporter = StyledHTMLExporter()
output, resources = exporter.from_notebook_node(nb)

# Save
with open('styled_output.html', 'w') as f:
    f.write(output)
```

### Processing Cell-Level Styles

```python
from jupyter_export_html_style import StylePreprocessor
import nbformat
from nbformat.v4 import new_code_cell, new_notebook

# Create a notebook with various style types
cell1 = new_code_cell("# Cell with all style types")
cell1.metadata['style'] = {'margin': '20px'}
cell1.metadata['input-style'] = {'color': 'blue'}
cell1.metadata['output-style'] = {'border': '1px solid green'}

nb = new_notebook(cells=[cell1])

# Process with preprocessor
preprocessor = StylePreprocessor()
processed_nb, resources = preprocessor.preprocess(nb, {})

# Check collected styles
print(f"Collected styles: {resources['styles']}")
# Output: {'cell-0': {'margin': '20px'}, 
#          'cell-0-input': {'color': 'blue'},
#          'cell-0-output': {'border': '1px solid green'}}
```

### Configuration via Traitlets

```python
from jupyter_export_html_style import StyledHTMLExporter
from traitlets.config import Config

# Create configuration
config = Config()
config.StylePreprocessor.style_metadata_key = "cell_style"
config.StyledHTMLExporter.template_name = "lab"

# Create exporter with config
exporter = StyledHTMLExporter(config=config)
```

### Using StyledWebPDFExporter

```python
from jupyter_export_html_style import StyledWebPDFExporter

# Create exporter with default settings
exporter = StyledWebPDFExporter()

# Export notebook to PDF
(pdf_data, resources) = exporter.from_filename('notebook.ipynb')

# Save to file
with open('output.pdf', 'wb') as f:
    f.write(pdf_data)
```

### PDF Export with Custom Options

```python
from jupyter_export_html_style import StyledWebPDFExporter

# Create exporter with custom settings
exporter = StyledWebPDFExporter(
    paginate=False,  # Single long page
    allow_chromium_download=True,  # Auto-download Chromium if needed
    disable_sandbox=False  # Keep sandbox enabled (default)
)

# Export notebook to PDF
(pdf_data, resources) = exporter.from_filename('styled_notebook.ipynb')

# Save to file
with open('styled_output.pdf', 'wb') as f:
    f.write(pdf_data)
```

### PDF Export in Container Environments

```python
from jupyter_export_html_style import StyledWebPDFExporter

# For Docker/Kubernetes, disable sandbox
exporter = StyledWebPDFExporter(
    disable_sandbox=True  # Required in most containers
)

# Export notebook to PDF
(pdf_data, resources) = exporter.from_filename('notebook.ipynb')

# Save to file
with open('output.pdf', 'wb') as f:
    f.write(pdf_data)
```

## Entry Points

The package registers the following nbconvert entry points:

### Preprocessors

- `style`: Points to `jupyter_export_html_style.preprocessor:StylePreprocessor`

### Exporters

- `styled_html`: Points to `jupyter_export_html_style.exporters.html:StyledHTMLExporter`
- `styled_webpdf`: Points to `jupyter_export_html_style.exporters.webpdf:StyledWebPDFExporter`
- `styled_slides`: Points to `jupyter_export_html_style.exporters.slides:StyledSlidesExporter`

These can be used directly with nbconvert command line:

```bash
# Export to styled HTML
jupyter nbconvert --to styled_html notebook.ipynb

# Export to styled PDF
jupyter nbconvert --to styled_webpdf notebook.ipynb
```

## See Also

- [nbconvert Documentation](https://nbconvert.readthedocs.io/)
- [Traitlets Configuration](https://traitlets.readthedocs.io/en/stable/config.html)
- [JupyterLab Extensions](https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html)
