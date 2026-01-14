# Visual Examples

This directory contains example notebooks demonstrating the various styling capabilities of `jupyter-export-html-style`.

## Example Files

### 1. Cell-Level Styling (`cell_styling.ipynb`)

Demonstrates various cell-level styling options:
- Yellow highlighted important cells with dashed borders
- Error/warning cells with red left border
- Success cells with green accents
- Gradient backgrounds for section headers
- Box shadows for elevated card-like appearance

**Files:**
- `cell_styling.ipynb` - Source notebook
- `cell_styling.html` - Exported HTML with styles
- `cell_styling.png` - Screenshot of rendered output

### 2. Input and Output Styling (`input_output_styling.ipynb`)

Shows how to style input (code) and output (results) areas independently:
- Blue-accented input areas with custom fonts
- Green-themed output areas with borders
- Combined styling with contrasting input/output colors
- Gradient backgrounds for code sections

**Files:**
- `input_output_styling.ipynb` - Source notebook
- `input_output_styling.html` - Exported HTML with styles
- `input_output_styling.png` - Screenshot of rendered output

### 3. Custom CSS Classes (`custom_classes.ipynb`)

Demonstrates using custom CSS classes with an external stylesheet:
- Custom CSS classes from external stylesheet
- Reusable style definitions
- Dark-themed code highlighting
- Class-based styling combined with inline styles

**Files:**
- `custom_classes.ipynb` - Source notebook
- `custom_classes.html` - Exported HTML with styles
- `custom_classes.png` - Screenshot of rendered output
- `custom-styles.css` - External CSS stylesheet

### 4. Notebook-Level Styling (`notebook_styling.ipynb`)

Shows how to apply global styles affecting the entire notebook:
- Global font and layout settings
- Consistent spacing and shadows on all cells
- Colored left borders to distinguish cell types
- Maximum width for better readability
- Light gray page background

**Files:**
- `notebook_styling.ipynb` - Source notebook
- `notebook_styling.html` - Exported HTML with styles
- `notebook_styling.png` - Screenshot of rendered output

### 5. Comprehensive Demo (`comprehensive_demo.ipynb`)

A complete example combining multiple styling techniques:
- Gradient header with centered text
- Color-coded sections (warnings, info, results)
- Combined cell, input, and output styling
- Box shadows and rounded corners
- Professional color scheme throughout

**Files:**
- `comprehensive_demo.ipynb` - Source notebook
- `comprehensive_demo.html` - Exported HTML with styles
- `comprehensive_demo.png` - Screenshot of rendered output

## Regenerating Examples

To regenerate the example notebooks and exports:

```bash
# Generate notebooks
python generate_examples.py

# Export to HTML
jupyter nbconvert --to styled_html cell_styling.ipynb
jupyter nbconvert --to styled_html input_output_styling.ipynb
jupyter nbconvert --to styled_html custom_classes.ipynb
jupyter nbconvert --to styled_html notebook_styling.ipynb
jupyter nbconvert --to styled_html comprehensive_demo.ipynb

# Take screenshots (requires playwright)
python take_screenshots.py
```

## Using These Examples

You can:
1. Open the `.ipynb` files in Jupyter to see the metadata structure
2. View the `.html` files in a browser to see the rendered output
3. Look at the `.png` screenshots to quickly preview the results
4. Use these as templates for your own styled notebooks

## Tips for Creating Visually Striking Examples

- Use bold, contrasting colors for different cell types
- Add gradients for headers and important sections
- Use box shadows to create depth and visual hierarchy
- Combine multiple styling techniques for a polished look
- Keep color schemes consistent within a notebook
- Use adequate padding and margins for breathing room
