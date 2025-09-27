# Prompted Objects Library

**Prompted Objects** is a Python library for docstring-driven, object-oriented LLM orchestration that automatically routes between model calls and vetted code artifacts.

## 🚀 Key Features

- **@llm decorator** for natural language programming
- **Policy-based routing** between code and LLM execution
- **Safe code generation** with sandboxing and validation
- **Versioned artifact storage** and lifecycle management
- **Comprehensive observability** and CLI tooling

## 🏗️ Architecture

The library is organized into 14 independent workstreams that can be developed in parallel with clear interfaces and dependencies:

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
- **Decorator Wrapper** ← depends on Docstring Parser
- **Codegen Engine** ← depends on OpenAI Adapter
- **Router Core** ← depends on multiple Phase 1 components
- **Auto-Tests** ← works with Codegen Engine

### Phase 3: Advanced Features
- **CLI Tooling** ← depends on Router Core and other components
- **Spec Loader** ← depends on Docstring Parser

## 🛠️ Installation

```bash
# Install from source (development)
git clone <repository-url>
cd prompted-objects
pip install -e ".[dev]"

# Or install from PyPI (when available)
pip install prompted-objects
```

## 📖 Usage Example

```python
from prompted_objects import llm

class MathAssistant:
    """A helpful math assistant that can solve problems and explain concepts."""

    @llm(policy="auto")  # Automatically route between code and LLM
    def solve_problem(self, problem: str) -> str:
        """
        Solve a math problem and provide step-by-step explanation.

        Args:
            problem: The math problem to solve

        Returns:
            Step-by-step solution with explanation
        """
        # This method will be automatically implemented
        # by either running generated code or calling an LLM
        pass
```

## 🔧 Development

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd prompted-objects
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests:
   ```bash
   pytest
   ```

4. Check code quality:
   ```bash
   mypy prompted_objects
   black prompted_objects tests
   isort prompted_objects tests
   ```

### Workstream Development

This project uses a workstream-based development approach. Each major component is developed as an independent workstream with clear interfaces and dependencies.

To contribute to a workstream:

1. Check the [Workstreams README](workstreams/README.md) for available tasks
2. Claim an available workstream by updating the status board
3. Follow the detailed instructions in the specific workstream file
4. Update progress in `AGENT_COORDINATION.md`

## 📁 Project Structure

```
prompted-objects/
├── prompted_objects/           # Main package
│   ├── adapters/              # LLM provider adapters
│   ├── artifacts/             # Artifact storage and management
│   ├── cli/                   # Command-line interface
│   ├── codegen/               # Code generation engine
│   ├── decorators.py          # @llm decorator implementation
│   ├── exceptions.py          # Custom exceptions
│   ├── policy.py              # Policy DSL implementation
│   ├── router.py              # Request routing logic
│   ├── sandbox/               # Safe code execution
│   └── telemetry/             # Observability and logging
├── examples/                  # Usage examples
├── tests/                     # Test suite
├── workstreams/               # Development workstreams
├── docs/                      # Documentation
└── pyproject.toml             # Project configuration
```

## 🤝 Contributing

1. **Read the docs**: Start with `requirements.md` for complete technical specifications
2. **Check coordination**: Review `AGENT_COORDINATION.md` for current status
3. **Claim workstream**: Update `workstreams/README.md` to claim available tasks
4. **Follow patterns**: Check existing examples in the codebase
5. **Test thoroughly**: Maintain high test coverage and quality standards

## 📋 Requirements

- Python 3.12+
- Type hints throughout
- 90%+ test coverage
- Strict mypy compliance
- Comprehensive documentation

## 📄 License

[Add license information here]

## 🆘 Support

- **Documentation**: [Link to detailed docs]
- **Issues**: [Link to issue tracker]
- **Discussions**: [Link to discussions]