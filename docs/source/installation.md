# Installation

## Requirements

- Python 3.11 or higher
- JupyterLab 4.0 or higher (for JupyterLab extension features)
- nbconvert 6.0 or higher

## Installation Methods

### Using pip

The easiest way to install is via pip:

```bash
pip install jupyter-export-html-style
```

For development installation:

```bash
pip install jupyter-export-html-style[dev]
```

To include JupyterLab integration:

```bash
pip install jupyter-export-html-style[jupyterlab]
```

### Using conda

Install from phygbu:

```bash
conda install -c phygbu jupyter-export-html-style
```

### From Source

To install from source:

```bash
git clone https://github.com/gb119/jupyter_export_html_style.git
cd jupyter_export_html_style
pip install -e .
```

For development:

```bash
pip install -e ".[dev,docs]"
```

## Verification

Verify the installation:

```bash
python -c "import jupyter_export_html_style; print(jupyter_export_html_style.__version__)"
```

Check that the nbconvert extensions are registered:

```bash
jupyter nbconvert --help-all | grep -A 5 "styled_html"
```

## Building from Source

### Building Python Wheels

To build a wheel distribution:

```bash
pip install build
python -m build
```

This creates distributions in the `dist/` directory.

### Building Conda Packages

To build a conda package:

```bash
conda install conda-build
conda build conda.recipe
```

The package will be built in your conda-bld directory.

## Next Steps

After installation, see the [Usage](usage.md) guide to learn how to use the package.
