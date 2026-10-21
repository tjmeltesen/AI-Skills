---
name: v-model
description: >-
  Execute dual-track systems development with symmetric decomposition and
  verification based on Forsberg & Mooz (1991). Use for safety-critical,
  embedded, or regulated engineering where every design specification level
  requires an explicit, pre-planned verification test suite.
trigger: /v-model
argument-hint: "[system specification or verification level]"
compatibility: Requires test planning directory at tests/plans/** and documentation at docs/v-model/**
model: inherit
context: inherit
role: "V&V Systems Verification Engineer"
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - run_command
enable-write-tools: true
enable-subagent-tools: false
paths:
  - "docs/v-model/**"
  - "tests/plans/**"
version: "1.0.0"
author: "TJ Meltesen"
license: "MIT"
category: "swe"
repository: "https://github.com/tjmeltesen/AI-Skills"
tags:
  - v-model
  - verification
  - validation
  - traceability
  - safety-critical
metadata:
  short-description: "Forsberg & Mooz dual-track Verification and Validation lifecycle"
  paper: "The Relationship of System Engineering to the Project Cycle (Forsberg & Mooz, 1991)"
---

# V-Model Process Model

Execute software engineering through symmetric decomposition (the downward left wing) paired with corresponding integration and verification (the upward right wing). Based on Kevin Forsberg and Harold Mooz's 1991 NCOSE/INCOSE foundation paper *"The Relationship of System Engineering to the Project Cycle"*.

> **Core Axiom:** Testing is not an afterthought at the end of development. Every level of specification on the descending wing defines its corresponding verification test suite *concurrently*, before any implementation begins.

## Commands

| Runtime | Command |
| --- | --- |
| Claude Code | `/v-model [phase or scope]` |
| Cursor | `/v-model [phase or scope]` |
| Grok Build | `/v-model [phase or scope]` |
| Codex, ChatGPT | `$v-model` then the phase or scope |

## The Symmetric Vee Structure

```text
User Requirements  ══════════════════════════════════>  User Acceptance Testing
      ↓                                                         ↑
System Specification  ═════════════════════════>  System Verification Testing
      ↓                                                 ↑
Architecture & Subsystem Design  ════════>  Integration & Interface Testing
      ↓                                         ↑
Detailed Component Design  ════════>  Unit / Component Verification
      ↓                                         ↑
      ╚══════════════> Implementation <═════════╝
```

---

## Downward Wing: Decomposition & Definition

### Step 1: User Requirements Definition & Acceptance Test Planning
- **Left Side (Define):** Elicit user needs, operational context, business constraints, and regulatory standards. Produce `docs/v-model/user-requirements.md`.
- **Right Bridge (Plan):** Concurrently author the **User Acceptance Test (UAT) Plan** (`tests/plans/acceptance-test-plan.md`). Define operational scenarios, user workflows, and pass/fail thresholds.
- **Completion Criterion:** Requirements are verifiable; UAT scenarios are documented before system architecture begins.

### Step 2: System Specification & System Test Planning
- **Left Side (Define):** Translate user needs into functional system specifications, non-functional performance bounds, telemetry needs, and environmental limits. Produce `docs/v-model/system-specification.md`.
- **Right Bridge (Plan):** Concurrently author the **System Test Plan** (`tests/plans/system-test-plan.md`). Specify end-to-end data flows, load thresholds, failure recovery modes, and security benchmarks.
- **Completion Criterion:** System specification is complete and traced 1:1 to system test cases.

### Step 3: Architecture / Subsystem Design & Integration Test Planning
- **Left Side (Define):** Decompose the system into distinct subsystems, services, communication protocols, and interface contracts (APIs, schemas, message formats). Produce `docs/v-model/architectural-design.md`.
- **Right Bridge (Plan):** Concurrently author the **Integration Test Suite** (`tests/plans/integration-test-plan.md`). Define contract tests, mock boundaries, and network fault tolerance tests.
- **Completion Criterion:** Interface boundaries are frozen; integration test harnesses are ready to execute once components exist.

### Step 4: Detailed Component Design & Unit Test Planning
- **Left Side (Define):** Specify the internal algorithms, data structures, error handling, and state machines for individual components/classes. Produce `docs/v-model/detailed-design.md`.
- **Right Bridge (Plan):** Concurrently write the **Unit Test Cases** (`tests/plans/unit-test-spec.md`). Define branch coverage criteria, boundary values, and nominal input expectations.
- **Completion Criterion:** Unit test cases are written prior to code authoring.

---

## The Apex: Implementation

### Step 5: Module Implementation (Coding)
- **Objective:** Code components strictly to detailed design specifications and passing static analysis.
- **Agent Action:** Write clean, modular, typed code. Validate against linter and compiler bounds.
- **Completion Criterion:** Code compiles with zero warnings/errors and is ready for upward wing verification.

---

## Upward Wing: Integration & Verification

### Step 6: Unit / Component Verification
- **Objective:** Verify component code against detailed design specifications.
- **Agent Action:** Execute the unit test suite authored in Step 4. Validate branch coverage, edge cases, and deterministic execution.
- **Completion Criterion:** 100% of unit tests pass; code coverage meets or exceeds threshold.

### Step 7: Subsystem Integration & Interface Testing
- **Objective:** Verify interactions, communication protocols, and interface contracts between assembled components.
- **Agent Action:** Execute the integration test suite authored in Step 3. Verify protocol compliance, data marshalling, and error propagation across boundaries.
- **Completion Criterion:** All component seams and interface contracts verified with zero regression.

### Step 8: System Verification Testing
- **Objective:** Verify the integrated whole against system-level functional and non-functional requirements.
- **Agent Action:** Execute the system test suite authored in Step 2. Verify end-to-end system throughput, latency, security controls, and recovery behaviors.
- **Completion Criterion:** Full system passes all system-level tests in a production-like staging environment.

### Step 9: Acceptance & Operational Validation
- **Objective:** Validate that the completed system fulfills real user needs in the target operational environment.
- **Agent Action:** Execute the UAT scenarios authored in Step 1 alongside human stakeholders. Measure real-world performance against operational success criteria.
- **Completion Criterion:** Formal human sign-off on user acceptance; system ready for deployment.

---

## Bidirectional Traceability Matrix

Every V-Model project must maintain a traceability matrix (`docs/v-model/traceability-matrix.md`):

| User Req ID | System Spec ID | Architecture ID | Component ID | Unit Test | Integration Test | System Test | Acceptance Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `UR-001` | `SYS-010` | `ARCH-AUTH` | `TokenParser` | `UT-AUTH-01` | `IT-AUTH-01` | `ST-AUTH-01` | `UAT-LOGIN-01` |

If a requirement lacks a corresponding test case at its matching tier, the stage gate is blocked.
