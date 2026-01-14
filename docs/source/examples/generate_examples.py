#!/usr/bin/env python3
"""Generate example notebooks demonstrating various styling features.

This script creates notebooks with visually striking examples of the different
styling capabilities of jupyter-export-html-style.
"""

import nbformat as nbf
from pathlib import Path

# Create output directory
examples_dir = Path(__file__).parent
examples_dir.mkdir(exist_ok=True)


def create_cell_styling_examples():
    """Create a notebook demonstrating cell-level styling."""
    nb = nbf.v4.new_notebook()
    
    # Title
    title_cell = nbf.v4.new_markdown_cell(
        "# Cell-Level Styling Examples\n\n"
        "This notebook demonstrates various cell-level styling options."
    )
    nb.cells.append(title_cell)
    
    # Example 1: Highlighted Important Cell
    markdown_cell = nbf.v4.new_markdown_cell(
        "## Important Information\n\n"
        "This cell uses a yellow highlight to draw attention to important content."
    )
    markdown_cell.metadata['style'] = {
        'background-color': '#fff9c4',
        'border': '3px dashed #fbc02d',
        'padding': '20px',
        'margin': '15px 0',
        'border-radius': '8px'
    }
    nb.cells.append(markdown_cell)
    
    # Example 2: Error/Warning Styling
    code_cell = nbf.v4.new_code_cell(
        "# This cell demonstrates error/warning styling\n"
        "import sys\n"
        "print('Warning: This is a demonstration of error styling')\n"
        "print('Use this style for cells that show error examples')"
    )
    code_cell.metadata['style'] = {
        'background-color': '#ffebee',
        'border-left': '6px solid #f44336',
        'padding': '15px',
        'margin': '15px 0'
    }
    nb.cells.append(code_cell)
    
    # Example 3: Success/Info Styling
    code_cell = nbf.v4.new_code_cell(
        "# Success styling example\n"
        "result = 42\n"
        "print(f'Success! The answer is {result}')\n"
        "print('Use this style to highlight successful operations')"
    )
    code_cell.metadata['style'] = {
        'background-color': '#e8f5e9',
        'border-left': '6px solid #4caf50',
        'padding': '15px',
        'margin': '15px 0'
    }
    nb.cells.append(code_cell)
    
    # Example 4: Gradient Background
    markdown_cell = nbf.v4.new_markdown_cell(
        "## Stylish Gradient\n\n"
        "This cell uses a CSS gradient for a modern, eye-catching appearance.\n\n"
        "Perfect for section headers or key takeaways."
    )
    markdown_cell.metadata['style'] = (
        "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
        "color: white; padding: 30px; margin: 20px 0; "
        "border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
    )
    nb.cells.append(markdown_cell)
    
    # Example 5: Box Shadow Effect
    code_cell = nbf.v4.new_code_cell(
        "# Elevated card-like styling\n"
        "data = {'x': [1, 2, 3], 'y': [4, 5, 6]}\n"
        "print('This cell has a subtle shadow for depth')\n"
        "print(data)"
    )
    code_cell.metadata['style'] = {
        'background-color': '#ffffff',
        'border': '1px solid #e0e0e0',
        'border-radius': '12px',
        'padding': '20px',
        'margin': '20px 0',
        'box-shadow': '0 8px 16px rgba(0,0,0,0.15)'
    }
    nb.cells.append(code_cell)
    
    # Save notebook
    output_path = examples_dir / 'cell_styling.ipynb'
    with open(output_path, 'w') as f:
        nbf.write(nb, f)
    print(f"Created: {output_path}")


