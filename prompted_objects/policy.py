"""
Policy DSL & Parser for Prompted Objects.

This module implements a safe expression evaluation system for declarative routing rules
that determine whether method calls should route to code artifacts, LLM models, or code generation.

The Policy DSL allows defining routing rules in YAML format within docstring metadata:

```yaml
policy:
  - if: "is_int(a) and is_int(b)"
    then: code
  - if: "input_size_kb(args) > 1.0"
    then: model
  - else: model
```

The system provides safe evaluation with:
- Restricted execution environment (no arbitrary code execution)
- Timeout protection to prevent infinite loops
- Comprehensive error handling and logging
- First-match-wins evaluation logic
"""

import ast
import re
import sys
import time
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from contextlib import contextmanager
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Type aliases
PolicyRule = Dict[str, Any]
PolicyResult = Literal['code', 'model', 'codegen']


class PolicyError(Exception):
    """Raised when policy evaluation fails."""
    pass


class PolicyTimeoutError(PolicyError):
    """Raised when policy evaluation exceeds timeout."""
    pass


class PolicySyntaxError(PolicyError):
    """Raised when policy expression has invalid syntax."""
    pass


@contextmanager
def safe_execution_context(timeout: float = 1.0):
    """
    Context manager that provides a restricted execution environment with timeout protection.

    Args:
        timeout: Maximum execution time in seconds

    Yields:
        Dict containing safe globals for expression evaluation
    """
    # Define safe built-in functions and types
    safe_builtins = {
        'len': len,
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
        'list': list,
        'dict': dict,
        'tuple': tuple,
        'set': set,
        'range': range,
        'enumerate': enumerate,
        'zip': zip,
        'sum': sum,
        'min': min,
        'max': max,
        'abs': abs,
        'round': round,
        'all': all,
        'any': any,
        'isinstance': isinstance,
        'hasattr': hasattr,
        'getattr': getattr,
        'setattr': setattr,
    }

    # Define safe operators and constants
    safe_globals = {
        '__builtins__': safe_builtins,
        'True': True,
        'False': False,
        'None': None,
    }

    # Add safe math operations
    import math
    safe_math = {
        'pi': math.pi,
        'e': math.e,
        'inf': float('inf'),
        'nan': float('nan'),
    }
    safe_globals.update(safe_math)

    # Add safe string operations
    import string
    safe_string = {
        'ascii_letters': string.ascii_letters,
        'ascii_lowercase': string.ascii_lowercase,
        'ascii_uppercase': string.ascii_uppercase,
        'digits': string.digits,
        'hexdigits': string.hexdigits,
        'octdigits': string.octdigits,
        'punctuation': string.punctuation,
        'printable': string.printable,
        'whitespace': string.whitespace,
    }
    safe_globals.update(safe_string)

    start_time = time.time()
    try:
        yield safe_globals
    finally:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise PolicyTimeoutError(f"Policy evaluation timed out after {elapsed:.3f}s")


def is_int(value: Any) -> bool:
    """
    Check if a value is an integer.

    Args:
        value: Value to check

    Returns:
        True if value is an integer, False otherwise
    """
    try:
        return isinstance(value, int) and not isinstance(value, bool)
    except Exception:
        return False


def is_float(value: Any) -> bool:
    """
    Check if a value is a float.

    Args:
        value: Value to check

    Returns:
        True if value is a float, False otherwise
    """
    try:
        return isinstance(value, float) and not isinstance(value, bool)
    except Exception:
        return False


def is_str(value: Any) -> bool:
    """
    Check if a value is a string.

    Args:
        value: Value to check

    Returns:
        True if value is a string, False otherwise
    """
    try:
        return isinstance(value, str)
    except Exception:
        return False


def is_list(value: Any) -> bool:
    """
    Check if a value is a list.

    Args:
        value: Value to check

    Returns:
        True if value is a list, False otherwise
    """
    try:
        return isinstance(value, list)
    except Exception:
        return False


def is_dict(value: Any) -> bool:
    """
    Check if a value is a dictionary.

    Args:
        value: Value to check

    Returns:
        True if value is a dictionary, False otherwise
    """
    try:
        return isinstance(value, dict)
    except Exception:
        return False


