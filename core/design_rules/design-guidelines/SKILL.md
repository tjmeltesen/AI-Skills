---
name: design-guidelines
description: Apply the user's architecture and coding preferences when writing, refactoring, or reviewing code, including organization, generalization, object design, and stable contract tests.
---

# Design guidelines

Apply these preferences alongside Ponytail. Follow explicit task requirements
and project constraints; surface material conflicts before choosing a design.

## Atomic organization

Group folders by feature, domain, or service. Each folder owns a cohesive
capability with a clear interface. Build larger capabilities from these units.

Each file owns one cohesive responsibility. Each function performs one
cohesive operation at a consistent level of abstraction.

Keep handwritten source and test files within 500 physical lines after
formatting, including comments and blank lines. Exclude generated files.

Generally keep 1–3 classes per file. Function-only modules are appropriate.
Split by responsibility and ownership, rather than arbitrary chunks or
wrappers introduced solely to satisfy the limits.

## Generalization and consistent flows

Inspect the known use cases before choosing an abstraction. Generalize their
shared behavior behind a small interface; keep meaningful differences explicit.

Build abstractions around demonstrated common behavior. Each abstraction
should simplify its callers or centralize a shared rule.

Similar operations should follow recognizable patterns for input, validation,
processing, results, and errors. Where user journeys are involved, keep similar
interactions consistent too. Share implementation when the behavior is shared.

## Functions, objects, and inheritance

Use functions for transformations and classes for state with related behavior.
Keep state with the operations responsible for preserving its invariants.

Prefer composition when assembling capabilities. Use inheritance when
implementations can satisfy the same behavioral contract and callers can
substitute them without special handling.

## Minimal checks

Validate external input at system boundaries. Within those boundaries, trust
established types and invariants.

Write the minimum implementation that satisfies known behavior. Add internal
conditions for demonstrated cases, including failures found during testing.
Trace a failure to its cause before adding a defensive branch.

Preserve protections needed for security and preventing data loss.

## Stable contract tests

Define observable behavior at the shared interface. Run the same contract
tests against each implementation using fixtures or parameterization.

Keep tests stable when implementation details change. Change the contract
tests when intended behavior changes, rather than to accommodate refactoring.

Add focused tests for distinct behavior and regressions. Avoid duplicating
coverage for every new helper, class, or implementation detail.

## Verify the design

Before finishing, inspect changed files for cohesion, formatted line counts,
class organization, consistent flows, and justified abstractions.

Run the relevant behavior and contract tests. Report any unmet guideline
and its concrete reason.