def create_input_output_styling():
    """Create a notebook demonstrating input/output styling."""
    nb = nbf.v4.new_notebook()
    
    # Title
    title_cell = nbf.v4.new_markdown_cell(
        "# Input and Output Styling Examples\n\n"
        "This notebook demonstrates how to style input and output areas separately."
    )
    nb.cells.append(title_cell)
    
    # Example 1: Input Styling
    code_cell = nbf.v4.new_code_cell(
        "# Input area with blue accent\n"
        "def calculate_sum(a, b):\n"
        "    return a + b\n\n"
        "result = calculate_sum(10, 20)\n"
        "print(f'The sum is: {result}')"
    )
    code_cell.metadata['input-style'] = {
        'background-color': '#e3f2fd',
        'border-left': '5px solid #2196f3',
        'padding': '15px',
        'font-family': 'Monaco, Consolas, monospace',
        'font-size': '14px'
    }
    nb.cells.append(code_cell)
    
    # Example 2: Output Styling
    code_cell = nbf.v4.new_code_cell(
        "# Output area with green accent\n"
        "print('=' * 50)\n"
        "print('OUTPUT STYLING EXAMPLE')\n"
        "print('=' * 50)\n"
        "print('This output has custom styling applied')\n"
        "for i in range(1, 4):\n"
        "    print(f'Item {i}: Value {i * 10}')"
    )
    code_cell.metadata['output-style'] = {
        'background-color': '#e8f5e9',
        'border': '2px solid #4caf50',
        'padding': '15px',
        'font-family': 'Monaco, Consolas, monospace',
        'font-size': '13px',
        'border-radius': '6px'
    }
    nb.cells.append(code_cell)
    
    # Example 3: Combined Input and Output Styling
    code_cell = nbf.v4.new_code_cell(
        "# Both input and output styled\n"
        "import random\n\n"
        "print('Generating random numbers:')\n"
        "numbers = [random.randint(1, 100) for _ in range(5)]\n"
        "print(f'Numbers: {numbers}')\n"
        "print(f'Average: {sum(numbers) / len(numbers):.2f}')"
    )
    code_cell.metadata['style'] = {
        'margin': '25px 0',
        'border-radius': '10px',
        'overflow': 'hidden',
        'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'
    }
    code_cell.metadata['input-style'] = {
        'background-color': '#fce4ec',
        'color': '#880e4f',
        'padding': '18px',
        'border-bottom': '2px solid #d81b60'
    }
    code_cell.metadata['output-style'] = {
        'background-color': '#f3e5f5',
        'padding': '18px',
        'font-family': 'Monaco, Consolas, monospace'
    }
    nb.cells.append(code_cell)
    
    # Example 4: Code Highlighting with Output
    code_cell = nbf.v4.new_code_cell(
        "# Styled code execution\n"
        "def fibonacci(n):\n"
        "    if n <= 1:\n"
        "        return n\n"
        "    return fibonacci(n-1) + fibonacci(n-2)\n\n"
        "print('Fibonacci sequence:')\n"
        "for i in range(10):\n"
        "    print(f'F({i}) = {fibonacci(i)}')"
    )
    code_cell.metadata['input-style'] = {
        'background': 'linear-gradient(to right, #f5f5f5 0%, #e8e8e8 100%)',
        'border-left': '4px solid #ff6b6b',
        'padding': '15px',
        'font-weight': 'bold'
    }
    code_cell.metadata['output-style'] = {
        'background-color': '#fff3cd',
        'border': '1px solid #ffc107',
        'padding': '15px',
        'border-radius': '4px'
    }
    nb.cells.append(code_cell)
    
    # Save notebook
    output_path = examples_dir / 'input_output_styling.ipynb'
    with open(output_path, 'w') as f:
        nbf.write(nb, f)
    print(f"Created: {output_path}")


def create_custom_classes_example():
    """Create a notebook demonstrating custom CSS classes."""
    nb = nbf.v4.new_notebook()
    
    # Add notebook-level stylesheet
    nb.metadata['stylesheet'] = 'custom-styles.css'
    
    # Title
    title_cell = nbf.v4.new_markdown_cell(
        "# Custom CSS Classes Example\n\n"
        "This notebook demonstrates using custom CSS classes with an external stylesheet."
    )
    nb.cells.append(title_cell)
    
    # Example 1: Cell-level class
    markdown_cell = nbf.v4.new_markdown_cell(
        "## Important Notice\n\n"
        "This cell uses custom CSS classes defined in an external stylesheet."
    )
    markdown_cell.metadata['class'] = 'highlight-important bordered'
    nb.cells.append(markdown_cell)
    
    # Example 2: Input and output classes
    code_cell = nbf.v4.new_code_cell(
        "# Code with custom classes\n"
        "def greet(name):\n"
        "    return f'Hello, {name}!'\n\n"
        "message = greet('World')\n"
        "print(message)"
    )
    code_cell.metadata['input-class'] = 'code-highlight'
    code_cell.metadata['output-class'] = 'result-highlight'
    nb.cells.append(code_cell)
    
    # Example 3: Combined classes and inline styles
    code_cell = nbf.v4.new_code_cell(
        "# Mixing classes and styles\n"
        "data = [1, 2, 3, 4, 5]\n"
        "squared = [x**2 for x in data]\n"
        "print(f'Original: {data}')\n"
        "print(f'Squared: {squared}')"
    )
    code_cell.metadata['class'] = 'important-cell'
    code_cell.metadata['style'] = {'margin': '20px 0'}
    code_cell.metadata['input-class'] = 'code-section'
    nb.cells.append(code_cell)
    
    # Save notebook
    output_path = examples_dir / 'custom_classes.ipynb'
    with open(output_path, 'w') as f:
        nbf.write(nb, f)
    print(f"Created: {output_path}")


