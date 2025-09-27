# Workstream 1: Policy DSL & Parser

## Overview
Implement the Policy DSL & Parser component that evaluates declarative routing rules to determine whether method calls should route to code artifacts, LLM models, or code generation.

## Context
The Prompted Objects library enables docstring-driven LLM orchestration. The Policy DSL is the foundation that determines routing decisions based on method arguments, types, and other conditions. This workstream has **zero dependencies** and can be developed completely independently.

## Deliverables

### Core Components
- `prompted_objects/policy.py` - Complete implementation
- Expression parser with safe evaluation
- Helper functions for policy predicates
- Policy linter for validation
- First-match evaluator for routing decisions
- Comprehensive test suite

### Interfaces
```python
def evaluate_policy(
    policy_rules: List[Dict[str, Any]],
    args: tuple[Any, ...],
    kwargs: dict[str, Any]
) -> Literal['code','model','codegen']
```

## Technical Specifications

### Policy DSL Syntax
Policies are defined in YAML within the `METADATA.policy` section of docstrings:

```yaml
policy:
  - if: "is_int(a) and is_int(b)"
    then: code
  - if: "input_size_kb(args) > 1.0"
    then: model
  - else: model
```

### Required Helper Functions
Implement these predicate functions for use in policy expressions:

- `is_int(x)`, `is_float(x)`, `is_str(x)`, `is_list(x)`, `is_dict(x)`
- `matches(s, pattern)` - regex matching
- `len_of(x)` - length of sequences/mappings
- `has_keys(obj, [..])` - dict key checking
- `input_size_kb(args)` - size estimation
- `schema_ok(args, "SchemaName")` - schema validation (placeholder for now)
- `in_range(x, lo, hi)` - range checking

### Safety Requirements
- **No arbitrary code execution** - expressions must be safely evaluable
- **Restricted evaluation context** - only allowlisted functions and operations
- **Timeout protection** - prevent infinite loops or excessive computation
- **Error handling** - unknown errors treated as non-match with logging

### Evaluation Logic
- **First-match wins**: Evaluate rules in order, return result of first matching condition
- **Default route**: "model" when no rules match
- **Error behavior**: Policy evaluation errors treated as non-match, logged with fingerprint

## Development Setup

```bash
# Switch to workstream branch
git checkout feature/workstream-1-policy-dsl

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/test_policy.py -v --cov=prompted_objects.policy
```

## Implementation Plan

### Phase 1: Core Infrastructure
1. Set up safe evaluation environment (restricted globals, timeout)
2. Implement helper functions
3. Create basic expression evaluator

### Phase 2: Policy Engine
1. Parse YAML policy rules
2. Implement first-match evaluation logic
3. Add comprehensive error handling

### Phase 3: Validation & Linting
1. Policy rule validation
2. Expression syntax checking
3. Performance monitoring

### Phase 4: Testing
1. Unit tests for all helper functions
2. Integration tests for policy evaluation
3. Edge cases and error conditions
4. Performance benchmarks

## Success Criteria

### Functional Requirements
- [ ] All helper functions work correctly with various input types
- [ ] Policy evaluation follows first-match-wins logic
- [ ] Safe execution prevents code injection attacks
- [ ] Default routing to "model" when no rules match
- [ ] Proper error handling and logging

### Quality Requirements
- [ ] ≥90% test coverage
- [ ] Type hints on all functions
- [ ] Comprehensive docstrings
- [ ] No security vulnerabilities
- [ ] Performance suitable for runtime evaluation

### Integration Requirements
- [ ] Interface matches specification exactly
- [ ] Compatible with existing stub implementations
- [ ] No breaking changes to other components

## Testing Strategy

### Unit Tests
- Helper function behavior with valid/invalid inputs
- Expression evaluation with various data types
- Error conditions and exception handling

### Integration Tests
- Full policy evaluation workflows
- YAML parsing and rule processing
- Performance under load

### Security Tests
- Code injection attempts blocked
- Timeout enforcement
- Memory usage limits

## Examples

### Basic Type Checking
```python
policy = [{"if": "is_int(a) and is_int(b)", "then": "code"}]
result = evaluate_policy(policy, (2, 3), {})
assert result == "code"
```

### Regex Matching
```python
policy = [{"if": "matches(name, r'^test_')", "then": "model"}]
result = evaluate_policy(policy, (), {"name": "test_function"})
assert result == "model"
```

### Size-Based Routing
```python
policy = [{"if": "input_size_kb(args) > 1.0", "then": "model"}]
result = evaluate_policy(policy, (large_object,), {})
assert result == "model"
```

## Dependencies & Blockers
- **Blocks**: Workstream 4 (Router Core)
- **Blocked by**: None
- **Parallel workstreams**: Can work alongside all other workstreams

## Files to Modify
- `prompted_objects/policy.py` (extend existing stub)
- `tests/test_policy.py` (create comprehensive tests)

## Acceptance Tests
Run these commands to verify completion:

```bash
# All tests pass
pytest tests/test_policy.py

# Coverage meets requirements
pytest --cov=prompted_objects.policy --cov-report=term-missing

# Type checking passes
mypy prompted_objects/policy.py

# Security audit (manual)
# - No eval() or exec() usage
# - Restricted execution environment
# - Timeout protection implemented
```

## Next Steps
1. Claim this workstream by updating `AGENT_COORDINATION.md`
2. Switch to feature branch: `git checkout -b feature/workstream-1-policy-dsl`
3. Implement core functionality following the plan above
4. Submit PR when complete with comprehensive tests

## Questions & Support
- Reference `requirements.md` section 3 for Policy DSL details
- Check `AGENT_COORDINATION.md` for coordination updates
- Use existing code patterns from other modules
- Ping other agents for integration questions
