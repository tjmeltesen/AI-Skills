---
name: agentic-sdlc
description: >-
  Execute the modern Agentic Software Development Lifecycle (A-SDLC / SE 3.0).
  Inverts traditional human-driven workflows into agent-executed, human-steered
  phases: Intent Elicitation, Living Specification, Autonomous Task DAG Execution,
  Self-Refining Code Loops, Continuous Automated Verification, and Governance.
trigger: /agentic-sdlc
argument-hint: "[epic, initiative, or repository goal]"
compatibility: Requires git, python >= 3.8, and terminal execution access for automated verification
model: pro
context: fresh
workspace: branch
role: "Agentic SDLC Orchestrator"
timeout: 1200
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - run_command
enable-write-tools: true
enable-subagent-tools: true
enable-mcp-tools: true
paths:
  - "docs/asdlc/**"
version: "1.0.0"
author: "TJ Meltesen"
license: "MIT"
category: "swe"
repository: "https://github.com/tjmeltesen/AI-Skills"
tags:
  - agentic-sdlc
  - se-3.0
  - ace
  - aee
  - lifecycle
metadata:
  short-description: "End-to-end Agentic SDLC (SE 3.0) reference workflow"
  papers:
    - "Agentic AI in the Software Development Lifecycle (2024)"
    - "Agentic Software Engineering: Foundational Pillars and a Research Roadmap (2024)"
---

# Agentic Software Development Lifecycle (A-SDLC)

Execute software engineering through the modern **Agentic SDLC (SE 3.0)** framework. Based on contemporary peer-reviewed research including *"Agentic AI in the Software Development Lifecycle: Architecture, Empirical Evidence, and the Reshaping of Software Engineering"* (2024) and *"Agentic Software Engineering: Foundational Pillars and a Research Roadmap"* (Bavishi et al., 2024).

> **The Core Paradigm Shift (Inversion of Control):** Traditional SDLC treated software development as human-executed work assisted by tools. The Agentic SDLC inverts this control model: **AI agents execute the planning, coding, navigation, and testing loops**, while **humans provide intent steering, architectural boundary governance, and risk oversight**.

## Commands

| Runtime | Command |
| --- | --- |
| Claude Code | `/agentic-sdlc [feature or initiative]` |
| Cursor | `/agentic-sdlc [feature or initiative]` |
| Grok Build | `/agentic-sdlc [feature or initiative]` |
| Codex, ChatGPT | `$agentic-sdlc` then the feature or initiative |

## The 6 Phases of Agentic SDLC

```text
1. Intent Elicitation & Steering (Human ──> Agent Command Environment)
           │
           ▼
2. Living Specification & Seam Design (SPEC.md & Interface Contracts)
           │
           ▼
3. Task DAG Decomposition (Dependencies, Ready Frontiers, Concurrency)
           │
           ▼
4. Autonomous Execution & Self-Refinement (Agent Execution Environment)
           │
           ▼
5. Multi-Layer Automated Verification (Reproductions, Tests, Invariants)
           │
           ▼
6. Human Governance & Merge Danger Assessment (Two-way Door Review)
```

---

### Phase 1: Intent Elicitation & Steering (ACE)
- **Objective:** Translate high-level human objectives and ambiguous requirements into precise, bounded engineering intent inside the **Agent Command Environment (ACE)**.
- **Agent Action:**
  1. Conduct an alignment grill: interrogate vague terms, hidden assumptions, edge-case behavior, and operational constraints.
  2. Identify immutable boundaries (security controls, performance ceilings, backward compatibility).
  3. Produce `docs/asdlc/01-intent-brief.md`.
- **Exit Gate:** Human confirms the intent brief; zero ambiguous business terms remain.

### Phase 2: Living Specification & Seam Design
- **Objective:** Establish the technical contract and deep module seams before writing any implementation code.
- **Agent Action:**
  1. Author a comprehensive **Living Specification** (`docs/asdlc/02-spec.md`):
     - Domain vocabulary and state definitions.
     - Public API contracts, JSON schemas, and database migrations.
     - Non-functional requirements (throughput, error recovery).
  2. Define **Deep Module Seams**: maximize internal logic hidden behind narrow, stable interfaces.
- **Exit Gate:** Specification committed; interface contracts frozen.

### Phase 3: Task DAG Decomposition & Frontier Planning
- **Objective:** Deconstruct the specification into a Directed Acyclic Graph (DAG) of isolated, atomic work units.
- **Agent Action:**
  1. Map dependencies between tasks into `docs/asdlc/03-task-dag.md`.
  2. Identify the **Ready Frontier**: tasks whose prerequisite edges are fully satisfied and can execute concurrently without merge collisions.
  3. Define explicit, checkable **Completion Criteria** for each task node.
- **Exit Gate:** Work graph validated; zero circular dependencies; ready frontier identified.

### Phase 4: Autonomous Execution & Self-Refinement (AEE)
- **Objective:** Dispatch agent workers into the **Agent Execution Environment (AEE)** to implement tasks against their defined seams.
- **Agent Action:**
  1. Worker agents load strictly the context needed for their assigned node (preventing context bloat).
  2. Agents leverage specialized tool interfaces (file editing, AST searching, terminal execution).
  3. **Self-Refinement Loop:** On syntax errors, compilation failures, or static analysis warnings, the agent inspects the diagnostic output, hypothesizes the root cause, and edits in-place until clean.
- **Exit Gate:** All nodes in the ready frontier compile with zero warnings; tasks advance the DAG frontier.

### Phase 5: Multi-Layer Automated Verification
- **Objective:** Validate the synthesized code through deterministic, layered verification tiers before human review.
- **Agent Action:**
  1. **Tier 1 (Static Analysis):** Linting, strict type checking, and schema validation.
  2. **Tier 2 (Test-Driven Verification):** Unit tests, edge case assertions, and negative path testing.
  3. **Tier 3 (Interface & Contract Testing):** Verify inter-module contract compliance and API marshalling.
  4. **Tier 4 (Regression Audit):** Execute full test suite to guarantee zero existing features were broken.
  5. Generate verification telemetry in `docs/asdlc/04-verification-report.md`.
- **Exit Gate:** 100% green verification runs across all tiers; zero unresolved test regressions.

### Phase 6: Human Governance & Merge Danger Assessment
- **Objective:** Provide human maintainers with a high-signal, compressed decision packet for final merge approval.
- **Agent Action:**
  1. Prepare the Pull Request using the AI Hero PR standard:
     - **Summary:** Call tree, architecture diagram, or minimal diff-sketch.
     - **Evidence:** Concrete before & after test runs or terminal outputs.
     - **Merge Danger:** One-way vs. Two-way door classification and blast radius.
  2. Escalate only genuine trade-offs or high-risk decisions requiring human judgment.
- **Exit Gate:** Human maintainer approves PR; automated CI check passes; branch merged.