def create_custom_stylesheet():
    """Create a custom CSS stylesheet for the classes example."""
    css_content = """/* Custom Styles for Jupyter Export HTML Style Examples */

.highlight-important {
    background: linear-gradient(135deg, #fff9c4 0%, #ffeb3b 100%);
    border: 3px solid #fbc02d;
    padding: 20px;
    margin: 15px 0;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(251, 192, 45, 0.3);
}

.bordered {
    border-radius: 12px;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.code-highlight {
    background-color: #263238;
    color: #aed581;
    padding: 15px;
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 14px;
    border-left: 5px solid #00bcd4;
}

.result-highlight {
    background-color: #e8f5e9;
    border-left: 5px solid #4caf50;
    padding: 15px;
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 13px;
}

.important-cell {
    background-color: #fff3e0;
    border: 2px solid #ff9800;
    border-radius: 8px;
    padding: 10px;
}

.code-section {
    background: linear-gradient(to right, #e3f2fd 0%, #bbdefb 100%);
    border-left: 4px solid #2196f3;
    padding: 15px;
}

.warning-cell {
    background-color: #fff3cd;
    border: 2px dashed #ff9800;
    border-radius: 8px;
    padding: 15px;
}
"""
    
    css_path = examples_dir / 'custom-styles.css'
    with open(css_path, 'w') as f:
        f.write(css_content)
    print(f"Created: {css_path}")


def create_notebook_level_styling():
    """Create a notebook demonstrating notebook-level styling."""
    nb = nbf.v4.new_notebook()
    
    # Add notebook-level styles
    nb.metadata['style'] = """
    body {
        font-family: 'Segoe UI', 'Roboto', 'Helvetica', sans-serif;
        max-width: 1200px;
        margin: 0 auto;
        padding: 30px;
        background-color: #fafafa;
    }
    .jp-Cell {
        margin-bottom: 30px;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        padding: 15px;
    }
    .jp-MarkdownCell {
        border-left: 4px solid #2196f3;
    }
    .jp-CodeCell {
        border-left: 4px solid #4caf50;
    }
    """
    
    # Title
    title_cell = nbf.v4.new_markdown_cell(
        "# Notebook-Level Styling Example\n\n"
        "This entire notebook has custom global styles applied that affect all cells."
    )
    nb.cells.append(title_cell)
    
    # Content cells
    markdown_cell = nbf.v4.new_markdown_cell(
        "## Introduction\n\n"
        "Notice how all cells in this notebook have a consistent, polished appearance "
        "with shadows, spacing, and colored left borders.\n\n"
        "The body has a maximum width and is centered on the page."
    )
    nb.cells.append(markdown_cell)
    
    code_cell = nbf.v4.new_code_cell(
        "# Code cells also inherit the global styling\n"
        "print('This notebook has a cohesive, professional look')\n"
        "print('All cells have the same spacing and shadow effects')"
    )
    nb.cells.append(code_cell)
    
    markdown_cell = nbf.v4.new_markdown_cell(
        "## Features\n\n"
        "- Consistent spacing between cells\n"
        "- Subtle shadows for depth\n"
        "- Colored left borders to distinguish cell types\n"
        "- Limited width for better readability\n"
        "- Light gray background"
    )
    nb.cells.append(markdown_cell)
    
    code_cell = nbf.v4.new_code_cell(
        "# More code\n"
        "for i in range(3):\n"
        "    print(f'Line {i+1}: Global styling applies to all content')"
    )
    nb.cells.append(code_cell)
    
    # Save notebook
    output_path = examples_dir / 'notebook_styling.ipynb'
    with open(output_path, 'w') as f:
        nbf.write(nb, f)
    print(f"Created: {output_path}")


