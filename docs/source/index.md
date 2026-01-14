# Jupyter Export HTML Style

Welcome to the documentation for Jupyter Export HTML Style!

## Overview

A JupyterLab extension and nbconvert preprocessor/exporter that allows custom cell-level styling when exporting notebooks to HTML, Slides and PDF.

This extension was written to help with using Jupyterlab for authoring teaching materials. The motivation was dealing with cases where you need to have some initialisation code (for example to apply custom css to the notebook's IPython rendering) but do not want those code cells to be visible in exported slides, html or pdf versions. With this extension you can tweak the css in the exported notebook from within the notebook environment. Similarly, it embeds images and local stylesheets into the exported html so that they can be pasted directly into virtual learning environments. The Blackboard Ultra VLE in particular does not like internal anchor links in its html, so there is a notebook level control of whether these should be excluded.

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
conda install -c phygbu jupyter-export-html-style
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
