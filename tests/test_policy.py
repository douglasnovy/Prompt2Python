"""
Comprehensive tests for the Policy DSL & Parser module.
"""

import pytest
import time
from typing import Any, Dict, List

from prompted_objects.policy import (
    # Core functions
    safe_eval, evaluate_policy, validate_policy_rules,
    # Helper functions
    is_int, is_float, is_str, is_list, is_dict, is_bool,
    matches, contains, len_of, has_keys, has_any_key,
    input_size_kb, in_range, gt, lt, eq, ne, schema_ok,
)
from prompted_objects.exceptions import PolicyError


class TestHelperFunctions:
    """Test all helper functions for policy expressions."""

    def test_type_checking_functions(self):
        """Test type checking helper functions."""
        # Test is_int
        assert is_int(42) is True
        assert is_int(42.0) is False
        assert is_int("42") is False
        assert is_int(True) is False  # bool is not int
        assert is_int(False) is False

        # Test is_float
        assert is_float(42.0) is True
        assert is_float(42) is False
        assert is_float("42.0") is False

        # Test is_str
        assert is_str("hello") is True
        assert is_str(42) is False
        assert is_str("") is True

        # Test is_list
        assert is_list([1, 2, 3]) is True
        assert is_list((1, 2, 3)) is False
        assert is_list("hello") is False

        # Test is_dict
        assert is_dict({"a": 1}) is True
        assert is_dict([("a", 1)]) is False

        # Test is_bool
        assert is_bool(True) is True
        assert is_bool(False) is True
        assert is_bool(1) is False
        assert is_bool(0) is False

    def test_string_functions(self):
        """Test string and pattern matching functions."""
        # Test matches (regex)
        assert matches("test_string", r"test_.*") is True
        assert matches("hello", r"test_.*") is False
        assert matches("123", r"\d+") is True

        # Test contains
        assert contains("hello world", "world") is True
        assert contains("hello world", "foo") is False
        assert contains("", "foo") is False

    def test_collection_functions(self):
        """Test collection helper functions."""
        # Test len_of
        assert len_of([1, 2, 3]) == 3
        assert len_of("hello") == 5
        assert len_of({"a": 1, "b": 2}) == 2
        assert len_of(42) == 0  # Non-collections return 0

        # Test has_keys
        data = {"a": 1, "b": 2, "c": 3}
        assert has_keys(data, ["a", "b"]) is True
        assert has_keys(data, ["a", "d"]) is False
        assert has_keys(data, []) is True  # Empty list always true
        assert has_keys("not_a_dict", ["a"]) is False

        # Test has_any_key
        assert has_any_key(data, ["a", "d"]) is True
        assert has_any_key(data, ["d", "e"]) is False
        assert has_any_key("not_a_dict", ["a"]) is False

    def test_size_estimation(self):
        """Test input size estimation function."""
        # Test with various data types
        small_args = (1, "hello", [1, 2])
        size = input_size_kb(small_args)
        assert size > 0
        assert size < 1.0  # Should be much less than 1KB

        # Test with larger data
        large_args = ("x" * 1000, [1] * 100)
        large_size = input_size_kb(large_args)
        assert large_size > size

        # Test with empty args
        assert input_size_kb(()) == 0.0

    def test_range_functions(self):
        """Test range and comparison functions."""
        # Test in_range
        assert in_range(5, 1, 10) is True
        assert in_range(0, 1, 10) is False
        assert in_range(15, 1, 10) is False
        assert in_range("not_a_number", 1, 10) is False

        # Test gt (greater than)
        assert gt(10, 5) is True
        assert gt(5, 10) is False
        assert gt("not_a_number", 5) is False

        # Test lt (less than)
        assert lt(5, 10) is True
        assert lt(10, 5) is False
        assert lt("not_a_number", 5) is False

        # Test eq (equals)
        assert eq(5, 5) is True
        assert eq(5, 10) is False
        assert eq("hello", "hello") is True

        # Test ne (not equals)
        assert ne(5, 10) is True
        assert ne(5, 5) is False

    def test_schema_validation(self):
        """Test schema validation function (placeholder)."""
        # Currently always returns True
        assert schema_ok((1, 2, 3), "any_schema") is True


