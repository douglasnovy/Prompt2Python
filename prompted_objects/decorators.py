"""
Decorator module for Prompted Objects.

This module provides the @llm decorator and related functionality.
Currently a stub implementation for testing purposes.
"""

from typing import Any, Callable, Dict, Optional


def llm(
    role: str = "method",
    model: str = "gpt-4o-mini",
    allow_hot_codegen: bool = True,
    **kwargs: Any
) -> Callable:
    """
    Decorator for LLM-powered methods.

    This is a stub implementation for testing purposes.
    The full implementation will be provided in workstream 3.

    Args:
        role: The role of this method (e.g., "method", "class")
        model: The default LLM model to use
        allow_hot_codegen: Whether to allow hot code generation
        **kwargs: Additional configuration options

    Returns:
        The decorated function
    """
    def decorator(func: Callable) -> Callable:
        # Store metadata on the function for later use
        func._llm_config = {
            "role": role,
            "model": model,
            "allow_hot_codegen": allow_hot_codegen,
            **kwargs
        }
        return func
    return decorator


__all__ = ["llm"]