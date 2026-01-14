# Jupyter Export HTML Style

[![Test](https://github.com/gb119/jupyter_export_html_style/actions/workflows/test.yml/badge.svg)](https://github.com/gb119/jupyter_export_html_style/actions/workflows/test.yml)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://gb119.github.io/jupyter_export_html_style/)
[![PyPI version](https://badge.fury.io/py/jupyter-export-html-style.svg)](https://pypi.org/project/jupyter-export-html-style/)
[![Conda Version](https://img.shields.io/conda/vn/phygbu/jupyter-export-html-style.svg)](https://anaconda.org/phygbu/jupyter-export-html-style)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/1132382644.svg)](https://doi.org/10.5281/zenodo.18231801)

A JupyterLab extension and nbconvert preprocessor/exporter that allows custom cell-level styling when exporting notebooks to HTML, Slides and PDF.

This extension was written to help with using Jupyterlab for authoring teaching materials. The motivation was dealing with cases where you need to have
some initialisation code (for example to apply custom css to the notebook's IPython rendering) but do not want those code cells to be visible in exported
slides, html or pdf versions. With this extension you can tweak the css in the exported notebook from within the notebook environment. Similarly, it embeds
images and local stylesheets into the exported html so that they can be pasted directly into virtual learning environments. The Blackboard Ultra VLE in 
particular does not like internal anchor links in its html, so there is a notebook level control of whether these should be excluded.

## Features

- 🎨 **Custom Cell Styling**: Apply CSS styles to individual cells via metadata
- 🎯 **Input/Output Styling**: Separate styles for cell inputs and outputs
- 🏷️ **Custom CSS Classes**: Add custom CSS classes to cells, inputs, and outputs for use with external stylesheets
- 📝 **Notebook-Level Styling**: Add custom styles and stylesheets to the entire notebook
- 📦 **Resource Embedding**: Automatically embeds local CSS files as inline styles for self-contained HTML
- 🖼️ **Image Embedding**: Embeds images as base64 data URIs for self-contained HTML exports
- 🔧 **nbconvert Integration**: Seamlessly integrates with nbconvert's export pipeline
- 📄 **PDF Export with Styles**: Export to PDF via HTML with all custom styles applied
- 🎭 **Reveal.js Slides with Styles**: Create presentation slides with custom cell styling
- 🚀 **Easy to Use**: Simple metadata-based configuration


## Installation

### Using pip

```bash
pip install jupyter-export-html-style
```

### Using conda

```bash
conda install -c phygbu jupyter-export-html-style
```

### From source

```bash
git clone https://github.com/gb119/jupyter_export_html_style.git
cd jupyter_export_html_style
pip install -e .
```

## Quick Start

### 1. Add Style Metadata to Cells

In your Jupyter notebook, add style metadata to cells:

```json
{
  "metadata": {
    "style": {
      "background-color": "#f0f0f0",
      "border": "2px solid #333",
      "padding": "10px"
    }
  }
}
```

### 2. Export with Custom Styles

#### HTML Export

From the command line:

```bash
jupyter nbconvert --to styled_html notebook.ipynb
```

Or using Python:

```python
from jupyter_export_html_style import StyledHTMLExporter

exporter = StyledHTMLExporter()
(body, resources) = exporter.from_filename('notebook.ipynb')
```

#### PDF Export (with Styles)

Export to PDF via HTML with all custom styles applied:

From the command line:

```bash
jupyter nbconvert --to styled_webpdf notebook.ipynb
```

Or using Python:

```python
from jupyter_export_html_style import StyledWebPDFExporter

exporter = StyledWebPDFExporter()
(body, resources) = exporter.from_filename('notebook.ipynb')
```

**Note**: PDF export requires [Playwright](https://playwright.dev/) to be installed:

```bash
pip install nbconvert[webpdf]
playwright install chromium
```

#### Reveal.js Slides Export (with Styles)

Export to Reveal.js presentation slides with all custom styles applied:

From the command line:

```bash
jupyter nbconvert --to styled_slides notebook.ipynb
```

Or using Python:

```python
from jupyter_export_html_style import StyledSlidesExporter

exporter = StyledSlidesExporter()
(body, resources) = exporter.from_filename('notebook.ipynb')
```

**Note**: For slides to work properly, cells should have slideshow metadata. In JupyterLab, use **View → Activate Presentation Mode** to set slide types for cells.

You can also customize the Reveal.js theme and other options:

```python
exporter = StyledSlidesExporter(
    reveal_theme='moon',
    reveal_transition='fade',
    reveal_number='c/t'
)
```

#### JupyterLab Integration

In JupyterLab, the exporters are available in the **File → Save and Export Notebook As...** menu with user-friendly names:

- **HTML (with styles)** - Export to HTML with custom cell and notebook styles
- **PDF via HTML (with styles)** - Export to PDF via HTML with custom styles applied
- **Reveal.js slides (with styles)** - Export to Reveal.js presentation slides with custom styles

These menu entries correspond to the `styled_html`, `styled_webpdf`, and `styled_slides` exporters used in the command line examples above.

## Visual Examples

Want to see what the styling looks like? Check out our [Visual Examples Gallery](https://gb119.github.io/jupyter_export_html_style/usage.html#visual-examples-gallery) in the documentation, which includes screenshots and live examples of:

- 🎨 **Cell-level styling** with highlights, borders, and gradients
- 📥📤 **Input/output styling** with separate colors and themes
- 🏷️ **Custom CSS classes** using external stylesheets
- 📝 **Notebook-level styling** for consistent, professional documents
- ✨ **Comprehensive demos** combining multiple techniques

All example notebooks and their exported HTML files are available in the [examples directory](docs/source/examples/).

## Usage Examples

### Cell-Level Styling

#### Highlighting Important Cells

```json
{
  "style": {
    "background-color": "#fff9c4",
    "border": "2px dashed #fbc02d"
  }
}
```

#### Error/Warning Styling

```json
{
  "style": {
    "background-color": "#ffebee",
    "border-left": "5px solid #f44336"
  }
}
```

#### Custom CSS Strings

```json
{
  "style": "background: linear-gradient(to right, #667eea 0%, #764ba2 100%); color: white; padding: 15px;"
}
```

### Input and Output Styling

Style the input and output areas of cells separately:

#### Input Styling

```json
{
  "input-style": {
    "background-color": "#f5f5f5",
    "border-left": "4px solid #2196f3",
    "padding": "10px"
  }
}
```

#### Output Styling

```json
{
  "output-style": {
    "background-color": "#e8f5e9",
    "border": "1px solid #4caf50",
    "font-family": "monospace"
  }
}
```

#### Combined Cell, Input, and Output Styles

```json
{
  "style": {
    "margin": "20px 0",
    "border-radius": "8px"
  },
  "input-style": {
    "background-color": "#fce4ec",
    "color": "#880e4f"
  },
  "output-style": {
    "background-color": "#e8f5e9",
    "font-family": "monospace"
  }
}
```

### Custom CSS Classes

Apply custom CSS classes to cells and their components using the `class`, `input-class`, and `output-class` metadata. These classes are added to the HTML elements alongside the standard JupyterLab classes, allowing you to use external stylesheets or define custom styles in the notebook-level metadata.

#### Cell-Level Classes

Add custom CSS classes to an entire cell:

```json
{
  "class": "highlight-important warning-cell"
}
```

This adds the specified classes to the cell's `<div>` element, e.g.:
```html
<div class="jp-Cell jp-CodeCell jp-Notebook-cell highlight-important warning-cell">
```

#### Input and Output Classes

Add custom classes to input and output areas separately:

```json
{
  "input-class": "code-highlight",
  "output-class": "result-highlight"
}
```

#### Combined Classes and Styles

You can use both custom classes and inline styles together:

```json
{
  "class": "important-cell",
  "style": {
    "margin": "20px 0"
  },
  "input-class": "code-section",
  "input-style": {
    "border-left": "4px solid #2196f3"
  }
}
```

#### Using Custom Classes with External Stylesheets

Define your styles in a CSS file and reference them in the notebook metadata:

**custom-styles.css:**
```css
.highlight-important {
  background-color: #fff9c4;
  border: 2px solid #fbc02d;
}

.code-highlight {
  background-color: #f5f5f5;
  font-size: 1.1em;
}

.result-highlight {
  background-color: #e8f5e9;
  border-left: 4px solid #4caf50;
}
```

**Notebook metadata:**
```json
{
  "metadata": {
    "stylesheet": "custom-styles.css"
  }
}
```

**Cell metadata:**
```json
{
  "class": "highlight-important",
  "input-class": "code-highlight",
  "output-class": "result-highlight"
}
```

### Notebook-Level Styling

Add custom styles and stylesheets that apply to the entire notebook. Add these to the notebook metadata (not cell metadata):

> **Note:** Local or relative CSS file paths will be automatically embedded as inline styles in the exported HTML, creating self-contained files. Remote URLs (http:// or https://) will remain as external `<link>` tags.

#### Custom Inline Styles

```json
{
  "metadata": {
    "style": ".jp-Cell { box-shadow: 0 2px 4px rgba(0,0,0,0.1); } body { font-family: Arial, sans-serif; }"
  }
}
```

#### External Stylesheets

Single stylesheet (local file):
```json
{
  "metadata": {
    "stylesheet": "custom-theme.css"
  }
}
```

Single stylesheet (remote URL):
```json
{
  "metadata": {
    "stylesheet": "https://example.com/custom-theme.css"
  }
}
```

Multiple stylesheets (mixed local and remote):
```json
{
  "metadata": {
    "stylesheet": [
      "local-styles.css",
      "https://fonts.googleapis.com/css2?family=Roboto&display=swap",
      "https://example.com/custom-theme.css"
    ]
  }
}
```

#### Combined Notebook Styles

```json
{
  "metadata": {
    "style": "body { max-width: 1200px; margin: 0 auto; }",
    "stylesheet": ["local-theme.css", "https://fonts.googleapis.com/css2?family=Inter&display=swap"]
  }
}
```

#### Controlling Header Anchor Links

By default, the HTML exporter adds anchor links (¶) to headings in markdown cells, allowing users to link directly to specific sections. You can control this behavior using the `anchors` metadata field:

Disable anchor links:
```json
{
  "metadata": {
    "anchors": false
  }
}
```

Explicitly enable anchor links (this is the default):
```json
{
  "metadata": {
    "anchors": true
  }
}
```

**Note:** When anchor links are disabled, headings will not include the clickable ¶ symbol or the ID attribute, making them cleaner but non-linkable.

### Reveal.js Slides Styling

When exporting to Reveal.js slides, all the same styling options work:

#### Styling Individual Slides

```json
{
  "metadata": {
    "slideshow": {
      "slide_type": "slide"
    },
    "style": {
      "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      "color": "white"
    }
  }
}
```

#### Styling Slide Content

You can style the input and output areas of code cells in slides:

```json
{
  "metadata": {
    "slideshow": {
      "slide_type": "slide"
    },
    "input-style": {
      "font-size": "1.2em",
      "background-color": "#2d2d2d"
    },
    "output-style": {
      "border-left": "4px solid #4CAF50"
    }
  }
}
```

#### Customizing Reveal.js Options

You can customize the Reveal.js presentation settings:

From the command line:
```bash
jupyter nbconvert --to styled_slides notebook.ipynb \
  --SlidesExporter.reveal_theme=moon \
  --SlidesExporter.reveal_transition=fade \
  --SlidesExporter.reveal_scroll=true
```

Or in Python:
```python
from jupyter_export_html_style import StyledSlidesExporter

exporter = StyledSlidesExporter(
    reveal_theme='moon',
    reveal_transition='fade',
    reveal_scroll=True,
    reveal_number='c/t'
)
output, resources = exporter.from_filename('notebook.ipynb')
```

Available reveal.js themes include: `black`, `white`, `league`, `beige`, `sky`, `night`, `serif`, `simple`, `solarized`, `blood`, `moon`.

Available transitions include: `none`, `fade`, `slide`, `convex`, `concave`, `zoom`.

## Building from Source

### Building Python Wheels

```bash
pip install build
python -m build
```

The wheel and source distribution will be created in the `dist/` directory.

### Building Conda Packages

```bash
conda install conda-build
conda build conda.recipe
```

The conda package will be built in your conda-bld directory.

## Documentation

Full documentation is available at [https://gb119.github.io/jupyter_export_html_style/](https://gb119.github.io/jupyter_export_html_style/)

- [Installation Guide](docs/source/installation.md)
- [Usage Guide](docs/source/usage.md)
- [API Reference](docs/source/api.md)
- [Contributing](docs/source/contributing.md)

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/gb119/jupyter_export_html_style.git
cd jupyter_export_html_style

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev,docs]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black jupyter_export_html_style

# Lint code
ruff check jupyter_export_html_style

# Type check
mypy jupyter_export_html_style
```

## Project Structure

```
jupyter_export_html_style/
├── jupyter_export_html_style/    # Main Python package
│   ├── __init__.py              # Package initialization
│   ├── preprocessor.py          # nbconvert preprocessor
│   ├── exporters/               # Exporters sub-package
│   │   ├── __init__.py          # Exporters package initialization
│   │   ├── html.py              # Custom HTML exporter
│   │   ├── slides.py            # Reveal.js slides exporter
│   │   └── webpdf.py            # WebPDF exporter
│   └── templates/               # Jinja2 templates for exporters
│       ├── styled/              # HTML exporter templates
│       ├── styled_reveal/       # Slides exporter templates
│       └── webpdf/              # WebPDF exporter templates
├── tests/                       # Test suite
│   ├── test_exporter.py
│   ├── test_slides_exporter.py
│   ├── test_webpdf_exporter.py
│   ├── test_preprocessor.py
│   └── test_integration.py
├── docs/                        # Documentation
│   ├── source/                  # Sphinx documentation source
│   │   ├── index.md
│   │   ├── installation.md
│   │   ├── usage.md
│   │   ├── api.md
│   │   └── contributing.md
│   ├── Makefile                # Documentation build (Unix)
│   └── make.bat                # Documentation build (Windows)
├── conda.recipe/               # Conda build recipe
│   └── meta.yaml              # Conda package metadata
├── .github/                   # GitHub configuration
│   └── workflows/            # CI/CD workflows
│       ├── build.yml         # Build and test workflow
│       └── docs.yml          # Documentation build workflow
├── pyproject.toml            # Project metadata and build configuration
├── README.md                 # This file
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore patterns
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/source/contributing.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of [nbconvert](https://github.com/jupyter/nbconvert)
- Designed for use with [JupyterLab](https://github.com/jupyterlab/jupyterlab)

## Support

- **Issues**: [GitHub Issues](https://github.com/gb119/jupyter_export_html_style/issues)
- **Discussions**: [GitHub Discussions](https://github.com/gb119/jupyter_export_html_style/discussions)
- **Documentation**: [GitHub Pages](https://gb119.github.io/jupyter_export_html_style/)

## Citation

If you use this project in your research, please cite:

```bibtex
@software{jupyter_export_html_style,
  author = {Burnell, Gavin},
  title = {Jupyter Export HTML Style},
  year = {2026},
  url = {https://github.com/gb119/jupyter_export_html_style}
}
```
