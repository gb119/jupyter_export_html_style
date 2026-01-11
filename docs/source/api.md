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
      
      :param nb: The notebook to preprocess
      :type nb: NotebookNode
      :param resources: Additional resources used in the conversion process
      :type resources: dict
      :return: Tuple of processed notebook and updated resources
      :rtype: tuple(NotebookNode, dict)

   .. method:: preprocess_cell(cell, resources, index)
   
      Preprocess a single cell.
      
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

   An HTML exporter that supports cell-level style customization.
   
   This exporter extends the standard nbconvert HTMLExporter to include
   custom styles defined in cell metadata. It automatically registers
   the StylePreprocessor and injects collected styles into the output HTML.

   .. attribute:: template_name
      :type: str
      :value: "classic"
      
      Name of the template to use for HTML generation. Default is "classic".

   .. method:: from_notebook_node(nb, resources=None, **kw)
   
      Convert a notebook node to HTML with style support.
      
      :param nb: The notebook to convert
      :type nb: NotebookNode
      :param resources: Additional resources used in the conversion process
      :type resources: dict, optional
      :param kw: Additional keyword arguments
      :type kw: dict
      :return: Tuple of HTML output and updated resources
      :rtype: tuple(str, dict)
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

## Entry Points

The package registers the following nbconvert entry points:

### Preprocessors

- `style`: Points to `jupyter_export_html_style.preprocessor:StylePreprocessor`

### Exporters

- `styled_html`: Points to `jupyter_export_html_style.exporter:StyledHTMLExporter`

These can be used directly with nbconvert command line:

```bash
jupyter nbconvert --to styled_html notebook.ipynb
```

## See Also

- [nbconvert Documentation](https://nbconvert.readthedocs.io/)
- [Traitlets Configuration](https://traitlets.readthedocs.io/en/stable/config.html)
- [JupyterLab Extensions](https://jupyterlab.readthedocs.io/en/stable/extension/extension_dev.html)
