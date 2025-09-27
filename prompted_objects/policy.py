"""
Policy DSL & Parser for Prompted Objects.

This module implements a safe expression evaluation system for policy rules
that determine routing decisions between code artifacts, LLM models, and code generation.
"""

import ast
import re
import sys
import time
from typing import Any, Dict, List, Literal, Callable, Union
import logging

from prompted_objects.exceptions import PolicyError

# Configure logging
logger = logging.getLogger(__name__)

# Safe evaluation timeout in seconds
EVALUATION_TIMEOUT = 5.0

# Restricted globals for safe expression evaluation
SAFE_GLOBALS = {
    '__builtins__': {
        # Math operations
        'abs': abs,
        'min': min,
        'max': max,
        'round': round,
        'sum': sum,
        # Type checking
        'isinstance': isinstance,
        'type': type,
        # String operations
        'len': len,
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
        # Logic operations
        'all': all,
        'any': any,
        # Safe containers
        'list': list,
        'dict': dict,
        'set': set,
        'tuple': tuple,
    }
}


def safe_eval(expression: str, variables: Dict[str, Any], timeout: float = EVALUATION_TIMEOUT) -> Any:
    """
    Safely evaluate an expression with restricted globals and timeout protection.

    Args:
        expression: The expression string to evaluate
        variables: Variables to make available in the evaluation context
        timeout: Maximum evaluation time in seconds

    Returns:
        The result of the expression evaluation

    Raises:
        PolicyError: If evaluation fails or times out
    """
    try:
        # Create restricted evaluation environment
        eval_globals = SAFE_GLOBALS.copy()
        eval_locals = variables.copy()

        # Add timeout protection
        start_time = time.time()

        # Use eval with restricted globals
        result = eval(expression, eval_globals, eval_locals)

        # Check for timeout
        if time.time() - start_time > timeout:
            raise PolicyError(f"Expression evaluation timed out after {timeout}s", {"expression": expression})

        return result

    except Exception as e:
        # Log the error with fingerprint for debugging
        error_fingerprint = hash(f"{expression}:{str(e)}")
        logger.warning(f"Policy evaluation error (fingerprint: {error_fingerprint}): {e}")
        raise PolicyError(f"Expression evaluation failed: {e}", {
            "expression": expression,
            "error": str(e),
            "fingerprint": error_fingerprint
        })


# Type checking helper functions
def is_int(x: Any) -> bool:
    """Check if value is an integer."""
    return isinstance(x, int) and not isinstance(x, bool)


def is_float(x: Any) -> bool:
    """Check if value is a float."""
    return isinstance(x, float)


def is_str(x: Any) -> bool:
    """Check if value is a string."""
    return isinstance(x, str)


def is_list(x: Any) -> bool:
    """Check if value is a list."""
    return isinstance(x, list)


def is_dict(x: Any) -> bool:
    """Check if value is a dictionary."""
    return isinstance(x, dict)


def is_bool(x: Any) -> bool:
    """Check if value is a boolean."""
    return isinstance(x, bool)


# String and pattern matching functions
def matches(s: str, pattern: str) -> bool:
    """
    Check if string matches a regex pattern.

    Args:
        s: String to test
        pattern: Regex pattern to match against

    Returns:
        True if string matches pattern
    """
    try:
        return bool(re.match(pattern, s))
    except re.error as e:
        raise PolicyError(f"Invalid regex pattern: {e}", {"pattern": pattern})


def contains(s: str, substring: str) -> bool:
    """
    Check if string contains a substring.

    Args:
        s: String to search in
        substring: Substring to search for

    Returns:
        True if substring is found
    """
    return substring in s


# Collection helper functions
def len_of(x: Any) -> int:
    """
    Get length of a collection (list, dict, string, etc.).

    Args:
        x: Collection to get length of

    Returns:
        Length of the collection
    """
    try:
        return len(x)
    except TypeError:
        return 0