class TestSafeEvaluation:
    """Test the safe expression evaluation system."""

    def test_basic_expression_evaluation(self):
        """Test basic expression evaluation."""
        context = {"a": 5, "b": 3}

        # Simple arithmetic
        result = safe_eval("a + b", context)
        assert result == 8

        # Function calls
        result = safe_eval("is_int(a)", context)
        assert result is True

        # Complex expressions
        result = safe_eval("a > 0 and is_int(b)", context)
        assert result is True

    def test_security_restrictions(self):
        """Test that dangerous operations are blocked."""
        context = {"data": [1, 2, 3]}

        # Test that eval is not available
        with pytest.raises(PolicyError):
            safe_eval("eval('1+1')", context)

        # Test that exec is not available
        with pytest.raises(PolicyError):
            safe_eval("exec('print(1)')", context)

        # Test that open is not available
        with pytest.raises(PolicyError):
            safe_eval("open('/etc/passwd')", context)

    def test_timeout_protection(self):
        """Test that evaluation times out for long-running expressions."""
        context = {"data": list(range(10000))}

        # This should timeout due to large list operations
        with pytest.raises(PolicyError, match="timed out"):
            safe_eval("sum(len_of(data) for _ in range(10000))", context, timeout=0.1)

    def test_error_handling(self):
        """Test error handling for invalid expressions."""
        context = {"a": 5}

        # Syntax error
        with pytest.raises(PolicyError):
            safe_eval("a + ", context)

        # Name error
        with pytest.raises(PolicyError):
            safe_eval("nonexistent_variable", context)

        # Type error in expression
        with pytest.raises(PolicyError):
            safe_eval("a / 0", context)


class TestPolicyEvaluation:
    """Test policy rule evaluation and routing decisions."""

    def test_basic_policy_evaluation(self):
        """Test basic policy evaluation with simple rules."""
        policy = [
            {"if": "is_int(a) and is_int(b)", "then": "code"}
        ]

        # Should match and return "code"
        result = evaluate_policy(policy, (2, 3), {})
        assert result == "code"

        # Should not match and return default "model"
        result = evaluate_policy(policy, ("hello", 3), {})
        assert result == "model"

    def test_multiple_rules_first_match_wins(self):
        """Test that first matching rule wins."""
        policy = [
            {"if": "is_str(a)", "then": "model"},
            {"if": "is_int(a)", "then": "code"}
        ]

        # First rule should match strings
        result = evaluate_policy(policy, ("hello",), {})
        assert result == "model"

        # Second rule should match integers (if first rule doesn't match)
        result = evaluate_policy(policy, (42,), {})
        assert result == "code"

    def test_complex_policy_expressions(self):
        """Test complex policy expressions."""
        policy = [
            {"if": "input_size_kb(args) > 1.0", "then": "model"},
            {"if": "len_of(a) > 5", "then": "codegen"},
            {"if": "has_keys(kwargs, ['special'])", "then": "code"}
        ]

        # Test size-based routing
        large_data = ("x" * 2000,)  # > 1KB when estimated
        result = evaluate_policy(policy, large_data, {})
        assert result == "model"

        # Test length-based routing
        result = evaluate_policy(policy, ("short",), {})
        assert result == "codegen"

        # Test kwargs-based routing
        result = evaluate_policy(policy, ("anything",), {"special": True})
        assert result == "code"

    def test_default_routing(self):
        """Test default routing when no rules match."""
        policy = [
            {"if": "is_int(a) and a > 100", "then": "code"}
        ]

        # Should default to "model" when no rules match
        result = evaluate_policy(policy, (50,), {})
        assert result == "model"

        result = evaluate_policy(policy, ("not_int",), {})
        assert result == "model"

    def test_empty_policy(self):
        """Test behavior with empty policy."""
        result = evaluate_policy([], (1, 2, 3), {"key": "value"})
        assert result == "model"  # Default routing

    def test_invalid_policy_rules(self):
        """Test handling of invalid policy rule structures."""
        # Rule without 'if'
        policy = [{"then": "code"}]
        result = evaluate_policy(policy, (1,), {})
        assert result == "model"  # Should continue to default

        # Rule without 'then'
        policy = [{"if": "is_int(a)"}]
        result = evaluate_policy(policy, (1,), {})
        assert result == "model"  # Should continue to default

        # Rule with invalid result
        policy = [{"if": "is_int(a)", "then": "invalid"}]
        result = evaluate_policy(policy, (1,), {})
        assert result == "model"  # Should continue to default


