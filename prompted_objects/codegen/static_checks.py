"""Static analysis and validation for generated code."""

import ast
from typing import Any, Dict, List, Set

from prompted_objects.exceptions import ValidationError


# Forbidden builtin functions that pose security risks
FORBIDDEN_BUILTINS = {
    'eval', 'exec', 'compile', 'open', 'globals', 'locals',
    'input', 'print', 'exit', 'quit', '__import__'
}

# Dangerous modules that should be restricted
DANGEROUS_MODULES = {
    'os', 'sys', 'subprocess', 'socket', 'urllib', 'http',
    'ftplib', 'telnetlib', 'smtplib', 'imaplib', 'poplib'
}

# Safe modules that are allowed for computation
SAFE_MODULES = {
    'math', 'cmath', 're', 'itertools', 'functools', 'operator',
    'collections', 'datetime', 'time', 'decimal', 'fractions'
}


class ASTValidator(ast.NodeVisitor):
    """AST visitor that validates code safety and capability compliance."""

    def __init__(self, capabilities: Dict[str, Any] | None = None) -> None:
        self.capabilities = capabilities or {}
        self.errors: List[str] = []
        self.allowed_imports: Set[str] = set(self.capabilities.get('imports', []))
        self.io_allowed = self.capabilities.get('io', False)
        self.network_allowed = self.capabilities.get('network', False)
        self.imported_modules: Set[str] = set()

        # Extend allowed imports with safe modules
        self.allowed_imports.update(SAFE_MODULES)

    def visit_Call(self, node: ast.Call) -> None:
        """Check function calls for forbidden builtins and dangerous operations."""
        # Check for direct builtin calls
        if isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_BUILTINS:
                self.errors.append(f"Forbidden builtin function: {node.func.id}")

        # Check for attribute calls (e.g., os.system, subprocess.call)
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                module_name = node.func.value.id
                func_name = node.func.attr

                # Check dangerous module usage
                if module_name in DANGEROUS_MODULES:
                    if module_name == 'os' and not self.io_allowed:
                        self.errors.append(f"OS operation not allowed: os.{func_name}")
                    elif module_name == 'subprocess' and not self.io_allowed:
                        self.errors.append(f"Subprocess operation not allowed: subprocess.{func_name}")
                    elif module_name in {'socket', 'urllib', 'http'} and not self.network_allowed:
                        self.errors.append(f"Network operation not allowed: {module_name}.{func_name}")
                    # Note: If io=True or network=True, these operations are allowed

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        """Check import statements."""
        for alias in node.names:
            module_name = alias.name
            self.imported_modules.add(module_name)
            if module_name not in self.allowed_imports:
                self.errors.append(f"Import not allowed: {module_name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Check from import statements."""
        if node.module:
            self.imported_modules.add(node.module)
            if node.module not in self.allowed_imports:
                self.errors.append(f"Import not allowed: {node.module}")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Check function definitions for complexity."""
        # Count AST nodes for complexity check
        node_count = count_ast_nodes(node)
        if node_count > 1000:  # Configurable limit
            self.errors.append(f"Function too complex: {node_count} AST nodes (max 1000)")

        # Check nesting depth
        max_depth = get_max_nesting_depth(node)
        if max_depth > 10:  # Configurable limit
            self.errors.append(f"Function nesting too deep: {max_depth} levels (max 10)")

        self.generic_visit(node)

    def visit_Module(self, node: ast.Module) -> None:
        """Check module-level code for complexity."""
        # Also check top-level code complexity
        node_count = count_ast_nodes(node)
        if node_count > 2000:  # Higher limit for module-level code
            self.errors.append(f"Code too complex: {node_count} AST nodes (max 2000)")

        # Check nesting depth at module level
        max_depth = get_max_nesting_depth(node)
        if max_depth > 15:  # Higher limit for module-level
            self.errors.append(f"Code nesting too deep: {max_depth} levels (max 15)")

        self.generic_visit(node)


def count_ast_nodes(node: ast.AST) -> int:
    """Count total AST nodes in a subtree."""
    count = 1
    for child in ast.iter_child_nodes(node):
        count += count_ast_nodes(child)
    return count


def get_max_nesting_depth(node: ast.AST, current_depth: int = 0) -> int:
    """Calculate maximum nesting depth in a function."""
    max_depth = current_depth

    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            max_depth = max(max_depth, get_max_nesting_depth(child, current_depth + 1))
        else:
            max_depth = max(max_depth, get_max_nesting_depth(child, current_depth))

    return max_depth


def validate_ast(
    body_src: str,
    capabilities: Dict[str, Any] | None = None
) -> None:
    """
    Validate function body source code for safety and capability compliance.

    Args:
        body_src: Python function body as string
        capabilities: Dict of allowed capabilities (io, network, imports, etc.)

    Raises:
        ValidationError: If code fails validation with detailed error messages
    """
    try:
        # Parse the source code to AST
        tree = ast.parse(body_src, mode='exec')
    except SyntaxError as e:
        raise ValidationError(
            f"Syntax error in generated code: {e.msg}",
            {"line": e.lineno, "offset": e.offset, "text": e.text}
        )

    # Create validator and visit all nodes
    validator = ASTValidator(capabilities)
    validator.visit(tree)

    # Raise ValidationError if any issues found
    if validator.errors:
        raise ValidationError(
            f"Code validation failed: {len(validator.errors)} issue(s) found",
            {"errors": validator.errors, "capabilities": capabilities}
        )