def has_keys(obj: Any, keys: List[str]) -> bool:
    """
    Check if dictionary has all specified keys.

    Args:
        obj: Object to check (should be dict)
        keys: List of keys to check for

    Returns:
        True if all keys are present
    """
    if not isinstance(obj, dict):
        return False
    return all(key in obj for key in keys)


def has_any_key(obj: Any, keys: List[str]) -> bool:
    """
    Check if dictionary has any of the specified keys.

    Args:
        obj: Object to check (should be dict)
        keys: List of keys to check for

    Returns:
        True if any key is present
    """
    if not isinstance(obj, dict):
        return False
    return any(key in obj for key in keys)


# Size estimation functions
def input_size_kb(args: tuple[Any, ...]) -> float:
    """
    Estimate the size of input arguments in kilobytes.

    Args:
        args: Tuple of arguments to estimate size for

    Returns:
        Estimated size in kilobytes
    """
    total_size = 0

    def estimate_size(obj: Any, visited: set[int] | None = None) -> int:
        """Recursively estimate object size."""
        if visited is None:
            visited = set()

        obj_id = id(obj)
        if obj_id in visited:
            return 0  # Avoid circular references

        visited.add(obj_id)

        try:
            if isinstance(obj, (int, float, bool)):
                return sys.getsizeof(obj)
            elif isinstance(obj, str):
                return sys.getsizeof(obj)
            elif isinstance(obj, (list, tuple)):
                size = sys.getsizeof(obj)
                for item in obj:
                    size += estimate_size(item, visited)
                return size
            elif isinstance(obj, dict):
                size = sys.getsizeof(obj)
                for key, value in obj.items():
                    size += estimate_size(key, visited)
                    size += estimate_size(value, visited)
                return size
            elif isinstance(obj, set):
                size = sys.getsizeof(obj)
                for item in obj:
                    size += estimate_size(item, visited)
                return size
            else:
                # For other types, use sys.getsizeof as approximation
                return sys.getsizeof(obj)
        except Exception:
            # If estimation fails, return a safe default
            return 1024  # 1KB default

    for arg in args:
        total_size += estimate_size(arg)

    return total_size / 1024.0  # Convert to KB


# Range checking functions
def in_range(x: Union[int, float], lo: Union[int, float], hi: Union[int, float]) -> bool:
    """
    Check if value is within a range (inclusive).

    Args:
        x: Value to check
        lo: Lower bound
        hi: Upper bound

    Returns:
        True if value is within range [lo, hi]
    """
    try:
        return lo <= x <= hi
    except TypeError:
        return False


def gt(x: Union[int, float], threshold: Union[int, float]) -> bool:
    """Check if value is greater than threshold."""
    try:
        return x > threshold
    except TypeError:
        return False


def lt(x: Union[int, float], threshold: Union[int, float]) -> bool:
    """Check if value is less than threshold."""
    try:
        return x < threshold
    except TypeError:
        return False


def eq(x: Any, value: Any) -> bool:
    """Check if value equals comparison value."""
    return x == value


def ne(x: Any, value: Any) -> bool:
    """Check if value does not equal comparison value."""
    return x != value


# Schema validation (placeholder for future implementation)
def schema_ok(args: tuple[Any, ...], schema_name: str) -> bool:
    """
    Validate arguments against a schema (placeholder implementation).

    Args:
        args: Arguments to validate
        schema_name: Name of schema to validate against

    Returns:
        True if validation passes (always returns True for now)
    """
    # TODO: Implement schema validation when schema definitions are available
    logger.debug(f"Schema validation requested for {schema_name} - not yet implemented")
    return True


