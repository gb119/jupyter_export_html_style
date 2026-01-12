# Jupyter Export HTML Style

[![Build Status](https://github.com/gb119/jupyter_export_html_style/workflows/Build%20and%20Test/badge.svg)](https://github.com/gb119/jupyter_export_html_style/actions)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://gb119.github.io/jupyter_export_html_style/)
[![PyPI version](https://badge.fury.io/py/jupyter-export-html-style.svg)](https://pypi.org/project/jupyter-export-html-style/)
[![Conda Version](https://img.shields.io/conda/vn/phygbu/jupyter-export-html-style.svg)](https://anaconda.org/phygbu/jupyter-export-html-style)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A JupyterLab extension and nbconvert preprocessor/exporter that allows custom cell-level styling when exporting notebooks to HTML.

## Features

- 🎨 **Custom Cell Styling**: Apply CSS styles to individual cells via metadata
- 🎯 **Input/Output Styling**: Separate styles for cell inputs and outputs
- 📝 **Notebook-Level Styling**: Add custom styles and stylesheets to the entire notebook
- 🔧 **nbconvert Integration**: Seamlessly integrates with nbconvert's export pipeline
- 🚀 **Easy to Use**: Simple metadata-based configuration
- 📦 **Multiple Distribution Channels**: Available via pip and conda
- 🔌 **Extensible**: Built on nbconvert's preprocessor architecture

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

### Notebook-Level Styling

Add custom styles and stylesheets that apply to the entire notebook. Add these to the notebook metadata (not cell metadata):

#### Custom Inline Styles

```json
{
  "metadata": {
    "style": ".jp-Cell { box-shadow: 0 2px 4px rgba(0,0,0,0.1); } body { font-family: Arial, sans-serif; }"
  }
}
```

#### External Stylesheets

Single stylesheet:
```json
{
  "metadata": {
    "stylesheet": "https://example.com/custom-theme.css"
  }
}
```

Multiple stylesheets:
```json
{
  "metadata": {
    "stylesheet": [
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
    "stylesheet": ["https://fonts.googleapis.com/css2?family=Inter&display=swap"]
  }
}
```

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
│   └── exporter.py              # Custom HTML exporter
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
