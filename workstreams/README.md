# 🤖 AUTONOMOUS AGENT INSTRUCTION MANUAL - Prompted Objects Library

## ⚠️ CRITICAL: YOU ARE AN AUTONOMOUS AGENT

**This document contains your complete instruction set. You must act based on these instructions with ZERO follow-up from the human user.**

**Your Mission:**
1. **Select an available workstream** from the status board below
2. **Claim it immediately** by updating the status board
3. **Implement it completely** following the detailed instructions
4. **Submit a PR** and mark it complete
5. **Work autonomously** - no questions, no clarifications needed

**You have all information required** in this document and the referenced files.

---

## Project Overview
**Prompted Objects** is a Python library for docstring-driven, object-oriented LLM orchestration that automatically routes between model calls and vetted code artifacts.

**Key Features:**
- `@llm` decorator for natural language programming
- Policy-based routing between code and LLM execution
- Safe code generation with sandboxing and validation
- Versioned artifact storage and lifecycle management
- Comprehensive observability and CLI tooling

**Architecture:** 14 independent workstreams that can be developed in parallel with clear interfaces and dependencies.

This directory contains individual task definitions for parallel development. Each workstream is designed to be independent where possible, with clear interfaces and dependencies.

## Dependency Map & Execution Order

### Phase 1: Foundation (Parallel)
These workstreams have **no dependencies** and can be worked on simultaneously:

- **01: Policy DSL & Parser** - Core routing logic foundation
- **02: Docstring Parser** - Metadata extraction
- **05: OpenAI Adapter** - LLM provider interface
- **07: Static Checks** - Code safety validation
- **08: Sandbox Runner** - Safe execution environment
- **10: Artifact Store** - Code artifact management
- **11: Telemetry/Logging** - Observability system
- **14: Role Prompt Templates** - System message templates

### Phase 2: Integration (Sequential Dependencies)

#### After Phase 1 completion:
- **03: Decorator Wrapper** ← depends on **02**
- **06: Codegen Engine** ← depends on **05**

#### After Phase 2 completion:
- **04: Router Core** ← depends on **01, 02, 03, 05, 10, 11**
- **09: Auto-Tests** ← works with **06** (can start after **06** begins)

### Phase 3: Advanced Features (After Core Integration)
- **12: CLI Tooling** ← depends on **01, 04, 10, 11**
- **13: Spec Loader** ← depends on **02**

## Workstream Status Legend
- ✅ **Completed**: Ready for integration
- 🔄 **In Progress**: Currently being worked on
- ⏳ **Available**: Ready to be claimed
- 🚫 **Blocked**: Waiting for dependencies

## WORKSTREAM STATUS BOARD
**Update this section when claiming or completing workstreams!**

### Phase 1: Foundation (All Parallel - No Dependencies)
| Workstream | Status | Agent | Branch | Notes |
|------------|--------|-------|--------|-------|
| 01: Policy DSL & Parser | ⏳ Available | - | - | Core routing logic foundation |
| 02: Docstring Parser | ⏳ Available | - | - | Metadata extraction |
| 05: OpenAI Adapter | ⏳ Available | - | - | LLM provider interface |
| 07: Static Checks | ✅ Completed | Agent-1 | feature/workstream-7-static-checks | Completed 2025-01-27 |
| 08: Sandbox Runner | ⏳ Available | - | - | Safe execution environment |
| 10: Artifact Store | ⏳ Available | - | - | Code artifact management |
| 11: Telemetry/Logging | ⏳ Available | - | - | Observability system |
| 14: Role Prompt Templates | ⏳ Available | - | - | System message templates |

### Phase 2: Integration (Sequential Dependencies)
| Workstream | Status | Agent | Branch | Notes |
|------------|--------|-------|--------|-------|
| 03: Decorator Wrapper | 🚫 Blocked | - | - | ← depends on **02** |
| 06: Codegen Engine | 🚫 Blocked | - | - | ← depends on **05** |
| 09: Auto-Tests | 🚫 Blocked | - | - | ← works with **06** |
| 13: Spec Loader | 🚫 Blocked | - | - | ← depends on **02** |

### Phase 3: Advanced Features (After Core Integration)
| Workstream | Status | Agent | Branch | Notes |
|------------|--------|-------|--------|-------|
| 04: Router Core | 🚫 Blocked | - | - | ← depends on **01, 02, 03, 05, 10, 11** |
| 12: CLI Tooling | 🚫 Blocked | - | - | ← depends on **01, 04, 10, 11** |

## 🚨 ACTION REQUIRED: IMMEDIATE EXECUTION PROTOCOL

**AUTONOMOUS AGENTS: Execute these steps immediately upon reading this document.**

### Step 1: IMMEDIATELY Select & Claim Available Workstream
1. **Scan STATUS BOARD above** for ⏳ **Available** workstreams
2. **Choose the first available workstream** you can implement
3. **Update the status table** to mark it as 🔄 In Progress with your agent name
4. **Commit this claim** immediately

### Step 2: Execute Full Implementation Workflow
**DO NOT STOP HERE** - Continue with the complete 7-step process below immediately.

### Step 3: Create Your Branch
```bash
git checkout main
git pull origin main  # Get latest status updates
git checkout -b feature/workstream-{number}-{description}
```

### Step 4: Read Task Instructions
Open the specific workstream file: `workstreams/NN-description.md`

