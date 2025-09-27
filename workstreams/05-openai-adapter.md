# Workstream 5: OpenAI Adapter

## Overview
Implement the OpenAI adapter that provides normalized request/response handling for OpenAI-compatible APIs, including Azure OpenAI and standard OpenAI endpoints.

## Context
The adapter layer abstracts LLM provider specifics, providing a consistent interface for model interactions. This enables the router to work with different providers while maintaining uniform request/response handling, retries, and error normalization.

## Deliverables

### Core Components
- `prompted_objects/adapters/openai_adapter.py` - Complete implementation
- `prompted_objects/adapters/base.py` - Base adapter interface
- Provider-specific request construction
- Response normalization and parsing
- Retry logic with exponential backoff
- Error handling and classification
- Comprehensive test suite

### Interfaces
```python
class OpenAIAdapter(BaseAdapter):
    def call_method(
        self,
        prompt: str,
        metadata: dict[str, Any],
        args: dict[str, Any],
        context: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute method call via OpenAI API."""
```

## Technical Specifications

### Message Construction
The adapter constructs OpenAI chat completions with:

- **System Message**: Role prompt template (METHOD or CLASS)
- **User Message**: PROMPT text with templated arguments
- **Context JSON**: Structured args, examples, schema, parse mode

### Role Prompts
- **METHOD role**: Model acts as pure function implementation
- **CLASS role**: Model provides planning/artifacts for methods

### Request Parameters
- Temperature: 0 (deterministic)
- Top-p: 1 (full probability distribution)
- Max tokens: From budget or default
- Model: From configuration or default

### Response Handling
- Parse JSON responses when parse="json"
- Handle freeform responses when parse="freeform"
- Auto-detect format when parse="auto"
- Validate against Pydantic schemas when available

## Development Setup

```bash
# Switch to workstream branch
git checkout feature/workstream-5-openai-adapter

# Install dependencies
pip install -e ".[dev]"

# Set up API credentials (from api_credentials.yaml)
export AZURE_OPENAI_API_KEY="..."
export AZURE_OPENAI_ENDPOINT="..."

# Run tests
pytest tests/test_openai_adapter.py -v --cov=prompted_objects.adapters
```

## Implementation Plan

### Phase 1: Base Infrastructure
1. Create BaseAdapter abstract class
2. Set up OpenAI client configuration
3. Implement basic request/response structure

### Phase 2: Message Construction
1. System prompt templating
2. User message construction with args/context
3. Context JSON serialization
4. Template variable substitution

### Phase 3: API Integration
1. OpenAI client setup and configuration
2. Request execution with proper parameters
3. Response parsing and validation
4. Error handling and normalization

### Phase 4: Advanced Features
1. Retry logic with exponential backoff
2. Rate limiting and quota handling
3. Cost tracking and reporting
4. Streaming response support (future)

### Phase 5: Provider Support
1. Azure OpenAI integration
2. Standard OpenAI API support
3. Configuration validation
4. Provider-specific optimizations

## Success Criteria

### Functional Requirements
- [ ] Constructs proper OpenAI chat messages
- [ ] Handles METHOD and CLASS role prompts
- [ ] Parses responses according to parse mode
- [ ] Implements retry logic with backoff
- [ ] Normalizes errors across providers
- [ ] Tracks token usage and costs

### Quality Requirements
- [ ] ≥90% test coverage (with mocked API calls)
- [ ] Type hints on all functions
- [ ] Comprehensive docstrings
- [ ] Performance suitable for production use
- [ ] Clear error messages and logging

### Integration Requirements
- [ ] Compatible with Router expectations
- [ ] Interface matches specification exactly
- [ ] Works with existing configuration
- [ ] No breaking changes

## Testing Strategy

### Unit Tests (Mocked)
- Message construction correctness
- Parameter handling
- Response parsing logic
- Error classification
- Retry behavior

### Integration Tests
- Real API calls (with caution for rate limits)
- End-to-end method execution
- Error scenario handling
- Cost and token tracking

### Provider Tests
- Azure OpenAI compatibility
- Standard OpenAI API compatibility
- Configuration validation

## Examples

### Basic Method Call
```python
adapter = OpenAIAdapter()

result = adapter.call_method(
    prompt="Return the sum of a and b.",
    metadata={"parse": "auto", "strict": False},
    args={"a": 2, "b": 3},
    context={"return_schema": int}
)

# Expected: {"result": 5} or similar structured response
```

### With Examples Context
```python
result = adapter.call_method(
    prompt="Add two numbers.",
    metadata={"parse": "json"},
    args={"x": 10, "y": 20},
    context={
        "examples": [
            {"input": {"x": 1, "y": 2}, "output": 3}
        ],
        "return_schema": int
    }
)
```

### Error Handling
```python
try:
    result = adapter.call_method(...)
except AdapterError as e:
    # Normalized error with type, reason, details
    print(f"API Error: {e.type} - {e.reason}")
```

## Dependencies & Blockers
- **Blocks**: Workstream 4 (Router Core), Workstream 6 (Codegen Engine)
- **Blocked by**: None
- **Parallel workstreams**: Can work alongside most other workstreams

## Files to Create/Modify
- `prompted_objects/adapters/base.py` (create)
- `prompted_objects/adapters/openai_adapter.py` (create)
- `tests/test_openai_adapter.py` (create)

## Acceptance Tests
Run these commands to verify completion:

```bash
# All tests pass (mocked)
pytest tests/test_openai_adapter.py

# Coverage meets requirements
pytest --cov=prompted_objects.adapters --cov-report=term-missing

# Type checking passes
mypy prompted_objects/adapters/

# Manual integration test (requires API key)
python -c "
from prompted_objects.adapters import OpenAIAdapter
adapter = OpenAIAdapter()
# Test basic functionality
"
```

## Configuration
The adapter uses configuration from:

```yaml
# api_credentials.yaml (DO NOT COMMIT)
azure_openai:
  api_key: "..."
  endpoint: "..."
  deployment_name: "gpt-5-chat"
  api_version: "2025-01-01-preview"
```

## Next Steps
1. Claim this workstream by updating `AGENT_COORDINATION.md`
2. Switch to feature branch: `git checkout -b feature/workstream-5-openai-adapter`
3. Implement adapter following the plan above
4. Submit PR when complete with comprehensive tests

## Questions & Support
- Reference `requirements.md` section 2.2 for adapter specifications
- Check `api_credentials.yaml` for configuration format
- Use OpenAI Python SDK for API interactions
- Coordinate with Router agent for interface requirements
