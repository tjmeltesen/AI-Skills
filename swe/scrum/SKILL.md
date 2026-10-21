---
name: scrum
description: >-
  Execute empirical, iterative agile software development based on Ken Schwaber
  (1995) and Jeff Sutherland. Use for dynamic, evolving projects where
  requirements emerge through rapid feedback loops, small autonomous teams, and
  timeboxed sprint increments.
trigger: /scrum
argument-hint: "[phase or sprint task]"
compatibility: Requires sprint tracking documentation at docs/scrum/** and testing framework
model: inherit
context: inherit
role: "Scrum Master & Sprint Engineer"
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - run_command
enable-write-tools: true
enable-subagent-tools: false
paths:
  - "docs/scrum/**"
version: "1.0.0"
author: "TJ Meltesen"
license: "MIT"
category: "swe"
repository: "https://github.com/tjmeltesen/AI-Skills"
tags:
  - scrum
  - agile
  - schwaber-1995
  - sprint
  - backlog
metadata:
  short-description: "Schwaber's empirical process control and sprint cycle"
  paper: "SCRUM Development Process (Schwaber, 1995)"
---

# Scrum Process Model

Execute software engineering through empirical process control (transparency, inspection, and adaptation), managing complexity and shifting requirements through structured, timeboxed sprint iterations. Based on Ken Schwaber's 1995 OOPSLA paper *"SCRUM Development Process"* co-authored with Dr. Jeff Sutherland.

> **Core Axiom:** Software development is inherently non-linear and unpredictable. Attempting to lock down complete predictive plans upfront fails. Instead, software should be developed in small, self-organizing cycles that inspect and adapt to empirical evidence at every increment.

## Commands

| Runtime | Command |
| --- | --- |
| Claude Code | `/scrum [phase or sprint task]` |
| Cursor | `/scrum [phase or sprint task]` |
| Grok Build | `/scrum [phase or sprint task]` |
| Codex, ChatGPT | `$scrum` then the phase or sprint task |

## The 3 High-Level Phases (Schwaber 1995)

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. PRE-GAME PHASE                                           │
│    ├─ Planning: Vision, Product Backlog, Estimation         │
│    └─ Architecture: High-Level Design, Interface Contracts  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. GAME PHASE (Iterative Sprints)                           │
│    ┌───────────────────────────────────────────────────┐    │
│    │ 1. Sprint Planning ──> 2. Sprint Execution        │    │
│    │          ▲                     │                  │    │
│    │          │                     ▼                  │    │
│    │ 4. Retrospective   <── 3. Sprint Review & Demo    │    │
│    └───────────────────────────────────────────────────┘    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. POST-GAME PHASE                                          │
│    └─ Integration, System Testing, Release & Documentation  │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Pre-Game

### Step 1: Product Planning & Backlog Creation
- **Objective:** Establish the product vision, high-level business goals, and initialize the Product Backlog.
- **Agent Action:**
  1. Define user stories with clear "As a... I want... So that..." structure.
  2. Establish unambiguous acceptance criteria for each story.
  3. Prioritize items by business value, risk, and dependencies into `docs/scrum/product-backlog.md`.
  4. Estimate relative effort (story points / t-shirt sizes).

### Step 2: Architecture & High-Level Design
- **Objective:** Establish a workable technical foundation and interface boundaries without over-engineering speculative features.
- **Agent Action:**
  1. Determine macro-architecture (monolith vs. modular services, persistence model, frameworks).
  2. Document core system context and component interfaces in `docs/scrum/architecture-baseline.md`.
  3. Conduct technical feasibility spikes for novel technologies.

---

## Phase 2: Game (The Sprint Cycle)

Each sprint runs on a fixed timebox (typically 1 to 2 weeks) and executes the following four steps:

### Step 3: Sprint Planning
- **Objective:** Commit to a focused Sprint Goal and select the highest-priority backlog items the team will deliver.
- **Agent Action:**
  1. Formulate a single, cohesive **Sprint Goal** (e.g., "Enable OAuth authentication and profile management").
  2. Pull stories from the top of the Product Backlog into the **Sprint Backlog** (`docs/scrum/sprint-<N>/backlog.md`).
  3. Decompose stories into technical implementation tasks (estimated in hours or sub-steps).
  4. Verify that the scope fits within the team's historical velocity.

### Step 4: Sprint Execution & Daily Inspection
- **Objective:** Develop, test, and integrate the selected stories into a working, production-grade increment.
- **Agent Action:**
  1. Pick tasks in prioritized order; drive implementation using test-driven practices (`/tdd`).
  2. Enforce the **Definition of Done (DoD)** on every story:
     - Code compiles with zero static analysis warnings.
     - Unit and integration tests pass cleanly.
     - Automated CI checks (`validate-skills`, linting, tests) pass.
     - Code review approved by peer or maintainer.
  3. Run daily inspection checkpoints:
     - *What was finished yesterday?*
     - *What will be tackled today?*
     - *What blockers or impediments exist?* (Log blockers in `docs/scrum/sprint-<N>/blockers.md`).

### Step 5: Sprint Review & Demonstration
- **Objective:** Inspect the working product increment alongside stakeholders and adapt the product backlog.
- **Agent Action:**
  1. Demonstrate only stories that satisfy 100% of the Definition of Done. Never demo unfinished work.
  2. Capture stakeholder feedback, usability observations, and new requests.
  3. Update the Product Backlog: adjust priorities, split complex stories, and add newly discovered requirements.

### Step 6: Sprint Retrospective
- **Objective:** Inspect team practices, tools, and workflows to commit to tangible process improvements.
- **Agent Action:**
  1. Evaluate the sprint across three prompts:
     - *What went well?*
     - *What slowed us down or failed?*
     - *What will we do differently next sprint?*
  2. Record 1 to 2 high-leverage process adjustments in `docs/scrum/sprint-<N>/retro.md`.
  3. Apply those adjustments immediately in Sprint $N+1$.

---

## Phase 3: Post-Game

### Step 7: Release Closure & Deployment
- **Objective:** Finalize product release, execute operational cutover, and archive sprint logs.
- **Agent Action:**
  1. Run end-to-end regression suites and security audits on the candidate release.
  2. Produce user-facing release notes and deployment runbooks.
  3. Execute automated deployment to production environment.
  4. Perform post-deployment smoke tests and verify monitoring telemetry.
