---
name: spec-driven-dev
description: >-
  Execute modern Specification-Driven Development (SDD) for AI agents. Combines
  rigorous requirements grilling, living specification authoring, deep module seam
  design, concurrent task frontier execution, and dual-axis code review (Standards vs. Spec).
trigger: /spec-driven-dev
argument-hint: "[feature name, user story, or RFC topic]"
compatibility: Requires workspace access to create SPEC.md and execute test-driven subagent loops
model: inherit
context: inherit
role: "Specification & Architecture Lead"
timeout: 900
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - run_command
enable-write-tools: true
enable-subagent-tools: true
paths:
  - "SPEC.md"
  - "docs/sdd/**"
version: "1.0.0"
author: "TJ Meltesen"
license: "MIT"
category: "swe"
repository: "https://github.com/tjmeltesen/AI-Skills"
tags:
  - sdd
  - specification
  - architecture
  - seams
  - tdd
metadata:
  short-description: "Specification-Driven Development for autonomous coding agents"
---

# Specification-Driven Development (SDD)

Execute software engineering through **Specification-Driven Development (SDD)**, the modern standard for AI-assisted and autonomous agentic engineering. Combines conversational grilling, living specifications, interface seams, task dependency graphs, and dual-axis code review.

> **Core Axiom:** Autonomous agents fail when prompt instructions are underspecified. Rather than jumping directly from a user prompt into code synthesis, SDD forces a strict sequence: **Grill Intent → Author Living Spec → Freeze Module Seams → Break into Task DAG → Execute across Concurrency Frontier → Review on Standards & Spec**.

## Commands

| Runtime | Command |
| --- | --- |
| Claude Code | `/spec-driven-dev [feature or RFC]` |
| Cursor | `/spec-driven-dev [feature or RFC]` |
| Grok Build | `/spec-driven-dev [feature or RFC]` |
| Codex, ChatGPT | `$spec-driven-dev` then the feature |

## The 6-Step Spec-Driven Lifecycle

```text
1. Grilling & Alignment (Interrogate assumptions, edge cases, boundaries)
           │
           ▼
2. Author Living Spec (SPEC.md, Domain Vocabulary, Architecture)
           │
           ▼
3. Deep Module Seam Design (Small stable interfaces, hidden complexity)
           │
           ▼
4. Ticket Graph & Ready Frontier (Dependencies, Concurrency Planning)
           │
           ▼
5. Subagent Implementation Loop (Test-driven code synthesis per seam)
           │
           ▼
6. Dual-Axis Code Review (Axis 1: Code Standards | Axis 2: Spec Faithfulness)
```

---

### Step 1: Grilling & Intent Clarification
- **Objective:** Interrogate the user's intent relentlessly until every ambiguous branch of the design tree is resolved.
- **Agent Action:**
  1. Ask targeted questions about edge cases, failure states, performance requirements, and data lifecycles.
  2. Disclose trade-offs: latency vs. cost, consistency vs. availability.
  3. Do not proceed to code or architecture while requirements remain vague.
- **Completion Criterion:** User aligns on decisions; zero unresolved trade-offs.

### Step 2: Author the Living Specification
- **Objective:** Create an authoritative, single source of truth for the system in `SPEC.md`.
- **Agent Action:**
  1. Document domain models, terminology glossary, and state machines.
  2. Detail public API endpoints, schemas, database tables, and event schemas.
  3. Define non-functional constraints (SLAs, error budgets, security bounds).
  4. Maintain `SPEC.md` as a living document: if requirements evolve during coding, update `SPEC.md` first before touching code.
- **Completion Criterion:** `SPEC.md` is complete, clear, and committed to the repository.

### Step 3: Deep Module Seam Design
- **Objective:** Design clean software seams that provide rich, deep capability behind small, stable interfaces.
- **Agent Action:**
  1. Place seams at natural boundaries (network, storage, domain service boundaries).
  2. Maximize information hiding: callers interact only with public function signatures; internal details are completely private.
  3. Ensure each interface is testable in isolation using mocks or in-memory stubs.
- **Completion Criterion:** Interface definitions and types committed; zero implementation logic written yet.

### Step 4: Ticket Graph & Concurrency Frontier
- **Objective:** Decompose the specification into discrete, testable tickets mapped into an execution graph.
- **Agent Action:**
  1. Author atomic tickets in `docs/sdd/tickets.md`, each referencing its corresponding section in `SPEC.md`.
  2. Declare blocking dependency edges for every ticket.
  3. Identify the **Ready Frontier**: tickets whose dependencies are satisfied and can be worked on concurrently by independent agents.
- **Completion Criterion:** Tickets organized into a dependency DAG; ready frontier clearly identified.

### Step 5: Subagent Implementation Loop
- **Objective:** Implement tickets along the ready frontier, driving test-driven development at each seam.
- **Agent Action:**
  1. Dispatch implementer subagents for tickets on the ready frontier.
  2. Implementer writes tests first to prove the seam behavior, then writes code to pass tests.
  3. As tickets complete, new tickets unlock on the frontier and are dispatched.
- **Completion Criterion:** All tickets implemented; all unit and integration tests passing.

### Step 6: Dual-Axis Code Review
- **Objective:** Perform a rigorous, two-perspective review of the completed work before merging.
- **Agent Action:**
  1. **Axis 1 (Standards Review):** Does the code follow repository coding conventions, type safety standards, test coverage bars, and Fowler smell baselines?
  2. **Axis 2 (Spec Faithfulness Review):** Does the code faithfully and completely implement everything requested in `SPEC.md`? Were any features omitted or invented?
  3. Run reviews independently so one perspective does not pollute the other.
- **Completion Criterion:** Both review axes pass with zero blocking comments; Pull Request submitted.
