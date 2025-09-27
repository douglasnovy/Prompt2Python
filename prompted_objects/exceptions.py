"""Public exceptions for the Prompted Objects library."""

from typing import Any, Dict


class PromptedObjectsError(Exception):
    """Base exception for all Prompted Objects errors."""

    def __init__(self, message: str, details: Dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


class RoutingError(PromptedObjectsError):
    """Raised when routing decisions fail."""


class PolicyError(PromptedObjectsError):
    """Raised when policy evaluation fails."""


class CodegenError(PromptedObjectsError):
    """Raised when code generation fails."""


class SandboxError(PromptedObjectsError):
    """Raised when sandbox execution fails."""


class ArtifactError(PromptedObjectsError):
    """Raised when artifact operations fail."""


class BudgetExceededError(PromptedObjectsError):
    """Raised when resource budgets are exceeded."""


class ValidationError(PromptedObjectsError):
    """Raised when validation fails."""

    def __str__(self) -> str:
        """Include error details in string representation."""
        if self.details and 'errors' in self.details:
            errors = self.details['errors']
            if isinstance(errors, list):
                return f"{self.message}\n" + "\n".join(f"- {error}" for error in errors)
        return super().__str__()