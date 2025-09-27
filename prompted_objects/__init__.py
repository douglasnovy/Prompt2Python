"""
Prompted Objects - Docstring-driven LLM orchestration library.

This library enables developers to write natural-language PROMPTs in docstrings
and have a runtime that routes method calls between LLM models and vetted code artifacts.
"""

__version__ = "0.1.0"
__all__ = ["llm", "parse_docstring", "DocstringParseResult", "evaluate_policy"]

# Import decorators if available, otherwise create a stub
try:
    from .decorators import llm
except ImportError:
    # Stub for when decorators module doesn't exist yet
    def llm(*args, **kwargs):
        """Stub decorator - to be implemented in workstream 3."""
        def decorator(func):
            return func
        return decorator

from .docstring_parser import parse_docstring, DocstringParseResult
from .policy import evaluate_policy
