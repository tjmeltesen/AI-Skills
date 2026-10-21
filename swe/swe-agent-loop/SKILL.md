---
name: swe-agent-loop
description: >-
  Execute autonomous software engineering and issue resolution based on Princeton's
  SWE-agent (Yang et al., NeurIPS 2024) and the SWE-bench benchmark paradigm.
  Drives systematic issue reproduction, Agent-Computer Interface (ACI) navigation,
  fault localization, minimal surgical patch synthesis, and regression verification.
trigger: /swe-agent-loop
argument-hint: "[issue description, bug report, or issue URL]"
compatibility: Requires test runner and terminal execution in an isolated git worktree/branch
model: pro
context: fresh
workspace: branch
role: "SWE-Agent Autonomous Engineer"
timeout: 900
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - run_command
enable-write-tools: true
enable-subagent-tools: false
paths:
  - "docs/swe-agent/**"
version: "1.0.0"
author: "TJ Meltesen"
license: "MIT"
category: "swe"
repository: "https://github.com/tjmeltesen/AI-Skills"
tags:
  - swe-agent
  - bug-fix
  - autonomous
  - swe-bench
metadata:
  short-description: "Autonomous issue-to-patch resolution loop (SWE-bench / SWE-agent)"
  paper: "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering (Yang et al., 2024)"
---

# SWE-Agent Autonomous Loop

Execute autonomous software engineering, bug fixing, and feature implementation using the **Agent-Computer Interface (ACI)** trajectory methodology. Based on Princeton University's seminal NeurIPS 2024 paper *"SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering"* (Yang, Jimenez, et al.) and the **SWE-bench** evaluation benchmark.

> **Core Axiom:** Autonomous software engineering succeeds not through raw prompting, but through a **disciplined, tool-mediated trajectory**: first isolate the bug into a deterministic reproduction script, navigate code with structured search, synthesize the minimal necessary patch, and verify against regressions.

## Commands

| Runtime | Command |
| --- | --- |
| Claude Code | `/swe-agent-loop [issue description or URL]` |
| Cursor | `/swe-agent-loop [issue description or URL]` |
| Grok Build | `/swe-agent-loop [issue description or URL]` |
| Codex, ChatGPT | `$swe-agent-loop` then the issue |

## The 5-Step Autonomous Resolution Trajectory

```text
1. Issue Ingestion & Context Framing
           │
           ▼
2. Author Reproduction Script / Failing Test (GOES RED)
           │
           ▼
3. ACI Navigation & Fault Localization (Search, Symbol Jump, Trace)
           │
           ▼
4. Minimal Surgical Patch Synthesis (Edit & Self-Correction)
           │
           ▼
5. Dual Verification: Repro Passes (GOES GREEN) & Full Regression Passes
```

---

### Step 1: Issue Ingestion & Context Framing
- **Objective:** Extract the exact failure mode, expected behavior, and reproduction conditions from the issue description.
- **Agent Action:**
  1. Parse the issue text, stack traces, and environment descriptions.
  2. Identify the target subsystem, relevant modules, and potential input vectors.
  3. Summarize the problem statement into `docs/swe-agent/issue-summary.md`.
- **Completion Criterion:** Unambiguous description of: (a) actual broken behavior, and (b) expected correct behavior.

### Step 2: Author Reproduction Script (Go Red)
- **Objective:** Build a minimal, self-contained, automated test or reproduction script that reliably fails on the current codebase.
- **Agent Action (The Golden Rule of SWE-agent):**
  1. Author a reproduction script (e.g. `reproduce_issue.py` or a dedicated test case `tests/test_issue_repro.py`).
  2. Execute the reproduction script in the test environment.
  3. **Verify the Red State:** The reproduction must exit with a non-zero code or failed assertion due to the specific issue, *not* due to environment misconfiguration or missing dependencies.
- **Completion Criterion:** Reproduction script runs deterministically and reproduces the exact reported failure.

### Step 3: ACI Navigation & Fault Localization
- **Objective:** Locate the precise file, class, and line numbers responsible for the failure using Agent-Computer Interface tools.
- **Agent Action:**
  1. Use structured search tools (`grep`, symbol lookup, AST inspection) rather than reading random files.
  2. Trace call graphs backwards from the point of failure / error stack trace.
  3. Inspect variable state, type assumptions, and boundary conditions.
  4. Identify the root cause and document in `docs/swe-agent/root-cause-analysis.md`.
- **Completion Criterion:** Exact lines of code causing the failure identified and verified against the reproduction trace.

### Step 4: Minimal Surgical Patch Synthesis
- **Objective:** Apply the smallest possible, cleanest code change that resolves the bug without side effects.
- **Agent Action:**
  1. Formulate a hypothesis for the fix.
  2. Edit target files with surgical precision. Avoid refactoring unrelated code, reformatting whitespace, or introducing unnecessary dependencies.
  3. If syntax errors or runtime exceptions occur during editing, observe the error feedback and immediately self-correct.
- **Completion Criterion:** Target files edited; code passes local linting and syntax checks cleanly.

### Step 5: Dual Verification & Clean PR Generation
- **Objective:** Prove the fix works and introduce zero regressions to existing capabilities.
- **Agent Action:**
  1. **Reproduction Test:** Run the reproduction script authored in Step 2. It must now pass cleanly (turn **GREEN**).
  2. **Regression Suite:** Run the full existing test suite of the repository. Zero unrelated tests may fail.
  3. **Self-Review:** Inspect the `git diff`. Verify that:
     - No debug statements, `console.log`, or `print` statements remain.
     - The diff contains only code directly related to the issue.
  4. Package the solution into a Pull Request with before/after evidence from Step 2 and Step 5.
- **Completion Criterion:** Repro goes green; entire test suite passes; clean diff prepared for review.