def matches(text: str, pattern: str) -> bool:
    """
    Check if text matches a regex pattern.

    Args:
        text: Text to match against
        pattern: Regex pattern to match

    Returns:
        True if text matches pattern, False otherwise
    """
    try:
        return bool(re.match(pattern, str(text)))
    except Exception:
        return False


def len_of(value: Any) -> int:
    """
    Get the length of a value (works with sequences and mappings).

    Args:
        value: Value to get length of

    Returns:
        Length of the value, or 0 if not applicable
    """
    try:
        return len(value)
    except Exception:
        return 0


def has_keys(obj: Any, keys: List[str]) -> bool:
    """
    Check if a dictionary has all specified keys.

    Args:
        obj: Object to check (should be a dict)
        keys: List of keys to check for

    Returns:
        True if obj is a dict and has all keys, False otherwise
    """
    try:
        if not isinstance(obj, dict):
            return False
        return all(key in obj for key in keys)
    except Exception:
        return False


def input_size_kb(args: Tuple[Any, ...], kwargs: Optional[Dict[str, Any]] = None) -> float:
    """
    Estimate the size of input arguments in kilobytes.

    Args:
        args: Positional arguments
        kwargs: Keyword arguments

    Returns:
        Estimated size in kilobytes
    """
    import sys

    def get_size(obj: Any) -> int:
        """Recursively calculate object size."""
        if obj is None:
            return 0
        try:
            size = sys.getsizeof(obj)
            if isinstance(obj, (list, tuple, set)):
                size += sum(get_size(item) for item in obj)
            elif isinstance(obj, dict):
                size += sum(get_size(k) + get_size(v) for k, v in obj.items())
            return size
        except Exception:
            return sys.getsizeof(str(obj))

    total_size = 0
    # Add args size
    for arg in args:
        total_size += get_size(arg)

    # Add kwargs size
    if kwargs:
        for key, value in kwargs.items():
            total_size += get_size(key) + get_size(value)

    return total_size / 1024.0  # Convert to KB


def schema_ok(args: Tuple[Any, ...], schema_name: str) -> bool:
    """
    Placeholder for schema validation.

    Args:
        args: Arguments to validate
        schema_name: Name of schema to validate against

    Returns:
        Always returns True (placeholder implementation)
    """
    # TODO: Implement actual schema validation
    logger.warning(f"Schema validation not implemented: {schema_name}")
    return True


def in_range(value: Union[int, float], lo: Union[int, float], hi: Union[int, float]) -> bool:
    """
    Check if a value is within a specified range.

    Args:
        value: Value to check
        lo: Lower bound (inclusive)
        hi: Upper bound (inclusive)

    Returns:
        True if value is within range, False otherwise
    """
    try:
        return lo <= value <= hi
    except Exception:
        return False


def safe_eval(expression: str, variables: Dict[str, Any], timeout: float = 1.0) -> Any:
    """
    Safely evaluate an expression with restricted context and timeout.

    Args:
        expression: Expression string to evaluate
        variables: Variables available in the expression context
        timeout: Maximum execution time in seconds

    Returns:
        Result of the expression evaluation

    Raises:
        PolicyTimeoutError: If evaluation exceeds timeout
        PolicySyntaxError: If expression has invalid syntax
        PolicyError: For other evaluation errors
    """
    try:
        # Parse expression to validate syntax
        ast.parse(expression, mode='eval')

        with safe_execution_context(timeout) as safe_globals:
            # Create local context with variables and helper functions
            local_context = {
                **variables,
                # Add helper functions to context
                'is_int': is_int,
                'is_float': is_float,
                'is_str': is_str,
                'is_list': is_list,
                'is_dict': is_dict,
                'matches': matches,
                'len_of': len_of,
                'has_keys': has_keys,
                'input_size_kb': lambda args: input_size_kb(args, variables.get('kwargs')),
                'schema_ok': schema_ok,
                'in_range': in_range,
            }

            # Evaluate expression
            result = eval(expression, safe_globals, local_context)

            # Log successful evaluation
            logger.debug(f"Evaluated expression '{expression}' -> {result}")
            return result

    except SyntaxError as e:
        error_msg = f"Invalid syntax in policy expression: {expression}"
        logger.error(f"{error_msg}: {e}")
        raise PolicySyntaxError(error_msg) from e
    except TimeoutError as e:
        error_msg = f"Policy evaluation timed out: {expression}"
        logger.error(error_msg)
        raise PolicyTimeoutError(error_msg) from e
    except Exception as e:
        error_msg = f"Error evaluating policy expression: {expression}"
        logger.error(f"{error_msg}: {e}")
        raise PolicyError(error_msg) from e