def create_comprehensive_example():
    """Create a comprehensive notebook showcasing multiple features."""
    nb = nbf.v4.new_notebook()
    
    # Add notebook-level styles
    nb.metadata['style'] = """
    body {
        font-family: 'Arial', sans-serif;
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
    }
    h1, h2 { color: #1976d2; }
    """
    
    # Title with gradient
    title_cell = nbf.v4.new_markdown_cell(
        "# Comprehensive Styling Demo\n\n"
        "**A showcase of all styling features in one notebook**"
    )
    title_cell.metadata['style'] = (
        "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); "
        "color: white; padding: 40px; margin: 0 0 30px 0; "
        "border-radius: 15px; box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3); "
        "text-align: center;"
    )
    nb.cells.append(title_cell)
    
    # Section 1
    section_cell = nbf.v4.new_markdown_cell(
        "## 1. Important Information"
    )
    section_cell.metadata['style'] = {
        'background-color': '#fff3cd',
        'border-left': '6px solid #ffc107',
        'padding': '15px',
        'margin': '20px 0'
    }
    nb.cells.append(section_cell)
    
    code_cell = nbf.v4.new_code_cell(
        "# Configuration settings\n"
        "config = {\n"
        "    'version': '1.0',\n"
        "    'mode': 'production',\n"
        "    'debug': False\n"
        "}\n"
        "print('Configuration loaded:')\n"
        "for key, value in config.items():\n"
        "    print(f'  {key}: {value}')"
    )
    code_cell.metadata['input-style'] = {
        'background-color': '#e3f2fd',
        'border-left': '4px solid #2196f3',
        'padding': '15px'
    }
    code_cell.metadata['output-style'] = {
        'background-color': '#e8f5e9',
        'border': '1px solid #4caf50',
        'padding': '15px',
        'border-radius': '6px'
    }
    nb.cells.append(code_cell)
    
    # Section 2
    section_cell = nbf.v4.new_markdown_cell(
        "## 2. Data Processing"
    )
    section_cell.metadata['style'] = {
        'background-color': '#e1f5fe',
        'border-left': '6px solid #03a9f4',
        'padding': '15px',
        'margin': '20px 0'
    }
    nb.cells.append(section_cell)
    
    code_cell = nbf.v4.new_code_cell(
        "# Process data\n"
        "data = [10, 20, 30, 40, 50]\n"
        "average = sum(data) / len(data)\n"
        "print(f'Data: {data}')\n"
        "print(f'Average: {average}')\n"
        "print(f'Min: {min(data)}, Max: {max(data)}')"
    )
    code_cell.metadata['style'] = {
        'background-color': '#ffffff',
        'border-radius': '10px',
        'box-shadow': '0 4px 8px rgba(0,0,0,0.1)',
        'padding': '10px',
        'margin': '15px 0'
    }
    nb.cells.append(code_cell)
    
    # Section 3
    section_cell = nbf.v4.new_markdown_cell(
        "## 3. Results Summary"
    )
    section_cell.metadata['style'] = {
        'background-color': '#f3e5f5',
        'border-left': '6px solid #9c27b0',
        'padding': '15px',
        'margin': '20px 0'
    }
    nb.cells.append(section_cell)
    
    summary_cell = nbf.v4.new_markdown_cell(
        "### ✅ Analysis Complete\n\n"
        "All data has been processed successfully. "
        "The results are ready for export."
    )
    summary_cell.metadata['style'] = {
        'background-color': '#e8f5e9',
        'border': '3px solid #4caf50',
        'padding': '25px',
        'border-radius': '12px',
        'margin': '15px 0',
        'box-shadow': '0 4px 8px rgba(76, 175, 80, 0.2)'
    }
    nb.cells.append(summary_cell)
    
    # Save notebook
    output_path = examples_dir / 'comprehensive_demo.ipynb'
    with open(output_path, 'w') as f:
        nbf.write(nb, f)
    print(f"Created: {output_path}")


if __name__ == '__main__':
    print("Generating example notebooks...")
    create_cell_styling_examples()
    create_input_output_styling()
    create_custom_classes_example()
    create_custom_stylesheet()
    create_notebook_level_styling()
    create_comprehensive_example()
    print("\nAll example notebooks created successfully!")
