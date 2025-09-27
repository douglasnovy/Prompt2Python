# Prompted Objects - Docstring-Driven LLM Orchestration

A Python library for docstring-driven, object-oriented LLM orchestration that auto-routes between model calls and vetted, sandboxed code artifacts.

## Features

- **Natural Language Programming**: Write prompts in docstrings, execute via LLM or optimized code
- **Policy-Based Routing**: Declarative rules determine when to use code vs. model execution
- **Safe Code Generation**: AST-validated, sandboxed code artifacts with resource limits
- **Versioned Artifacts**: Track and rollback generated code with full audit trails
- **Observability**: Comprehensive logging, cost tracking, and performance monitoring
- **CLI Tools**: Manage artifacts, policies, and deployments

## Installation

```bash
pip install prompted-objects
```

For development:
```bash
git clone <repository>
cd prompted-objects
pip install -e ".[dev]"
```

## Quick Start

```python
from prompted_objects import llm

class Math:
    @llm(role="method", model="gpt-4o-mini", allow_hot_codegen=True)
    def add(self, a: int, b: int) -> int:
        """
        PROMPT:
        Return the sum of a and b.

        METADATA:
        id: math.add
        policy:
          - if: "is_int(a) and is_int(b)"
            then: code
          - else: model
        examples:
          - input: {a: 2, b: 3}
            output: 5
        capabilities:
          io: false
          network: false
          imports: ["math"]
        parse: auto
        strict: false
        """
        pass

# Usage
math_ops = Math()
result = math_ops.add(2, 3)  # Routes to code or model based on policy
```

## Architecture

The library consists of several key components:

- **Decorators**: `@llm` decorator with policy-driven routing
- **Router**: Deterministic routing engine evaluating policies and budgets
- **Adapters**: Normalized interfaces to LLM providers (OpenAI, Azure, etc.)
- **Codegen**: Safe code generation with AST validation and testing
- **Sandbox**: Restricted execution environment with resource limits
- **Artifacts**: Versioned storage of generated code with manifests
- **Telemetry**: Structured logging and observability

## Development

### Workstreams

This project uses parallel development workstreams. See `workstreams/README.md` for the complete workflow and current status.

### ⚠️ CRITICAL: Git Workflow & Safety Practices

**This project uses git for coordination. NEVER use destructive git commands that can lose work!**

#### ✅ SAFE Git Workflow

```bash
# ALWAYS start by checking status and pulling latest
git status                    # Check your current state
git pull origin main          # Get latest coordination updates
cat workstreams/README.md     # Check workstream availability

# Claim a workstream (CRITICAL FIRST STEP)
# Edit workstreams/README.md and change status to 🔄 In Progress
git add workstreams/README.md
git commit -m "Claim workstream X: description"
git push origin main          # Push claim immediately!

# Create and switch to feature branch
git checkout -b feature/workstream-{number}-{description}
git push -u origin feature/workstream-{number}-{description}

# REGULAR COMMITS - Save points every 15-30 minutes
git add .
git commit -m "WIP: implemented X feature"
git push origin feature/workstream-{number}-{description}

# Complete workstream
# Edit workstreams/README.md and change status to ✅ Completed
git add workstreams/README.md
git commit -m "Complete workstream X: description"

# Merge back to main (NEVER force push!)
git checkout main
git pull origin main          # Ensure main is up to date
git merge feature/workstream-{number}-{description}
git push origin main          # Push merged changes

# Clean up (only after successful merge)
git branch -d feature/workstream-{number}-{description}
git push origin --delete feature/workstream-{number}-{description}
```

#### 🚫 DANGEROUS Commands - NEVER Use These!
```bash
# These can PERMANENTLY DELETE work - DON'T USE THEM!
git reset --hard HEAD~N     # Deletes commits and work
git reset --hard <commit>   # Deletes all work after that commit
git push --force            # Overwrites remote history
git push --force-with-lease # Still dangerous
```

#### 🛡️ Safety Rules
- **ALWAYS commit before risky operations**
- **NEVER reset to commits that remove work**
- **ALWAYS push feature branches regularly**
- **NEVER work directly on main branch**
- **ALWAYS pull before starting work**
- **Claim workstreams BEFORE starting implementation**

#### 🔄 Coordination Rules
- **Claim workstreams** by updating `workstreams/README.md` status board
- **Never work on** 🔄 In Progress or 🚫 Blocked workstreams
- **Regular commits** - treat them as save points, not final deliverables
- **Update status** when completing workstreams
- **Pull before starting** to get latest coordination updates

#### 🆘 Recovery (If Something Goes Wrong)
```bash
# If you accidentally lose work:
git reflog                    # See all recent actions
git checkout <commit-hash>    # Go back to a safe point
git checkout -b recovery-branch  # Create recovery branch
# Contact other agents for help with recovery
```

**Remember**: Git commits are your safety net. Commit early, commit often, and never use destructive commands!

### Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=prompted_objects

# Type checking
mypy prompted_objects

# Linting
ruff check prompted_objects
ruff format prompted_objects
```

## Security

- No network/file system access unless explicitly permitted
- AST validation prevents dangerous code patterns
- Sandbox execution with resource limits
- PII redaction in logs and API calls

## Contributing

1. Check `workstreams/README.md` for available workstreams
2. Follow the git workflow above - **safety first!**
3. Implement according to interface contracts
4. Add comprehensive tests (≥90% coverage)
5. Update documentation and examples
6. Submit PR for review

## License

MIT License - see LICENSE file for details.

## Requirements

See `requirements.md` for complete technical specifications.