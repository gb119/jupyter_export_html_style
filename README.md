# jupyter_export_html_style

A Jupyter nbconvert exporter that exports notebooks as HTML with support for cell-level style metadata overrides.

## Features

- Inherits from the standard HTML exporter
- Automatically embeds images in the output HTML
- Extracts `style` metadata from notebook cells
- Applies custom styles to cell div elements in the HTML output

## Installation

```bash
pip install -e .
```

## Usage

### Command Line

Export a notebook using the custom exporter:

```bash
jupyter nbconvert --to html_style example_notebook.ipynb
```

### Python API

```python
from jupyter_export_html_style import HTMLStyleExporter

# Create exporter instance
exporter = HTMLStyleExporter()

# Export notebook
(body, resources) = exporter.from_filename('example_notebook.ipynb')

# Save to file
with open('output.html', 'w') as f:
    f.write(body)
```

### Adding Style Metadata to Cells

To add custom styles to a cell, edit the cell metadata in Jupyter and add a `style` key with CSS properties:

```json
{
  "style": "background-color: #e3f2fd; padding: 10px; border-left: 5px solid #2196f3;"
}
```

The styles will be applied as inline CSS to the cell's div element in the exported HTML.

## Example

See `example_notebook.ipynb` for a demonstration of cells with custom styles.

## Components

- **HTMLStyleExporter**: Custom HTML exporter that embeds images and uses style-aware templates
- **StyleMetadataPreprocessor**: Preprocessor that extracts style metadata from cells
- **html_style.html.j2**: Custom Jinja2 template that includes style attributes in cell divs