class TestPolicyValidation:
    """Test policy rule validation."""

    def test_valid_policy_validation(self):
        """Test validation of valid policy rules."""
        valid_policy = [
            {"if": "is_int(a) and is_int(b)", "then": "code"},
            {"if": "len_of(a) > 5", "then": "model"}
        ]

        errors = validate_policy_rules(valid_policy)
        assert len(errors) == 0

    def test_invalid_policy_validation(self):
        """Test validation of invalid policy rules."""
        invalid_policy = [
            {"then": "code"},  # Missing 'if'
            {"if": "is_int(a)"},  # Missing 'then'
            {"if": "is_int(a)", "then": "invalid"},  # Invalid result
            "not_a_dict",  # Not a dict
        ]

        errors = validate_policy_rules(invalid_policy)
        assert len(errors) > 0
        assert any("missing 'if'" in error for error in errors)
        assert any("missing 'then'" in error for error in errors)
        assert any("invalid result" in error for error in errors)
        assert any("must be a dictionary" in error for error in errors)

    def test_syntax_validation(self):
        """Test validation of expression syntax."""
        # Invalid syntax
        invalid_policy = [
            {"if": "a +", "then": "code"}  # Syntax error
        ]

        errors = validate_policy_rules(invalid_policy)
        # Should catch syntax errors
        assert len(errors) > 0


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    def test_math_example_policy(self):
        """Test the math example from the workstream spec."""
        policy = [
            {"if": "is_int(a) and is_int(b)", "then": "code"},
            {"if": "input_size_kb(args) > 1.0", "then": "model"}
        ]

        # Should route to code for integers
        result = evaluate_policy(policy, (2, 3), {})
        assert result == "code"

        # Should route to model for large inputs
        large_input = ("x" * 2000, "y" * 2000)
        result = evaluate_policy(policy, large_input, {})
        assert result == "model"

        # Should route to model for non-integers
        result = evaluate_policy(policy, ("hello", 3), {})
        assert result == "model"

    def test_string_processing_policy(self):
        """Test string processing policy example."""
        policy = [
            {"if": "matches(name, r'^test_')", "then": "model"},
            {"if": "len_of(name) < 10", "then": "code"}
        ]

        # Should route to model for test functions
        result = evaluate_policy(policy, (), {"name": "test_function"})
        assert result == "model"

        # Should route to code for short names
        result = evaluate_policy(policy, (), {"name": "short"})
        assert result == "code"

        # Should route to model for long names
        result = evaluate_policy(policy, (), {"name": "very_long_function_name"})
        assert result == "model"

    def test_complex_nested_policy(self):
        """Test complex nested policy with multiple conditions."""
        policy = [
            {
                "if": "is_dict(kwargs) and has_keys(kwargs, ['user_id', 'action']) and is_str(kwargs['action'])",
                "then": "code"
            },
            {
                "if": "input_size_kb(args) > 0.1",
                "then": "model"
            },
            {
                "if": "len_of(a) > 100",
                "then": "codegen"
            }
        ]

        # Should route to code for valid user actions
        result = evaluate_policy(policy, (), {
            "user_id": 123,
            "action": "create"
        })
        assert result == "code"

        # Should route to model for large inputs
        large_input = (list(range(1000)),)
        result = evaluate_policy(policy, large_input, {})
        assert result == "model"

        # Should route to codegen for long collections
        result = evaluate_policy(policy, (list(range(200)),), {})
        assert result == "codegen"


class TestPerformance:
    """Test performance characteristics."""

    def test_evaluation_performance(self):
        """Test that policy evaluation is reasonably fast."""
        policy = [
            {"if": "is_int(a) and is_int(b) and len_of(a) < 1000", "then": "code"},
            {"if": "input_size_kb(args) > 1.0", "then": "model"}
        ]

        # Should complete quickly for normal inputs
        start_time = time.time()
        for _ in range(100):
            result = evaluate_policy(policy, (1, 2), {"data": [1, 2, 3]})
        end_time = time.time()

        # Should complete 100 evaluations in under 1 second
        assert end_time - start_time < 1.0

    def test_memory_usage(self):
        """Test that evaluation doesn't have memory leaks."""
        import gc

        policy = [{"if": "is_int(a)", "then": "code"}]

        # Force garbage collection before test
        gc.collect()

        initial_objects = len(gc.get_objects())

        # Run many evaluations
        for i in range(1000):
            result = evaluate_policy(policy, (i,), {})

        # Force garbage collection after test
        gc.collect()

        final_objects = len(gc.get_objects())

        # Should not create excessive objects
        assert final_objects - initial_objects < 1000


if __name__ == "__main__":
    pytest.main([__file__])