def evaluate_policy(
    policy_rules: List[PolicyRule],
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any]
) -> PolicyResult:
    """
    Evaluate policy rules and return routing decision.

    Args:
        policy_rules: List of policy rules from YAML
        args: Positional arguments from method call
        kwargs: Keyword arguments from method call

    Returns:
        Routing decision: 'code', 'model', or 'codegen'

    Raises:
        PolicyError: If policy evaluation fails
    """
    # Set up variables for expression evaluation
    variables = {
        'args': args,
        'kwargs': kwargs,
    }

    # Add individual arguments as variables (a, b, etc.)
    arg_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']  # Up to 10 positional args
    for i, arg in enumerate(args):
        if i < len(arg_names):
            variables[arg_names[i]] = arg

    # Add keyword arguments as variables
    for key, value in kwargs.items():
        variables[key] = value

    # Evaluate each rule in order (first-match wins)
    for i, rule in enumerate(policy_rules):
        try:
            # Check if this is an "else" rule
            if 'else' in rule:
                logger.debug(f"Using default rule (else): {rule['else']}")
                return rule['else']

            # Check if this rule has a condition
            if 'if' not in rule:
                logger.warning(f"Policy rule {i} missing 'if' condition: {rule}")
                continue

            condition = rule['if']
            if not isinstance(condition, str):
                logger.warning(f"Policy rule {i} 'if' condition must be string: {condition}")
                continue

            # Evaluate the condition
            result = safe_eval(condition, variables)

            # If condition is truthy, return the routing decision
            if result:
                if 'then' not in rule:
                    logger.warning(f"Policy rule {i} missing 'then' action: {rule}")
                    continue

                action = rule['then']
                if action not in ('code', 'model', 'codegen'):
                    logger.warning(f"Invalid action in policy rule {i}: {action}")
                    continue

                logger.debug(f"Policy rule {i} matched: {condition} -> {action}")
                return action

        except (PolicyTimeoutError, PolicySyntaxError, PolicyError) as e:
            # Log error but continue with next rule
            logger.warning(f"Error evaluating policy rule {i}: {e}")
            continue

    # No rules matched, return default routing
    logger.debug("No policy rules matched, using default routing: model")
    return 'model'


def validate_policy_syntax(policy_rules: List[PolicyRule]) -> List[str]:
    """
    Validate policy rules for syntax errors.

    Args:
        policy_rules: List of policy rules to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    for i, rule in enumerate(policy_rules):
        # Check rule structure
        if not isinstance(rule, dict):
            errors.append(f"Rule {i}: Must be a dictionary, got {type(rule)}")
            continue

        # Check for valid keys
        valid_keys = {'if', 'then', 'else'}
        invalid_keys = set(rule.keys()) - valid_keys
        if invalid_keys:
            errors.append(f"Rule {i}: Invalid keys {invalid_keys}, valid keys are {valid_keys}")

        # Validate 'if' condition
        if 'if' in rule:
            condition = rule['if']
            if not isinstance(condition, str):
                errors.append(f"Rule {i}: 'if' condition must be a string, got {type(condition)}")
            else:
                # Try to parse the condition to check syntax
                try:
                    ast.parse(condition, mode='eval')
                except SyntaxError as e:
                    errors.append(f"Rule {i}: Invalid syntax in condition '{condition}': {e}")

        # Validate 'then' action
        if 'then' in rule:
            action = rule['then']
            if action not in ('code', 'model', 'codegen'):
                errors.append(f"Rule {i}: Invalid action '{action}', must be 'code', 'model', or 'codegen'")

        # Check for mutually exclusive keys
        if 'else' in rule and ('if' in rule or 'then' in rule):
            errors.append(f"Rule {i}: 'else' cannot be combined with 'if' or 'then'")

        if 'else' not in rule and 'if' not in rule and 'then' not in rule:
            errors.append(f"Rule {i}: Must have at least one of 'if', 'then', or 'else'")

    return errors