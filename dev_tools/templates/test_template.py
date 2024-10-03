# This is the test template used for generating basic tests
TEMPLATE = """
import pytest

def test_imports():
    try:
        import {module_import}
    except ImportError:
        pytest.fail("Failed to import {module_import}")

def test_functions():
    # Add tests for functions in the {module_import} module
    try:
        from {module_import} import {function_names}
    except AttributeError:
        pytest.fail(f"Missing function(s) {{function_names}} in {{module_import}}")
"""
