# Workstream 8: Sandbox Runner

## Overview
Implement the sandbox execution environment with resource limits and import allowlists to safely run generated and approved code artifacts.

## Context
The sandbox provides a restricted execution environment that prevents system access while allowing necessary computations. It enforces resource limits and capability restrictions to ensure safe execution of dynamically generated code.

## Deliverables

### Core Components
- `prompted_objects/sandbox/runner.py` - Complete implementation
- Restricted execution environment
- Resource limit enforcement (CPU, memory, recursion)
- Import allowlist management
- Deterministic execution guarantees
- Comprehensive test suite

### Interfaces
```python
def run_in_sandbox(
    artifact: dict[str, Any],
    fn: Callable,
    args: tuple[Any, ...],
    kwargs: dict[str, Any]
) -> Any:
    """Execute function in restricted sandbox environment."""
```

## Technical Specifications

### Resource Limits
- **CPU Time**: ≤ 500ms per execution
- **Memory**: ≤ 256 MB heap usage
- **Recursion**: ≤ 100 call depth
- **Threads**: Single-threaded execution only
- **System Calls**: Completely blocked

### Import Allowlist
Safe modules for computation:
- `math`, `cmath` - Mathematical functions
- `re` - Regular expressions
- `json` - JSON processing
- `itertools` - Iterator tools
- `functools` - Functional programming
- `operator` - Operator functions
- `collections` - Data structures
- `datetime`, `time` - Time handling (safe subset)
- `decimal` - Decimal arithmetic
- `fractions` - Rational numbers

### Execution Environment
- **Global Restrictions**: Limited builtins, no system access
- **Module Isolation**: Custom module loader
- **Timeout Protection**: Execution time limits
- **Memory Monitoring**: Heap usage tracking
- **Exception Handling**: Comprehensive error capture

### Safety Measures
- No filesystem access
- No network operations
- No subprocess creation
- No dynamic code execution
- Restricted reflection capabilities

## Development Setup

```bash
# Switch to workstream branch
git checkout feature/workstream-8-sandbox-runner

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/test_sandbox_runner.py -v --cov=prompted_objects.sandbox
```

## Implementation Plan

### Phase 1: Execution Infrastructure
1. Restricted globals setup
2. Custom import system
3. Basic execution harness

### Phase 2: Resource Management
1. CPU time monitoring
2. Memory usage tracking
3. Recursion depth limits
4. Timeout implementation

### Phase 3: Security Hardening
1. Builtin function restrictions
2. Module access control
3. System call blocking
4. Reflection limitations

### Phase 4: Error Handling
1. Execution exception capture
2. Resource limit violation handling
3. Timeout error management
4. Comprehensive error reporting

### Phase 5: Integration Testing
1. End-to-end sandbox execution
2. Performance benchmarking
3. Security validation
4. Edge case handling

## Success Criteria

### Functional Requirements
- [ ] Executes code in restricted environment
- [ ] Enforces all resource limits
- [ ] Allows only allowlisted imports
- [ ] Prevents system access completely
- [ ] Provides deterministic execution
- [ ] Handles errors gracefully

### Quality Requirements
- [ ] ≥90% test coverage
- [ ] Type hints on all functions
- [ ] Comprehensive docstrings
- [ ] Performance suitable for production use
- [ ] Clear security boundaries

### Integration Requirements
- [ ] Compatible with artifact store output
- [ ] Interface matches specification exactly
- [ ] Works with validation pipeline
- [ ] No breaking changes

## Testing Strategy

### Unit Tests
- Individual limit enforcement
- Import allowlist validation
- Execution environment isolation
- Error condition handling

### Integration Tests
- Full artifact execution workflows
- Resource limit testing
- Security boundary validation
- Performance benchmarking

### Security Tests
- Attempted escape detection
- Resource exhaustion prevention
- Import violation blocking
- System access prevention

## Examples

### Basic Sandbox Execution
```python
artifact = {"code": "return a + b", "capabilities": {"imports": []}}

result = run_in_sandbox(artifact, add_function, (2, 3), {})
# Expected: 5
```

### With Allowlisted Imports
```python
artifact = {
    "code": "import math\nreturn math.sqrt(x)",
    "capabilities": {"imports": ["math"]}
}

result = run_in_sandbox(artifact, sqrt_function, (), {"x": 4})
# Expected: 2.0
```

### Resource Limit Enforcement
```python
# This should timeout
malicious_code = """
while True:
    pass  # Infinite loop
"""

try:
    result = run_in_sandbox({"code": malicious_code}, fn, args, kwargs)
except SandboxError as e:
    assert "timeout" in str(e)
```

### Import Violation
```python
# This should fail
unsafe_code = """
import os  # Not allowlisted
return os.getcwd()
"""

try:
    result = run_in_sandbox({"code": unsafe_code}, fn, args, kwargs)
except SandboxError as e:
    assert "import" in str(e)
```

## Dependencies & Blockers
- **Blocks**: None directly
- **Blocked by**: None
- **Parallel workstreams**: Can work alongside all other workstreams

## Files to Create/Modify
- `prompted_objects/sandbox/runner.py` (create)
- `tests/test_sandbox_runner.py` (create)

## Acceptance Tests
Run these commands to verify completion:

```bash
# All tests pass
pytest tests/test_sandbox_runner.py

# Coverage meets requirements
pytest --cov=prompted_objects.sandbox --cov-report=term-missing

# Type checking passes
mypy prompted_objects/sandbox/runner.py

# Manual security testing
python -c "
from prompted_objects.sandbox import run_in_sandbox
# Test basic execution and limits
"
```

## Next Steps
1. Claim this workstream by updating `AGENT_COORDINATION.md`
2. Switch to feature branch: `git checkout -b feature/workstream-8-sandbox-runner`
3. Implement sandbox logic following the plan above
4. Submit PR when complete with comprehensive tests

## Questions & Support
- Reference `requirements.md` section 2.3 for sandbox specifications
- Use Python's resource module for limit enforcement
- Implement custom importlib hooks for module control
- Focus on defense-in-depth security approach