# Policy evaluation function
def evaluate_policy(
    policy_rules: List[Dict[str, Any]],
    args: tuple[Any, ...],
    kwargs: Dict[str, Any]
) -> Literal['code', 'model', 'codegen']:
    """
    Evaluate policy rules to determine routing decision.

    Args:
        policy_rules: List of policy rule dictionaries
        args: Positional arguments from method call
        kwargs: Keyword arguments from method call

    Returns:
        Routing decision: 'code', 'model', or 'codegen'
    """
    # Create evaluation context with helper functions and arguments
    context = {
        'args': args,
        'kwargs': kwargs,
        # Helper functions
        'is_int': is_int,
        'is_float': is_float,
        'is_str': is_str,
        'is_list': is_list,
        'is_dict': is_dict,
        'is_bool': is_bool,
        'matches': matches,
        'contains': contains,
        'len_of': len_of,
        'has_keys': has_keys,
        'has_any_key': has_any_key,
        'input_size_kb': input_size_kb,
        'in_range': in_range,
        'gt': gt,
        'lt': lt,
        'eq': eq,
        'ne': ne,
        'schema_ok': schema_ok,
    }

    # Add individual arguments to context for easy access
    for i, arg in enumerate(args):
        context[f'a{i}'] = arg

    # Add keyword arguments to context
    context.update(kwargs)

    # Evaluate rules in order (first match wins)
    for rule in policy_rules:
        if not isinstance(rule, dict):
            logger.warning(f"Invalid policy rule format: {rule}")
            continue

        condition = rule.get('if')
        result = rule.get('then')

        if not condition or not result:
            logger.warning(f"Invalid policy rule structure: {rule}")
            continue

        if result not in ['code', 'model', 'codegen']:
            logger.warning(f"Invalid policy result: {result}")
            continue

        try:
            # Evaluate the condition
            if safe_eval(condition, context):
                logger.debug(f"Policy rule matched: {condition} -> {result}")
                return result

        except PolicyError as e:
            # Log error but continue to next rule
            logger.debug(f"Policy rule evaluation failed: {e}")
            continue

    # Default routing when no rules match
    logger.debug("No policy rules matched, using default routing: model")
    return 'model'


# Policy validation function
def validate_policy_rules(policy_rules: List[Dict[str, Any]]) -> List[str]:
    """
    Validate policy rules for syntax and structure.

    Args:
        policy_rules: List of policy rule dictionaries to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if not isinstance(policy_rules, list):
        errors.append("Policy rules must be a list")
        return errors

    for i, rule in enumerate(policy_rules):
        if not isinstance(rule, dict):
            errors.append(f"Rule {i} must be a dictionary")
            continue

        if 'if' not in rule:
            errors.append(f"Rule {i} missing 'if' condition")

        if 'then' not in rule:
            errors.append(f"Rule {i} missing 'then' result")

        if 'then' in rule:
            result = rule['then']
            if result not in ['code', 'model', 'codegen']:
                errors.append(f"Rule {i} has invalid result: {result}")

        if 'if' in rule:
            condition = rule['if']
            if not isinstance(condition, str):
                errors.append(f"Rule {i} condition must be a string")

            # Try to validate the expression syntax
            try:
                # Create a minimal context for syntax validation
                test_context = {
                    'args': (),
                    'kwargs': {},
                    'is_int': is_int,
                    'is_float': is_float,
                    'is_str': is_str,
                    'is_list': is_list,
                    'is_dict': is_dict,
                    'is_bool': is_bool,
                    'matches': matches,
                    'contains': contains,
                    'len_of': len_of,
                    'has_keys': has_keys,
                    'has_any_key': has_any_key,
                    'input_size_kb': input_size_kb,
                    'in_range': in_range,
                    'gt': gt,
                    'lt': lt,
                    'eq': eq,
                    'ne': ne,
                    'schema_ok': schema_ok,
                    'True': True,
                    'False': False,
                    'None': None,
                }

                # This will catch basic syntax errors
                safe_eval(condition, test_context)

            except PolicyError:
                # Expression errors are caught here
                pass  # We'll let the actual evaluation handle this
            except Exception as e:
                errors.append(f"Rule {i} has syntax error: {e}")

    return errors
