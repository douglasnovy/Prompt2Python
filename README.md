# Prompt2Python (Prompted Objects)

A Python library for **docstring-driven, object-oriented LLM orchestration** that automatically routes between model calls and vetted code artifacts.

## Overview

**Prompted Objects** revolutionizes LLM integration by enabling natural language programming through docstring-driven decorators while maintaining type safety, testability, and production reliability.

### Key Features

- **🗣️ `@llm` Decorator**: Natural language programming interface for seamless LLM integration
- **🔀 Policy-Based Routing**: Intelligent routing between code execution and LLM calls based on context and policies
- **🛡️ Safe Code Generation**: Sandboxed execution environment with comprehensive validation
- **📚 Versioned Artifacts**: Lifecycle management for generated code and prompts
- **📊 Observability**: Comprehensive telemetry and logging for production monitoring
- **🧪 Auto-Testing**: Automated test generation and validation for LLM outputs
- **⚡ CLI Tooling**: Complete command-line interface for development and operations

## Architecture

Built on **14 independent workstreams** designed for parallel development with clear interfaces:

### Phase 1: Foundation (Parallel Development)
- **Policy DSL & Parser** - Core routing logic foundation
- **Docstring Parser** - Metadata extraction from docstrings
- **OpenAI Adapter** - LLM provider interface abstraction
- **Static Checks** - Code safety and validation system
- **Sandbox Runner** - Secure execution environment
- **Artifact Store** - Versioned code artifact management
- **Telemetry/Logging** - Comprehensive observability system
- **Role Prompt Templates** - System message template management

### Phase 2: Integration (Sequential)
- **Decorator Wrapper** - `@llm` decorator implementation
- **Codegen Engine** - Safe code generation capabilities
- **Router Core** - Central orchestration logic
- **Auto-Tests** - Automated testing framework

### Phase 3: Advanced Features
- **CLI Tooling** - Complete command-line interface
- **Spec Loader** - Specification loading and parsing

## Quick Start

```python
from prompted_objects import llm

@llm(policy="math_solver", temperature=0.3)
def solve_math_problem(problem: str) -> str:
    """
    Solves mathematical problems using step-by-step reasoning.

    Args:
        problem: The mathematical problem to solve

    Returns:
        Step-by-step solution with explanation
    """
    # Your implementation here
    pass
```

## Installation

```bash
# From source (recommended for development)
git clone <repository-url>
cd prompted-objects
pip install -e ".[dev]"

# Production installation
pip install prompted-objects
```

## Development Status

**Current Phase**: Foundation workstreams in progress

| Workstream | Status | Description |
|------------|--------|-------------|
| Static Checks | ✅ Completed | Code safety validation system |
| Policy DSL & Parser | ⏳ Available | Core routing logic foundation |
| Docstring Parser | ⏳ Available | Metadata extraction |
| OpenAI Adapter | ⏳ Available | LLM provider interface |
| Sandbox Runner | ⏳ Available | Safe execution environment |
| Artifact Store | ⏳ Available | Code artifact management |
| Telemetry/Logging | ⏳ Available | Observability system |
| Role Prompt Templates | ⏳ Available | System message templates |

## Documentation

- **[Requirements Specification](requirements.md)** - Complete technical specifications
- **[Workstreams Guide](workstreams/)** - Detailed development tasks
- **[Examples](examples/)** - Usage examples and demos
- **[API Reference](docs/)** - Complete API documentation

## Contributing

This project uses a **parallel development model** with 14 independent workstreams. See our [Workstreams Guide](workstreams/README.md) for details on how to contribute.

### Quick Contribution Guide

1. **Claim a workstream** in `workstreams/README.md`
2. **Create a feature branch**: `git checkout -b feature/workstream-X-description`
3. **Implement following the workstream specification**
4. **Add tests and documentation**
5. **Submit a pull request**

### Development Requirements

- Python 3.12+
- Type hints required for all new code
- 90%+ test coverage
- MyPy strict mode compliance
- Security validation for all components

## License

[Add license information here]

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/prompted-objects/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/prompted-objects/discussions)
- **Documentation**: [Project Wiki](https://github.com/your-org/prompted-objects/wiki)

---

**Prompt2Python** - Bridging the gap between natural language and reliable code execution.