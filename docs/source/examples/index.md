# Visual Examples Gallery

This directory contains example notebooks demonstrating the styling capabilities of `jupyter-export-html-style`.

## Quick Links

- [Cell-Level Styling](#cell-level-styling) - Highlight important cells, errors, and successes
- [Input/Output Styling](#inputoutput-styling) - Style code and results independently
- [Custom CSS Classes](#custom-css-classes) - Use external stylesheets
- [Notebook-Level Styling](#notebook-level-styling) - Apply global styles
- [Comprehensive Demo](#comprehensive-demo) - All features combined

---

## Cell-Level Styling

**File:** `cell_styling.ipynb`

Demonstrates various cell-level styling options including highlighted cells, error/warning styles, success messages, gradient backgrounds, and shadow effects.

![Cell Styling Examples](cell_styling.png)

**Download:** [Notebook](cell_styling.ipynb) | [HTML](cell_styling.html)

---

## Input/Output Styling

**File:** `input_output_styling.ipynb`

Shows how to style input (code) and output (results) areas independently with different colors, fonts, and borders.

![Input Output Styling](input_output_styling.png)

**Download:** [Notebook](input_output_styling.ipynb) | [HTML](input_output_styling.html)

---

## Custom CSS Classes

**File:** `custom_classes.ipynb`

Demonstrates using custom CSS classes with an external stylesheet for reusable, maintainable styling.

![Custom Classes](custom_classes.png)

**Download:** [Notebook](custom_classes.ipynb) | [HTML](custom_classes.html) | [Stylesheet](custom-styles.css)

---

## Notebook-Level Styling

**File:** `notebook_styling.ipynb`

Shows how to apply global styles affecting the entire notebook for a cohesive, professional appearance.

![Notebook Styling](notebook_styling.png)

**Download:** [Notebook](notebook_styling.ipynb) | [HTML](notebook_styling.html)

---

## Comprehensive Demo

**File:** `comprehensive_demo.ipynb`

A complete example combining multiple styling techniques in a single notebook to create a polished, professional document.

![Comprehensive Demo](comprehensive_demo.png)

**Download:** [Notebook](comprehensive_demo.ipynb) | [HTML](comprehensive_demo.html)

---

## Generating Examples

To regenerate these examples:

```bash
# Generate notebooks
python generate_examples.py

# Export to HTML
jupyter nbconvert --to styled_html *.ipynb

# Take screenshots (requires playwright)
python take_screenshots.py
```

## Using These Examples

1. **View the notebooks** (`.ipynb`) in Jupyter to see the metadata structure
2. **Open the HTML files** in a browser to see the rendered output
3. **Look at the screenshots** (`.png`) to quickly preview the results
4. **Use as templates** for your own styled notebooks
