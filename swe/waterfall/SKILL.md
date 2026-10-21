---
name: waterfall
description: >-
  Execute sequential software development with formal stage gates, heavy design
  documentation, and iterative feedback loops based on Winston Royce (1970). Use
  when requirements are fully stable upfront, compliance or contractual gates
  are mandatory, and systems demand rigorous architectural specification before
  implementation.
trigger: /waterfall
argument-hint: "[phase or locked project scope]"
compatibility: Requires repository documentation storage at docs/waterfall/**
model: inherit
context: inherit
role: "Sequential Systems Engineer"
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - run_command
enable-write-tools: true
enable-subagent-tools: false
paths:
  - "docs/waterfall/**"
  - "docs/system-requirements.md"
  - "docs/detailed-design.md"
version: "1.0.0"
author: "TJ Meltesen"
license: "MIT"
category: "swe"
repository: "https://github.com/tjmeltesen/AI-Skills"
tags:
  - waterfall
  - royce-1970
  - stage-gate
  - sequential
  - srs
metadata:
  short-description: "Royce's sequential SDLC with formal feedback loops"
  paper: "Managing the Development of Large Software Systems (Royce, 1970)"
---

# Waterfall Process Model

Execute software engineering through a disciplined sequential lifecycle with formal stage-gate transitions, comprehensive design documentation, and built-in feedback loops. Based on Dr. Winston W. Royce's 1970 IEEE WESCON paper *"Managing the Development of Large Software Systems"*.

> **Royce's Foundational Warning:** A purely linear progression without iteration is inherently risky and invites catastrophic project failure. The disciplined Waterfall process requires formal feedback loops between adjacent phases, early preliminary prototyping ("do it twice"), and customer participation throughout.

## Commands

| Runtime | Command |
| --- | --- |
| Claude Code | `/waterfall [phase or scope]` |
| Cursor | `/waterfall [phase or scope]` |
| Grok Build | `/waterfall [phase or scope]` |
| Codex, ChatGPT | `$waterfall` then the phase or scope |

## The 7 Sequential Phases

```text
1. System Requirements Analysis
      ↓ ↑ (feedback)
2. Software Requirements Analysis
      ↓ ↑ (feedback)
3. Preliminary Design / Pilot ("Do It Twice")
      ↓ ↑ (feedback)
4. Program / Detailed Design
      ↓ ↑ (feedback)
5. Coding & Unit Assembly
      ↓ ↑ (feedback)
6. Testing & Quality Assurance
      ↓ ↑ (feedback)
7. Operational Deployment & Maintenance
```

### Phase 1: System Requirements Analysis
- **Objective:** Establish the total system boundary, external hardware/software dependencies, operating environment, and performance constraints.
- **Agent Action:** 
  1. Capture all functional capabilities, performance criteria, and platform constraints.
  2. Document interfaces to external hardware, databases, and third-party APIs.
  3. Produce `docs/system-requirements.md`.
- **Exit Gate:** Formal sign-off on system scope and environmental boundaries.

### Phase 2: Software Requirements Analysis
- **Objective:** Translate system-level goals into unambiguous software functional requirements.
- **Agent Action:**
  1. Deconstruct system requirements into specific software features, data schemas, and error-handling conditions.
  2. Define measurable acceptance criteria for every requirement.
  3. Produce `docs/software-requirements-spec.md` (SRS).
- **Exit Gate:** Baseline SRS locked; change-control protocol activated.

### Phase 3: Preliminary Design & Prototype ("Do It Twice")
- **Objective:** Build an exploratory pilot system to retire sizing, timing, and storage risks before detailed design.
- **Agent Action (Royce's Rule #3):**
  1. Design a scaled-down prototype targeting the highest architectural uncertainties (throughput, concurrency, unfamiliar APIs).
  2. Implement the pilot quickly to measure performance and validate assumptions.
  3. Document discoveries, discard disposable pilot code, and record lessons in `docs/preliminary-design.md`.
- **Exit Gate:** Architectural feasibility verified; performance limits empirically measured.

### Phase 4: Program & Detailed Design
- **Objective:** Complete the exhaustive program architecture before writing production code.
- **Agent Action (Royce's Rules #1 & #2):**
  1. Define all modules, classes, public interfaces, data structures, and database schemas.
  2. Specify control flow, state diagrams, and inter-module contracts.
  3. Ensure every software requirement in Phase 2 maps to specific design components (Traceability Matrix).
  4. Write `docs/detailed-design.md`.
- **Exit Gate:** Design review approved; no code is written until interfaces and data structures are frozen.

### Phase 5: Coding & Unit Assembly
- **Objective:** Implement production software strictly adhering to the detailed design.
- **Agent Action:**
  1. Write production code matching the frozen design specifications.
  2. Ensure clean modular separation and internal documentation.
  3. If coding reveals an architectural flaw, activate the **backward feedback loop** to Phase 4 (Detailed Design) before continuing.
- **Exit Gate:** 100% of defined modules implemented; code compiles and passes static analysis cleanly.

### Phase 6: Testing & Quality Assurance
- **Objective:** Verify and validate that the implemented software faithfully fulfills every requirement in the baseline SRS.
- **Agent Action (Royce's Rule #4):**
  1. Execute pre-planned test suites created by an independent verification perspective.
  2. Test against nominal paths, boundary extremes, and stress/overload conditions.
  3. Map test failures back to their originating phase:
     - Code bugs → feedback loop to Phase 5.
     - Design omissions → feedback loop to Phase 4.
     - Requirement ambiguities → feedback loop to Phase 2.
  4. Produce `docs/test-evaluation-report.md`.
- **Exit Gate:** All critical tests pass; test coverage threshold satisfied; zero open blocker defects.

### Phase 7: Operational Deployment & Maintenance
- **Objective:** Transition software to the production environment and manage post-release enhancements.
- **Agent Action:**
  1. Execute automated release migration scripts and operational health checks.
  2. Document operational runbooks and baseline configurations.
  3. Handle maintenance requests by treating enhancements as controlled mini-cycles through the requirements-design-code-test sequence.
- **Exit Gate:** Software operational; telemetry reporting healthy status.

---

## Royce's 5 Remediation Rules

To prevent waterfall failure, the agent must enforce Royce's five foundational rules:

1. **Program Design Comes First**: Spend substantial effort designing storage, execution timing, and interface boundaries before coding.
2. **Document the Design**: Maintain explicit design documents (`docs/detailed-design.md`) so design decisions outlive transient context.
3. **Do It Twice**: Build a throwaway pilot or prototype whenever sizing, timing, or tech stack assumptions are unverified.
4. **Plan, Control, and Monitor Testing**: Test planning begins in the requirements phase, executed systematically against pre-agreed criteria.
5. **Involve the Customer Formally**: Schedule explicit customer / human checkpoints at Requirements sign-off, Preliminary Design review, and Final Acceptance.
