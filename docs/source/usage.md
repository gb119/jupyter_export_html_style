# Usage Guide

## Basic Usage

### Adding Style Metadata to Cells

In Jupyter notebooks, you can add style metadata to cells in several ways:

#### Via Notebook Interface

1. Select a cell
2. Open the cell metadata editor (View → Cell Toolbar → Edit Metadata)
3. Add the style metadata:

```json
{
  "style": {
    "background-color": "#f0f0f0",
    "border": "2px solid #333",
    "padding": "10px"
  }
}
```

#### Programmatically

```python
from IPython.display import Javascript, display

# Set style for current cell
display(Javascript('''
    var cell = Jupyter.notebook.get_selected_cell();
    cell.metadata.style = {
        "background-color": "#e8f4f8",
        "border-left": "5px solid #2196F3"
    };
'''))
```

## Exporting with Custom Styles

### Command Line

Use the `styled_html` exporter with nbconvert:

```bash
jupyter nbconvert --to styled_html notebook.ipynb
```

With custom configuration:

```bash
jupyter nbconvert --to styled_html \
    --StylePreprocessor.style_metadata_key="custom_style" \
    notebook.ipynb
```

### Python API

```python
from jupyter_export_html_style import StyledHTMLExporter
from nbconvert.preprocessors import Preprocessor

# Create exporter
exporter = StyledHTMLExporter()

# Export notebook
with open('notebook.ipynb', 'r') as f:
    notebook_content = f.read()

(body, resources) = exporter.from_filename('notebook.ipynb')

# Save output
with open('output.html', 'w') as f:
    f.write(body)
```

## Configuration

### nbconvert Configuration

Create a `nbconvert_config.py` file:

```python
# Configure the StylePreprocessor
c.StylePreprocessor.style_metadata_key = "style"
c.StylePreprocessor.enabled = True

# Configure the StyledHTMLExporter
c.StyledHTMLExporter.template_name = "classic"
```

### Advanced Styling

#### CSS String Format

You can also use CSS strings directly:

```json
{
  "style": "background-color: #fff3cd; border: 1px solid #ffc107; padding: 15px;"
}
```

#### Conditional Styles

Apply different styles based on cell type:

```python
# In a code cell
def apply_style_if_error(cell):
    if cell.get('outputs') and any('error' in str(output) for output in cell['outputs']):
        cell['metadata']['style'] = {
            'background-color': '#ffebee',
            'border-left': '4px solid #f44336'
        }
```

## Integration with JupyterLab

When the JupyterLab extension is installed, you can:

1. Use the Export menu with "Styled HTML" option
2. Configure default styles in JupyterLab settings
3. Preview styled exports before saving

## Examples

### Example 1: Highlight Important Cells

```json
{
  "style": {
    "background-color": "#fff9c4",
    "border": "2px dashed #fbc02d",
    "padding": "12px",
    "margin": "8px 0"
  }
}
```

### Example 2: Error/Warning Styling

```json
{
  "style": {
    "background-color": "#ffebee",
    "border-left": "5px solid #f44336",
    "padding": "10px"
  }
}
```

### Example 3: Success/Info Styling

```json
{
  "style": {
    "background-color": "#e8f5e9",
    "border-left": "5px solid #4caf50",
    "padding": "10px"
  }
}
```

## Troubleshooting

### Styles Not Applied

1. Verify metadata is correctly formatted JSON
2. Check that the exporter is using `styled_html`
3. Ensure the preprocessor is enabled

### CSS Conflicts

If styles don't appear as expected:

1. Use more specific CSS selectors
2. Add `!important` to style values
3. Check browser developer tools for conflicts

## Next Steps

- See the [API Reference](api.md) for detailed class documentation
- Check out [examples on GitHub](https://github.com/gb119/jupyter_export_html_style/tree/main/examples)
