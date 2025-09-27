#!/usr/bin/env python3
"""
Simple test runner for the policy module.
"""

import sys
import traceback
from typing import Any, Callable

# Add the workspace to the Python path
sys.path.insert(0, '/workspace')

def run_test(test_func: Callable[[], None], test_name: str) -> bool:
    """Run a single test function and report results."""
    try:
        print(f"Running {test_name}...", end=" ")
        test_func()
        print("✅ PASSED")
        return True
    except Exception as e:
        print("❌ FAILED")
        print(f"  Error: {e}")
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic policy functionality."""
    from prompted_objects.policy import evaluate_policy, is_int, is_str, input_size_kb

    # Test helper functions
    assert is_int(42) is True
    assert is_str("hello") is True

    # Test basic policy evaluation
    policy = [{"if": "is_int(args[0])", "then": "code"}]
    result = evaluate_policy(policy, (42,), {})
    assert result == "code"

    # Test default routing
    result = evaluate_policy(policy, ("hello",), {})
    assert result == "model"

    # Test size estimation
    size = input_size_kb((1, 2, 3))
    assert size >= 0

def test_security():
    """Test security features."""
    from prompted_objects.policy import safe_eval
    from prompted_objects.exceptions import PolicyError

    # Test that dangerous functions are not available
    try:
        safe_eval("eval('1+1')", {})
        assert False, "Should have blocked eval"
    except PolicyError:
        pass  # Expected

    try:
        safe_eval("open('/etc/passwd')", {})
        assert False, "Should have blocked open"
    except PolicyError:
        pass  # Expected

def test_complex_policies():
    """Test complex policy scenarios."""
    from prompted_objects.policy import evaluate_policy

    # Complex nested policy (order matters - first match wins)
    policy = [
        {"if": "input_size_kb(args) > 1.0", "then": "model"},
        {"if": "len_of(args[0]) > 5", "then": "codegen"},
        {"if": "is_int(args[0]) and args[0] > 10", "then": "code"}
    ]

    # Should route to model for large data (matches first rule)
    large_data = ("x" * 2000,)
    result = evaluate_policy(policy, large_data, {})
    assert result == "model"

    # Should route to codegen for long strings
    result = evaluate_policy(policy, ("very_long_string",), {})
    assert result == "codegen"

    # Should route to code for integers > 10
    result = evaluate_policy(policy, (15,), {})
    assert result == "code"

def test_edge_cases():
    """Test edge cases and error conditions."""
    from prompted_objects.policy import evaluate_policy, validate_policy_rules

    # Empty policy should default to model
    result = evaluate_policy([], (1, 2, 3), {})
    assert result == "model"

    # Invalid policy rules should not crash
    result = evaluate_policy([{"invalid": "rule"}], (1,), {})
    assert result == "model"

    # Policy validation should work
    errors = validate_policy_rules([{"if": "is_int(a)", "then": "code"}])
    assert len(errors) == 0

    errors = validate_policy_rules([{"then": "code"}])  # Missing 'if'
    assert len(errors) > 0

def main():
    """Run all tests."""
    print("🧪 Running Policy DSL Tests")
    print("=" * 50)

    tests = [
        (test_basic_functionality, "Basic Functionality"),
        (test_security, "Security Features"),
        (test_complex_policies, "Complex Policies"),
        (test_edge_cases, "Edge Cases"),
    ]

    passed = 0
    total = len(tests)

    for test_func, test_name in tests:
        if run_test(test_func, test_name):
            passed += 1

    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())