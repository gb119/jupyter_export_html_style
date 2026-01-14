#!/usr/bin/env python3
"""Take screenshots of example HTML files."""

from pathlib import Path
from playwright.sync_api import sync_playwright

examples_dir = Path(__file__).parent
html_files = [
    'cell_styling.html',
    'input_output_styling.html',
    'custom_classes.html',
    'notebook_styling.html',
    'comprehensive_demo.html'
]

def take_screenshot(html_file):
    """Take a screenshot of an HTML file."""
    html_path = examples_dir / html_file
    screenshot_name = html_file.replace('.html', '.png')
    screenshot_path = examples_dir / screenshot_name
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1200, 'height': 800})
        
        # Load HTML file
        page.goto(f'file://{html_path.absolute()}')
        
        # Wait for page to load
        page.wait_for_load_state('networkidle')
        
        # Take screenshot of full page
        page.screenshot(path=str(screenshot_path), full_page=True)
        
        browser.close()
        print(f"Screenshot saved: {screenshot_path}")

if __name__ == '__main__':
    print("Taking screenshots of HTML examples...")
    for html_file in html_files:
        try:
            take_screenshot(html_file)
        except Exception as e:
            print(f"Error taking screenshot of {html_file}: {e}")
    print("\nAll screenshots taken!")
