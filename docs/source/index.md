# Jupyter Export HTML Style

Welcome to the documentation for Jupyter Export HTML Style!

## Overview

Jupyter Export HTML Style is a JupyterLab extension and nbconvert preprocessor/exporter that enables custom cell-level styling when exporting notebooks to HTML. This allows you to override default styles using cell metadata.

## Features

- **Custom Cell Styling**: Apply custom CSS styles to individual cells via metadata
- **nbconvert Integration**: Works seamlessly with nbconvert's export pipeline
- **JupyterLab Extension**: Integrated into JupyterLab for easy access
- **Flexible Configuration**: Configure style metadata keys and behavior

## Contents

```{toctree}
:maxdepth: 2

installation
usage
api
contributing
```

## Quick Start

### Installation

Install via pip:

```bash
pip install jupyter-export-html-style
```

Or via conda:

```bash
conda install -c conda-forge jupyter-export-html-style
```

### Basic Usage

Add style metadata to a notebook cell:

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

Export with the custom exporter:

```bash
jupyter nbconvert --to styled_html notebook.ipynb
```

## Links

- [GitHub Repository](https://github.com/gb119/jupyter_export_html_style)
- [Issue Tracker](https://github.com/gb119/jupyter_export_html_style/issues)
- [PyPI Package](https://pypi.org/project/jupyter-export-html-style/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
