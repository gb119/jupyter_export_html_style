# Known Issues

## CSS Styles Not Applied to HTML Elements

### Summary
The `StyledHTMLExporter` generates CSS rules (e.g., `#cell-0`, `#cell-0-input`, `#cell-0-output`) and successfully injects them into the HTML `<head>` section. However, these styles have **no visible effect** because the HTML elements in the output do not have the corresponding `id` attributes.

### Root Cause
The exporter does not override nbconvert's cell templates. The default nbconvert templates generate HTML cells without the custom `id` attributes that the CSS selectors target.

### Evidence
When exporting a notebook with cell styles:
```python
cell.metadata["style"] = {"background-color": "#f0f0f0"}
```

The exporter generates CSS in the `<head>`:
```html
<style>
/* Custom cell styles */
#cell-0 { background-color: #f0f0f0 }
</style>
```

But the HTML body contains elements like:
```html
<div id="cell-id=de5d2dbd">
  <!-- No id="cell-0" anywhere -->
</div>
```

The generated CSS selectors (`#cell-0`) don't match any elements in the DOM, so styles are not applied.

### How to Fix
To make the styles functional, the exporter needs to:

1. **Create Custom Jinja2 Templates**: Override nbconvert's cell templates to add the appropriate `id` attributes
   - Location for templates: Create a `templates/` directory in the package
   - Base template on nbconvert's existing templates (classic or lab)
   - Modify cell rendering to include: `id="cell-{{ cell_index }}"`
   - Modify input area to include: `id="cell-{{ cell_index }}-input"`
   - Modify output area to include: `id="cell-{{ cell_index }}-output"`

2. **Register Custom Template Path**: In `StyledHTMLExporter.__init__()`:
   ```python
   # Add custom template directory to the search path
   import os
   template_path = os.path.join(os.path.dirname(__file__), 'templates')
   self.extra_template_basedirs = [template_path]
   ```

3. **Template Hierarchy**: The custom template should:
   - Extend the base nbconvert template (e.g., `classic/index.html.j2`)
   - Override only the cell block to inject the custom IDs
   - Preserve all other nbconvert functionality

### Files to Modify
- Create `jupyter_export_html_style/templates/styled/index.html.j2`
- Create `jupyter_export_html_style/templates/styled/cell.html.j2` or override cell blocks
- Modify `jupyter_export_html_style/exporter.py` to:
  - Set `template_name` to the custom template
  - Configure `extra_template_basedirs` to include the package's template directory

### Testing Strategy
After implementing the fix:
1. Export a notebook with styles
2. Parse the HTML with BeautifulSoup
3. Verify elements exist with IDs: `#cell-0`, `#cell-0-input`, `#cell-0-output`
4. Verify the CSS selectors match the actual element IDs
5. Optionally: Render in a browser and verify styles are visually applied

### Related Files
- `jupyter_export_html_style/exporter.py` - Main exporter class
- `jupyter_export_html_style/preprocessor.py` - Processes cell metadata
- `tests/test_exporter.py` - Tests verify CSS generation but not application

### References
- nbconvert template documentation: https://nbconvert.readthedocs.io/en/latest/customizing.html
- nbconvert templates source: https://github.com/jupyter/nbconvert/tree/main/share/templates
- The preprocessor correctly assigns cell indices (0, 1, 2, ...) in `preprocess_cell()`
