#!/usr/bin/env python3
"""
Test script to demonstrate the HTMLStyleExporter functionality.
"""

from jupyter_export_html_style import HTMLStyleExporter
from jupyter_export_html_style.preprocessor import StyleMetadataPreprocessor
import sys


def test_exporter_creation():
    """Test that the exporter can be created successfully."""
    print("Test 1: Creating HTMLStyleExporter...")
    exporter = HTMLStyleExporter()
    assert exporter.embed_images == True, "Images should be embedded by default"
    assert exporter.template_name == 'html_style', "Should use html_style template"
    print("  ✓ Exporter created successfully")
    print(f"  ✓ Embed images: {exporter.embed_images}")
    print(f"  ✓ Template name: {exporter.template_name}")
    return True


def test_preprocessor_sanitization():
    """Test that the preprocessor sanitizes dangerous CSS."""
    print("\nTest 2: Testing CSS sanitization...")
    preprocessor = StyleMetadataPreprocessor()
    
    # Valid styles should pass through
    valid_style = "background-color: #e3f2fd; padding: 10px;"
    sanitized = preprocessor._sanitize_style(valid_style)
    assert sanitized == valid_style, "Valid styles should be preserved"
    print("  ✓ Valid CSS preserved")
    
    # Malicious styles should be sanitized
    malicious_styles = [
        ("background: url('javascript:alert(1)');", "javascript"),
        ("width: expression(alert('XSS'));", "expression"),
        ("@import url('evil.css');", "import"),
    ]
    
    for malicious, keyword in malicious_styles:
        sanitized = preprocessor._sanitize_style(malicious)
        assert keyword not in sanitized.lower().replace(' ', ''), f"Should remove {keyword}"
        print(f"  ✓ Sanitized {keyword}")
    
    return True


def test_notebook_export():
    """Test exporting a notebook with style metadata."""
    print("\nTest 3: Exporting example notebook...")
    exporter = HTMLStyleExporter()
    
    try:
        body, resources = exporter.from_filename('example_notebook.ipynb')
        print("  ✓ Notebook exported successfully")
        print(f"  ✓ Output size: {len(body)} bytes")
        
        # Check that styles are present in output
        assert 'style="background-color: #e3f2fd' in body, "Blue style should be in output"
        print("  ✓ Blue style present in HTML")
        
        assert 'style="background-color: #fff3e0' in body, "Orange style should be in output"
        print("  ✓ Orange style present in HTML")
        
        assert 'style="background: linear-gradient' in body, "Gradient style should be in output"
        print("  ✓ Gradient style present in HTML")
        
        return True
    except FileNotFoundError:
        print("  ⚠ example_notebook.ipynb not found, skipping this test")
        return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("HTMLStyleExporter Test Suite")
    print("=" * 60)
    
    tests = [
        test_exporter_creation,
        test_preprocessor_sanitization,
        test_notebook_export,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ Test failed with error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
