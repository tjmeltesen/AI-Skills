---
name: spiral-model
description: >-
  Execute risk-driven iterative software engineering based on Barry Boehm (1988).
  Use for complex, high-risk, open-ended systems where uncertainty must be
  retired through progressive prototyping, risk analysis, and stakeholder reviews
  before committing capital to full-scale development.
trigger: /spiral-model
argument-hint: "[spiral cycle number or risk evaluation topic]"
compatibility: Requires prototyping environment and documentation storage at docs/spiral/**
model: pro
context: fresh
workspace: branch
role: "Risk & Prototyping Architect"
timeout: 900
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - run_command
enable-write-tools: true
enable-subagent-tools: true
paths:
  - "docs/spiral/**"
version: "1.0.0"
author: "TJ Meltesen"
license: "MIT"
category: "swe"
repository: "https://github.com/tjmeltesen/AI-Skills"
tags:
  - spiral
  - boehm-1988
  - risk-analysis
  - prototyping
  - iterative
metadata:
  short-description: "Boehm's risk-driven four-quadrant spiral lifecycle"
  paper: "A Spiral Model of Software Development and Enhancement (Boehm, 1988)"
---

# Spiral Process Model

Execute software engineering through risk-driven iterative cycles combining the systematic control of classical engineering with the flexibility of progressive prototyping. Based on Dr. Barry W. Boehm's 1988 IEEE Computer paper *"A Spiral Model of Software Development and Enhancement"*.

> **Core Axiom:** Software process should be driven by risk, not by rigid documents or ad-hoc code sprints. If a requirement or architecture decision carries high uncertainty, that risk must be identified and retired via prototyping and analysis *before* committing to the next level of development.

## Commands

| Runtime | Command |
| --- | --- |
| Claude Code | `/spiral-model [cycle or task]` |
| Cursor | `/spiral-model [cycle or task]` |
| Grok Build | `/spiral-model [cycle or task]` |
| Codex, ChatGPT | `$spiral-model` then the cycle or task |

## The 4 Quadrants (Every Cycle)

Every loop of the spiral traverses four quadrants from the top-left, moving clockwise:

```text
                  Q1: Determine Objectives, Alternatives, Constraints
                                      ▲
                                      │
       Q4: Plan Next Phases           │           Q2: Evaluate Alternatives &
    & Review with Stakeholders        │              Resolve Risks (Prototypes)
──────────────────────────────────────┼──────────────────────────────────────
                                      │
                                      │           Q3: Develop & Verify
                                      ▼               Next-Level Product
```

---

### Quadrant 1: Objectives, Alternatives, & Constraints
- **Objective:** Establish the targets for this iteration, enumerate distinct implementation pathways, and define boundary constraints.
- **Agent Action:**
  1. Define explicit goals for the cycle (e.g., "Verify sub-millisecond query latency under 10k concurrent connections").
  2. List alternative solutions (e.g., Alternative A: Redis cache; Alternative B: Postgres read-replicas; Alternative C: In-memory Trie).
  3. Document system constraints: cost, memory bounds, latency ceilings, backward compatibility.
  4. Write `docs/spiral/cycle-<N>/01-objectives.md`.

### Quadrant 2: Risk Analysis & Prototyping
- **Objective:** Evaluate alternatives, identify critical risk factors, and resolve uncertainties before full development.
- **Agent Action (The Heart of the Spiral):**
  1. Build a Risk Table (`docs/spiral/cycle-<N>/02-risk-analysis.md`):
     - Identify top technical, architectural, or user interface risks.
     - Rate each risk by **Probability** (P) and **Impact** (I).
     - Calculate Risk Exposure: $RE = P \times I$.
  2. Build targeted prototypes, simulations, or benchmarks to resolve the top risk factors.
  3. Measure prototype outcomes against constraints identified in Quadrant 1.
  4. Eliminate inferior alternatives based on empirical measurements.

### Quadrant 3: Develop & Verify Next-Level Product
- **Objective:** Design, implement, and verify the chosen solution increment for this cycle.
- **Agent Action:**
  1. Apply the appropriate development technique for this increment (e.g., TDD, formal specification, or modular coding).
  2. Implement the verified architecture selected in Quadrant 2.
  3. Execute automated test suites, integration tests, and verification checks.
  4. Ensure zero unresolved regressions in `docs/spiral/cycle-<N>/03-development-report.md`.

### Quadrant 4: Review & Plan Next Phase
- **Objective:** Review cycle outcomes with human stakeholders and plan the scope of the next outward loop.
- **Agent Action:**
  1. Present evidence, benchmark results, and working increments to stakeholders.
  2. Conduct a **Life-Cycle Architecture (LCA) / Milestone Review**:
     - *Go / No-Go Decision*: Does the project still justify its investment?
     - Have the primary risks for this phase been retired?
  3. Allocate budget and establish scope for Cycle $N+1$.
  4. Write `docs/spiral/cycle-<N>/04-next-cycle-plan.md`.

---

## The 4 Canonical Outward Loops

The spiral progresses outwards through four standard development cycles:

### Loop 1: Concept & Feasibility Loop
- **Primary Focus:** Business concept, core feasibility, and fundamental technology selection.
- **Risk Mitigation:** Throwaway proof-of-concept prototypes to verify that the core value proposition is technically possible.
- **Milestone:** Life-Cycle Objectives (LCO) Review.

### Loop 2: Requirements & Architecture Loop
- **Primary Focus:** Full software requirements and baseline system architecture.
- **Risk Mitigation:** Architectural prototype (tracer bullets) to prove critical interfaces, database schema viability, and cross-cutting concerns (auth, logging, transport).
- **Milestone:** Life-Cycle Architecture (LCA) Review.

### Loop 3: Construction & Initial Operational Loop
- **Primary Focus:** Detailed design, production implementation, and comprehensive integration testing.
- **Risk Mitigation:** Continuous automated regression testing, integration harnesses, and performance stress testing under production loads.
- **Milestone:** Initial Operational Capability (IOC) Review.

### Loop 4: Operational Deployment & Enhancement Loop
- **Primary Focus:** Production deployment, monitoring telemetry, user feedback, and iterative enhancement.
- **Risk Mitigation:** Rollback automation, canary deployments, and error-budget monitoring.
- **Milestone:** Final Operational Capability & Continuous Evolution.

---

## Risk Decision Rule

```text
IF highest_risk_exposure > tolerance_threshold:
    STOP full implementation.
    Isolate the risk into a spike/prototype in Quadrant 2.
    Measure until risk exposure falls below threshold before advancing.
```
