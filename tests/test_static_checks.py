"""Tests for static code validation."""

import pytest
from prompted_objects.exceptions import ValidationError
from prompted_objects.codegen.static_checks import validate_ast


class TestStaticChecks:
    """Test static validation of generated code."""

    def test_valid_code_passes(self):
        """Test that valid, safe code passes validation."""
        body = """
result = a + b
if result > 10:
    result = result * 2
return result
"""
        # Should not raise any exception
        validate_ast(body)

    def test_forbidden_builtin_print(self):
        """Test that print builtin is forbidden."""
        body = """
print("Debug message")  # Forbidden builtin
return a + b
"""
        with pytest.raises(ValidationError) as exc_info:
            validate_ast(body)

        assert "print" in str(exc_info.value)

    def test_forbidden_builtin_eval(self):
        """Test that eval builtin is forbidden."""
        body = """
result = eval("a + b")  # Dangerous eval
return result
"""
        with pytest.raises(ValidationError) as exc_info:
            validate_ast(body)

        assert "eval" in str(exc_info.value)

    def test_import_violation_without_capability(self):
        """Test that imports not in allowlist are forbidden."""
        body = """
import os  # Not in default allowlist
return os.getcwd()
"""
        with pytest.raises(ValidationError) as exc_info:
            validate_ast(body)

        error_str = str(exc_info.value)
        assert "Import not allowed: os" in error_str

    def test_import_allowed_with_capability(self):
        """Test that allowed imports work with proper capabilities."""
        body = """
import math
import json
return math.sqrt(4)
"""
        capabilities = {"imports": ["math", "json"]}
        # Should not raise any exception
        validate_ast(body, capabilities)

    def test_os_operation_with_io_capability(self):
        """Test that OS operations work with io capability."""
        body = """
import os
return os.getcwd()
"""
        capabilities = {"imports": ["os"], "io": True}
        # Should not raise any exception
        validate_ast(body, capabilities)

    def test_safe_modules_allowed(self):
        """Test that safe modules are allowed by default."""
        body = """
import math
import re
import itertools
import functools
result = math.sqrt(4)
pattern = re.compile(r'\\d+')
return list(itertools.islice(functools.count(), 5))
"""
        # Should not raise any exception - these are safe modules
        validate_ast(body)
