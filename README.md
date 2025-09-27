# Prompted Objects Library

A Python library for docstring-driven, object-oriented LLM orchestration that automatically routes between model calls and vetted code artifacts.

## Overview

**Prompted Objects** enables seamless integration between natural language programming and traditional code execution through intelligent routing and policy-based decision making. The library provides a decorator-driven approach to LLM integration that feels natural to Python developers.

## Key Features

- **🔧 `@llm` Decorator**: Natural language programming interface for Python objects
- **🎯 Policy-Based Routing**: Intelligent decision making between code execution and LLM calls
- **🛡️ Safe Code Generation**: Sandboxed execution environment with comprehensive validation
- **📦 Versioned Artifacts**: Lifecycle management for generated code and prompts
- **📊 Observability**: Comprehensive logging and telemetry for LLM interactions
- **⚙️ CLI Tooling**: Command-line interface for artifact management and debugging

## Architecture

The library is organized into 14 independent workstreams that can be developed in parallel:

### Phase 1: Foundation (Parallel Development)
- **Policy DSL & Parser** - Core routing logic foundation
- **Docstring Parser** - Metadata extraction from Python objects
- **OpenAI Adapter** - LLM provider interface abstraction
- **Static Checks** - Code safety and validation system
- **Sandbox Runner** - Safe execution environment
- **Artifact Store** - Code artifact lifecycle management
- **Telemetry/Logging** - Observability and monitoring
- **Role Prompt Templates** - System message template management

### Phase 2: Integration (Sequential)
- **Decorator Wrapper** - `@llm` decorator implementation
- **Codegen Engine** - Dynamic code generation capabilities
- **Router Core** - Central routing orchestration
- **Auto-Tests** - Automated testing framework

### Phase 3: Advanced Features
- **CLI Tooling** - Command-line interface
- **Spec Loader** - Configuration and specification loading

## Quick Start

```python
from prompted_objects import llm

class MathAssistant:
    """A helpful math assistant that can solve problems and explain concepts."""

    @llm
    def solve_problem(self, problem: str) -> str:
        """
        Solve a mathematical problem and provide a step-by-step explanation.

        Args:
            problem: The mathematical problem to solve

        Returns:
            Step-by-step solution with explanation
        """
        # This method will be dynamically implemented by the LLM
        pass

    @llm
    def explain_concept(self, concept: str) -> str:
        """
        Explain a mathematical concept in simple terms.

        Args:
            concept: The mathematical concept to explain

        Returns:
            Clear explanation of the concept
        """
        pass

# Usage
assistant = MathAssistant()
result = assistant.solve_problem("What is the derivative of x^2?")
print(result)
```

## Installation

```bash
pip install prompted-objects
```

## Development

This project uses a workstream-based development approach. See [workstreams/README.md](workstreams/README.md) for detailed information about ongoing development efforts and how to contribute.

### Development Setup

```bash
git clone <repository-url>
cd prompted-objects
pip install -e ".[dev]"
```

## Documentation

- [Requirements Specification](requirements.md) - Complete technical requirements
- [Workstreams Guide](workstreams/README.md) - Development workflow and coordination
- [API Documentation](docs/api.md) - API reference (when available)
- [Examples](examples/) - Usage examples and demos

## Contributing

We welcome contributions! Please see our [contributing guide](CONTRIBUTING.md) for details on:

- How to claim and work on development workstreams
- Code standards and testing requirements
- Documentation guidelines

## License

[License information to be determined]

---

*Built with ❤️ for the Python and LLM ecosystem*