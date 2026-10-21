---
name: cleanroom
description: >-
  Execute formal defect-prevention software engineering using Box Structure
  Specification, mathematical correctness verification, and statistical usage
  testing based on Mills, Dyer, and Linger (1987). Use when ultra-high
  reliability, life-critical safety, or near-zero defect density is mandatory.
trigger: /cleanroom
argument-hint: "[increment or box-structure component]"
compatibility: Requires formal specification storage at docs/cleanroom/**; developer execution prohibited
model: pro
context: inherit
role: "Cleanroom Verification Engineer"
allowed-tools:
  - read_file
  - write_file
  - edit_file
disallowed-tools:
  - run_command
enable-write-tools: true
enable-subagent-tools: false
paths:
  - "docs/cleanroom/**"
version: "1.0.0"
author: "TJ Meltesen"
license: "MIT"
category: "swe"
repository: "https://github.com/tjmeltesen/AI-Skills"
tags:
  - cleanroom
  - mills-1987
  - formal-methods
  - box-structures
  - zero-defects
metadata:
  short-description: "Mills, Dyer, and Linger's formal defect-prevention lifecycle"
  paper: "Cleanroom Software Engineering (Mills, Dyer, & Linger, 1987)"
---

# Cleanroom Software Engineering

Execute software engineering through mathematical rigor, formal defect prevention, and statistical quality certification. Based on Dr. Harlan D. Mills, Michael G. Dyer, and Richard C. Linger's 1987 IEEE Software paper *"Cleanroom Software Engineering"*.

> **Core Axiom:** Borrowed from semiconductor cleanrooms, the fundamental philosophy is **defect prevention, not defect removal**. Software must be engineered correctly the first time through formal specification and mathematical correctness verification. Developers do not run unit-test debug cycles; software correctness is proven before execution, and testing is reserved for statistical reliability certification.

## Commands

| Runtime | Command |
| --- | --- |
| Claude Code | `/cleanroom [step or component]` |
| Cursor | `/cleanroom [step or component]` |
| Grok Build | `/cleanroom [step or component]` |
| Codex, ChatGPT | `$cleanroom` then the step or component |

## The 4 Cleanroom Steps

```text
1. Incremental Engineering Plan
           │
           ▼
2. Box Structure Specification
   ├─ Black Box (External Stimulus ──> Response)
   ├─ State Box (Stimulus + State ──> Response + Next State)
   └─ Clear Box (Procedural Control Structures)
           │
           ▼
3. Formal Correctness Verification (Axiomatic Proofs & Questions)
   [NO DEVELOPER EXECUTION / DEBUGGING ALLOWED]
           │
           ▼
4. Statistical Usage Testing & MTBF Reliability Certification
```

---

### Step 1: Incremental Engineering Planning
- **Objective:** Partition the total software capability into small, accumulative increments where each increment delivers executable functionality and is certified before the next is designed.
- **Agent Action:**
  1. Structure system delivery into increments: Increment 1 (core foundation), Increment 2 (extended capabilities), Increment $N$ (final system).
  2. Define the explicit mathematical boundary and interface contract for each increment in `docs/cleanroom/increment-plan.md`.
  3. Ensure each increment builds directly on top of previously certified increments.

### Step 2: Box Structure Specification
- **Objective:** Model software transitions using Box Structure Theory across three levels of mathematical abstraction:
- **Agent Action:**
  1. **Black Box Specification (`docs/cleanroom/black-box.md`)**:
     - Model system behavior purely as a function of external stimulus history to response: $S^* \rightarrow R$.
     - Encapsulate all internal state; specify solely what the system does observable from the outside.
  2. **State Box Specification (`docs/cleanroom/state-box.md`)**:
     - Introduce the minimal internal state variables needed to retain memory of past stimuli: $(S \times State) \rightarrow (R \times State')$.
     - Formally define state transitions and invariant constraints.
  3. **Clear Box Specification (`docs/cleanroom/clear-box.md`)**:
     - Decompose the state box into procedural control structures using only provably verifiable primitives:
       - **Sequence**: $P \;; Q$
       - **Alternation**: `if Condition then P else Q`
       - **Iteration**: `while Condition do P`
       - **Concurrent / Sub-box invocation**

### Step 3: Formal Correctness Verification
- **Objective:** Rigorously verify that the Clear Box code mathematically satisfies the State and Black Box specifications *without executing the code*.
- **Agent Action (The Cleanroom Strictness Rule):**
  1. **Prohibit Developer Debugging**: Code is not compiled or run to find bugs. Running code shifts developer psychology from careful mathematical thought to trial-and-error guessing.
  2. Execute the **Correctness Question Protocol** for every control structure (`docs/cleanroom/correctness-verification.md`):
     - **Sequence ($P \;; Q$)**: Does $P$ establish the precondition required for $Q$?
     - **Alternation (`if C then P else Q`)**: When $C$ is true, does $P$ satisfy the specification? When $C$ is false, does $Q$ satisfy the specification?
     - **Iteration (`while C do P`)**:
       - *Termination*: Is there a well-founded metric decreased by every execution of $P$?
       - *Loop Invariant*: Is the invariant maintained across every iteration?
       - *Postcondition*: When $C$ becomes false, does the invariant imply the required result?
  3. Conduct an independent verification review. Only when all correctness proofs pass is the increment permitted to be compiled.

### Step 4: Statistical Usage Testing & Reliability Certification
- **Objective:** Certify the operational reliability and Mean Time Between Failures (MTBF) of the software through scientific statistical sampling.
- **Agent Action (The Independent Certification Team):**
  1. Build an **Operational Profile** (`docs/cleanroom/operational-profile.md`):
     - Model the probability distribution of real-world user behaviors, environmental inputs, and operational sequences.
  2. Generate randomized, representative test sequences matching the operational profile.
  3. Execute the tests in an isolated clean environment.
  4. Track failures mathematically using statistical models:
     - Record failure intervals.
     - Calculate Mean Time to Failure (MTTF) and Mean Time Between Failures (MTBF).
  5. Produce the **Reliability Certification Report** (`docs/cleanroom/reliability-certificate.md`).
- **Completion Criterion:** Certified reliability meets or exceeds the required target (e.g., $MTBF \ge 10,000$ operational hours with 99% confidence).
