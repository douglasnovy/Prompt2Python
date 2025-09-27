"""
Prompted Objects - Docstring-driven LLM orchestration library.

This library enables developers to write natural-language PROMPTs in docstrings
and have a runtime that routes method calls between LLM models and vetted code artifacts.
"""

__version__ = "0.1.0"
__all__ = ["llm"]

from .decorators import llm
