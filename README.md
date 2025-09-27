# Prompt2Python

A Python library for docstring-driven, object-oriented LLM orchestration that automatically routes between model calls and vetted code artifacts.

## Overview

**Prompt2Python** enables natural language programming through the `@llm` decorator, allowing developers to write functions with docstrings that describe their behavior instead of implementing them directly. The library intelligently routes between:

- **LLM calls** for natural language tasks
- **Pre-vetted code artifacts** for deterministic operations
- **Safe code generation** with sandboxing and validation

## Key Features

- **Docstring-Driven Development**: Write functions with descriptive docstrings instead of implementation
- **Intelligent Routing**: Policy-based routing between LLM calls and code execution
- **Safety First**: Sandboxed execution environment with static code validation
- **Artifact Management**: Versioned storage and lifecycle management of generated code
- **Observability**: Comprehensive telemetry and logging for debugging and monitoring
- **CLI Tooling**: Command-line interface for project management and debugging

## Architecture

The library is organized into 14 independent workstreams that can be developed in parallel:

### Phase 1: Foundation (Parallel Development)
- **Policy DSL & Parser** - Core routing logic foundation
- **Docstring Parser** - Metadata extraction from function docstrings
- **OpenAI Adapter** - LLM provider interface
- **Static Checks** - Code safety validation
- **Sandbox Runner** - Safe execution environment
- **Artifact Store** - Code artifact management
- **Telemetry/Logging** - Observability system
- **Role Prompt Templates** - System message templates

### Phase 2: Integration
- **Decorator Wrapper** - `@llm` decorator implementation
- **Codegen Engine** - Dynamic code generation
- **Router Core** - Main orchestration logic
- **Auto-Tests** - Automated testing framework
- **Spec Loader** - Specification loading and parsing

### Phase 3: Advanced Features
- **CLI Tooling** - Command-line interface

## Installation

```bash
pip install prompt2python
```

## Quick Start

```python
from prompt2python import llm

@llm
def analyze_sentiment(text: str) -> str:
    """
    Analyze the sentiment of the given text and return:
    - 'positive' for positive sentiment
    - 'negative' for negative sentiment
    - 'neutral' for neutral sentiment

    Args:
        text: The text to analyze

    Returns:
        The sentiment classification
    """
    pass

# Use the function naturally
result = analyze_sentiment("I love this new feature!")
print(result)  # Output: positive
```

## Development

### Development Setup

```bash
git clone <repository-url>
cd prompt2python
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Type checking
mypy .

# Linting
ruff check .

# Formatting
black .

# Coverage
pytest --cov=prompt2python
```

## Contributing

This project uses a workstream-based development approach. See [workstreams/README.md](workstreams/README.md) for detailed information about available workstreams and how to contribute.

### Workstream Status

| Workstream | Status | Notes |
|------------|--------|-------|
| 07: Static Checks | ✅ Completed | Code safety validation |
| Others | ⏳ Available | Ready for development |

## License

MIT License - see LICENSE file for details.

## Support

For questions, issues, or contributions, please refer to the workstream documentation or create an issue in the repository.