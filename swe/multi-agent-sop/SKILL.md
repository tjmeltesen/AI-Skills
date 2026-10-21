---
name: multi-agent-sop
description: >-
  Coordinate specialized multi-agent software engineering using Standard Operating
  Procedures (SOPs) based on MetaGPT (Hong et al., ICLR 2024) and ChatDev. Eliminates
  cascading hallucinations across agent handoffs through role specialization,
  structured document contracts, and assembly-line verification gates.
trigger: /multi-agent-sop
argument-hint: "[project scope or system requirements]"
compatibility: Requires multi-agent runtime or subagent spawning tools; writes docs/sop/**
model: pro
context: fresh
workspace: branch
role: "Multi-Agent SOP Coordinator"
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
  - "docs/sop/**"
version: "1.0.0"
author: "TJ Meltesen"
license: "MIT"
category: "swe"
repository: "https://github.com/tjmeltesen/AI-Skills"
tags:
  - metagpt
  - chatdev
  - multi-agent
  - sop
  - assembly-line
metadata:
  short-description: "SOP-driven multi-agent software engineering assembly line"
  papers:
    - "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework (Hong et al., 2023 / ICLR 2024)"
    - "Communicative Agents for Software Development (Qian et al., 2023 / ACL 2024)"
---

# Multi-Agent SOP Process Model

Execute collaborative, multi-agent software engineering through **Standard Operating Procedures (SOPs)** and role-specialized assembly lines. Based on Sirui Hong et al.'s landmark paper *"MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework"* (ICLR 2024) and ChatDev (ACL 2024).

> **Core Axiom:** Unstructured chat between LLMs inevitably causes **cascading hallucinations** and context drift. Multi-agent systems succeed only when agents communicate through **standardized document artifacts** (SOPs) and strictly delineated responsibilities rather than free-form conversation.

## Commands

| Runtime | Command |
| --- | --- |
| Claude Code | `/multi-agent-sop [feature or repo task]` |
| Cursor | `/multi-agent-sop [feature or repo task]` |
| Grok Build | `/multi-agent-sop [feature or repo task]` |
| Codex, ChatGPT | `$multi-agent-sop` then the task |

## The 5-Stage Multi-Agent Assembly Line

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Product Manager Agent                                    │
│    └─ Input: User Idea / Issue ──> Output: PRD Document     │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Structured SOP Artifact)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. System Architect Agent                                   │
│    └─ Input: PRD ──> Output: System Architecture & Schemas  │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Structured SOP Artifact)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Project Manager Agent                                    │
│    └─ Input: Architecture ──> Output: Task DAG & Seams      │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Structured SOP Artifact)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Engineer Agent(s)                                        │
│    └─ Input: Assigned Task ──> Output: Modular Code Files   │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Code & Test Suite)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. QA / Reviewer Agent                                      │
│    └─ Input: Code & PRD ──> Output: Test Execution & Proof  │
└─────────────────────────────────────────────────────────────┘
```

---

### Stage 1: Product Manager Agent — PRD Formulation
- **Role Identity:** Focuses exclusively on user value, competitive differentiation, scope boundaries, and user journeys.
- **SOP Artifact Output:** `docs/sop/01-prd.md`
- **Agent Actions:**
  1. Parse user prompt; perform requirements analysis.
  2. Specify User Stories and Acceptance Criteria.
  3. Define Out-of-Scope boundaries to protect engineers from scope creep.
- **Handoff Contract:** The PRD must contain measurable acceptance criteria before passing to Stage 2.

### Stage 2: System Architect Agent — Architecture & Interface Design
- **Role Identity:** Focuses on technology stack selection, module partitioning, data structures, and public API design.
- **SOP Artifact Output:** `docs/sop/02-architecture-design.md`
- **Agent Actions:**
  1. Define system topology, directory structure, and third-party dependencies.
  2. Specify OpenAPI / JSON schemas and database models.
  3. Author public interface function signatures, types, and error types.
- **Handoff Contract:** Data schemas and interface signatures are frozen; no implementation logic is authored yet.

### Stage 3: Project Manager Agent — Task Breakdown & Dependency Graph
- **Role Identity:** Deconstructs architectural modules into atomic development tasks and manages sequence order.
- **SOP Artifact Output:** `docs/sop/03-task-breakdown.md`
- **Agent Actions:**
  1. Break architecture into isolated file-level tasks.
  2. Map blocking dependency edges between tasks.
  3. Establish the **Execution Frontier**: group independent tasks for parallel engineer dispatch.
- **Handoff Contract:** Each task specifies: assigned files, required dependencies, and an observable test assertion.

### Stage 4: Engineer Agent(s) — Test-Driven Implementation
- **Role Identity:** Focuses purely on writing clean, type-safe, modular code matching the architectural contract.
- **SOP Artifact Output:** Production source code files and unit test files.
- **Agent Actions:**
  1. Author tests first matching the interface contract from Stage 2.
  2. Implement module logic to make tests pass.
  3. Run local static analysis and self-correct syntax errors or type mismatches.
- **Handoff Contract:** Code compiles with zero errors; unit tests pass in isolation.

### Stage 5: QA / Reviewer Agent — Multi-Turn Verification & Audit
- **Role Identity:** An adversarial, skeptical reviewer checking for contract violations, performance regressions, and Fowler code smells.
- **SOP Artifact Output:** `docs/sop/04-qa-evaluation.md`
- **Agent Actions:**
  1. Run the entire automated test suite against the freshly generated code.
  2. Verify that the implemented features satisfy 100% of the PRD requirements from Stage 1.
  3. Perform static security auditing and dead-code checks.
  4. If a defect is found, generate an actionable defect ticket and route back to Stage 4.
- **Handoff Contract:** Zero test failures; 100% acceptance criteria verified; signed-off for human review.