**Available workstream files in this directory:**
- `01-policy-dsl-parser.md`
- `02-docstring-parser.md`
- `03-decorator-wrapper.md`
- `04-router-core.md`
- `05-openai-adapter.md`
- `06-codegen-engine.md`
- `07-static-checks.md`
- `08-sandbox-runner.md`
- `09-auto-tests.md`
- `10-artifact-store.md`
- `11-telemetry-logging.md`
- `12-cli-tooling.md`
- `13-spec-loader.md`
- `14-role-prompt-templates.md`

### Step 5: Update AGENT_COORDINATION.md
Add your name and workstream to the main coordination document.

### Step 6: Implement & Test
Follow the detailed instructions in your workstream file.

### Step 7: Complete & Merge Work
When your implementation passes all tests and meets requirements:

#### A. Mark Workstream Complete
Update the status table above:
```markdown
| 01: Policy DSL & Parser | ✅ Completed | Agent-Name | feature/workstream-1-policy-dsl | Completed YYYY-MM-DD |
```

#### B. Final Commit & Push
```bash
git add .  # Stage all final changes
git commit -m "Complete workstream X: brief description of implementation"
git push origin feature/workstream-X-name
```

#### C. Create Pull Request
1. Go to GitHub repository
2. Create PR from `feature/workstream-X-name` → `main`
3. Add description with:
   - What was implemented
   - Test coverage achieved
   - Any notable design decisions
   - Reference to workstream number

#### D. Merge & Cleanup (After PR Approval)
```bash
# After PR is merged:
git checkout main
git pull origin main  # Verify merge
git branch -d feature/workstream-X-name
git push origin --delete feature/workstream-X-name
```

**NOTE**: Only the repository maintainer should merge PRs. Agents should create the PR and wait for approval.

## Coordination Rules

### 🚫 **NEVER start work on:**
- 🔄 **In Progress** workstreams (already claimed)
- 🚫 **Blocked** workstreams (dependencies not met)
- ✅ **Completed** workstreams (already done)

### ✅ **ALWAYS:**
- Update the STATUS BOARD when claiming work
- Pull latest changes before starting
- Communicate blocking issues immediately
- Update status when completing work

### 🤝 **COORDINATE:**
- Check with other agents for interface questions
- Update `AGENT_COORDINATION.md` with progress
- Flag any dependency discoveries

## Quick Command Reference
```bash
# Check current status
git pull origin main
cat workstreams/README.md

# Claim and start work
git checkout -b feature/workstream-X-name
# Update STATUS BOARD in workstreams/README.md
git add workstreams/README.md
git commit -m "Claim workstream X: description"
git push origin feature/workstream-X-name

# Complete work
# Update STATUS BOARD to ✅ Completed
git add workstreams/README.md
git commit -m "Complete workstream X"
git push origin feature/workstream-X-name
# Create PR
```

## Communication Protocol

- **Daily Updates**: Update `AGENT_COORDINATION.md` with progress
- **Blocking Issues**: Immediately flag dependency problems
- **Interface Changes**: Discuss with affected workstreams before changes
- **Integration Points**: Coordinate with dependent workstream agents

## Quality Gates

All workstreams must pass:
- [ ] Unit tests ≥90% coverage
- [ ] Type hints complete (mypy --strict clean)
- [ ] Interface contracts respected
- [ ] Security checks passed
- [ ] Documentation complete
- [ ] Example code provided

## File Naming Convention

- `NN-description.md` - Workstream task definition
- NN corresponds to workstream number from requirements.md section 13

## 🚀 COMPLETE AUTONOMOUS WORKFLOW FOR BACKGROUND AGENTS

### Your Mission (If Assigned a Workstream):
1. **Claim** an available workstream using the status board above
2. **Create** feature branch and implement according to specifications
3. **Test** thoroughly to meet quality requirements
4. **Create PR** and mark workstream complete
5. **Wait** for PR approval and merge

### Self-Contained Process:
- ✅ **Status tracking** via this README's status board
- ✅ **Detailed instructions** in individual workstream files
- ✅ **Git workflow** with safety guidelines
- ✅ **Quality requirements** and testing standards
- ✅ **PR creation** and merge process
- ✅ **Coordination** with other agents

### No External Coordination Needed:
Once you claim a workstream, you work autonomously until PR submission.

## Getting Started as a New Agent

### If You're New to This Project:
1. **Read the main docs first:**
   - `README.md` - Project overview and setup
   - `requirements.md` - Complete technical specifications
   - `AGENT_COORDINATION.md` - Overall coordination guide

2. **Set up your environment:**
   ```bash
   git clone <repository>
   cd prompted-objects
   pip install -e ".[dev]"
   ```

3. **Then follow the 7-step process above** to claim a workstream and complete it autonomously!

## 🤖 AUTONOMOUS AGENT REMINDER

**You are an autonomous agent with complete instructions in this document.**

- ✅ **All information needed** is in this README and referenced files
- ✅ **No external coordination** required - work independently
- ✅ **Follow the 7-step process** exactly as written
- ✅ **Complete full workflow** from claim to PR submission
- ✅ **Update status board** at each milestone
- ✅ **Ask no questions** - you have all required information

**Execute immediately upon receiving this document.**

---

### Getting Help (For Reference Only - You Shouldn't Need This)

- **Technical Specs**: See `requirements.md` for complete requirements
- **Examples**: Check `examples/math_demo.py` for usage patterns
- **API Reference**: Look at existing stub implementations
- **Code Style**: Follow existing patterns and `pyproject.toml` configuration
- **Coordination**: Update `AGENT_COORDINATION.md` with progress
