# Prompt2Python

A Python library for docstring-driven, object-oriented LLM orchestration that automatically routes between model calls and vetted code artifacts.

## Overview

**Prompted Objects** enables natural language programming through the `@llm` decorator, providing policy-based routing between code execution and LLM calls with built-in safety mechanisms.

## Key Features

- **@llm Decorator**: Natural language programming interface
- **Policy-Based Routing**: Intelligent routing between code and LLM execution
- **Safe Code Generation**: Sandboxing and validation for secure code generation
- **Versioned Artifact Storage**: Lifecycle management for generated code artifacts
- **Comprehensive Observability**: Built-in telemetry and CLI tooling

## Architecture

The library is organized into 14 independent workstreams that can be developed in parallel:

### Phase 1: Foundation (Parallel Development)
- **Policy DSL & Parser** - Core routing logic foundation
- **Docstring Parser** - Metadata extraction
- **OpenAI Adapter** - LLM provider interface
- **Static Checks** - Code safety validation
- **Sandbox Runner** - Safe execution environment
- **Artifact Store** - Code artifact management
- **Telemetry/Logging** - Observability system
- **Role Prompt Templates** - System message templates

### Phase 2: Integration (Sequential Dependencies)
- **Decorator Wrapper** - Depends on Docstring Parser
- **Codegen Engine** - Depends on OpenAI Adapter
- **Router Core** - Depends on multiple Phase 1 components
- **Auto-Tests** - Works with Codegen Engine

### Phase 3: Advanced Features
- **CLI Tooling** - Depends on Router Core and other components
- **Spec Loader** - Depends on Docstring Parser

## Installation

```bash
pip install prompt2python
```

## Quick Start

```python
from prompt2python import llm

@llm(policy="auto")
def analyze_data(data: str) -> str:
    """
    Analyze the given data and provide insights.
    If data analysis fails, generate a summary using LLM.
    """
    # Your implementation here
    pass
```

## Development

This project uses a workstream-based development approach. See [workstreams/README.md](workstreams/README.md) for detailed task definitions and coordination information.

### Development Setup

```bash
git clone <repository>
cd prompt2python
pip install -e ".[dev]"
```

### Key Dependencies

- Python 3.12+
- OpenAI API access
- Type hints and modern Python practices

## Documentation

- [Requirements Specification](requirements.md) - Complete technical specifications
- [Workstreams Guide](workstreams/README.md) - Development coordination
- [Examples](examples/) - Usage examples and demos

## Contributing

1. Check available workstreams in [workstreams/README.md](workstreams/README.md)
2. Claim a workstream by updating the status board
3. Create a feature branch: `git checkout -b feature/workstream-X-description`
4. Implement following the workstream specifications
5. Ensure all quality gates are met (tests, type hints, documentation)

## License

[Add license information here]