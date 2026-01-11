# Contributing

Thank you for considering contributing to Jupyter Export HTML Style!

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- pip or conda

### Setting Up Development Environment

1. Fork the repository on GitHub

2. Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/jupyter_export_html_style.git
cd jupyter_export_html_style
```

3. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install in development mode:

```bash
pip install -e ".[dev,docs]"
```

## Development Workflow

### Running Tests

Run the test suite:

```bash
pytest
```

With coverage:

```bash
pytest --cov=jupyter_export_html_style --cov-report=html
```

### Code Style

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Format code:

```bash
black jupyter_export_html_style tests
```

Lint code:

```bash
ruff check jupyter_export_html_style tests
```

Type check:

```bash
mypy jupyter_export_html_style
```

### Building Documentation

Build the documentation locally:

```bash
cd docs
make html
```

View the documentation:

```bash
python -m http.server -d docs/_build/html
```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-exporter`
- `fix/style-preprocessing-bug`
- `docs/improve-installation-guide`

### Commit Messages

Follow these guidelines:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

### Pull Request Process

1. Update documentation for any changed functionality
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md with your changes
5. Submit a pull request with a clear description

## Testing Guidelines

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names: `test_style_preprocessor_extracts_metadata()`
- Test both success and failure cases
- Use fixtures for common test setup

Example test structure:

```python
import pytest
from jupyter_export_html_style import StylePreprocessor

def test_style_preprocessor_basic():
    """Test basic style preprocessing."""
    preprocessor = StylePreprocessor()
    # Test implementation
    assert True

def test_style_preprocessor_with_custom_key():
    """Test preprocessor with custom metadata key."""
    preprocessor = StylePreprocessor()
    preprocessor.style_metadata_key = "custom_style"
    # Test implementation
    assert True
```

## Building and Packaging

### Building Python Wheels

```bash
pip install build
python -m build
```

### Building Conda Packages

```bash
conda install conda-build
conda build conda.recipe
```

### Publishing

Maintainers can publish packages to PyPI and Anaconda Cloud.

#### Publishing to PyPI

```bash
pip install twine
# Using token authentication (recommended)
python -m twine upload --username __token__ --password $PYPI_TOKEN dist/*
```

Set the `PYPI_TOKEN` environment variable or GitHub secret with your PyPI API token.

#### Publishing to Anaconda Cloud

Modern conda-build (3.18+) creates `.conda` format packages by default, which are more efficient than `.tar.bz2` packages.

```bash
conda install anaconda-client
# Find the built package (supports both .conda and .tar.bz2 formats)
anaconda upload --token $ANACONDA_TOKEN $(conda info --base)/conda-bld/noarch/jupyter-export-html-style-*.conda
# Or if using older format:
anaconda upload --token $ANACONDA_TOKEN $(conda info --base)/conda-bld/noarch/jupyter-export-html-style-*.tar.bz2
```

Set the `ANACONDA_TOKEN` environment variable or GitHub secret with your Anaconda Cloud API token.

#### Required GitHub Secrets for CI/CD

If setting up automated publishing in GitHub Actions, configure these secrets in your repository settings:

- `ANACONDA_TOKEN`: API token from Anaconda Cloud for uploading conda packages
- `PYPI_TOKEN`: API token from PyPI for uploading Python packages

## Documentation Guidelines

- Use Markdown for documentation files
- Include code examples
- Keep explanations clear and concise
- Add links to related resources
- Update API documentation for code changes

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Reporting Issues

Report unacceptable behavior to the project maintainers.

## Getting Help

- **Documentation**: Check the docs first
- **Issues**: Search existing issues
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for sensitive matters

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
