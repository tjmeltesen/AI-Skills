---
name: session-start
description: Initialize the AI-Skills framework at the start of every session or after context reset, loading Ponytail and design guidelines before handling the task. Use when starting work with this skill tree.
license: MIT
---

# Session start

Read `../ponytail/SKILL.md` relative to this skill's directory and apply Ponytail
for this session before doing the task. Use the user's requested level, otherwise
`full`; honor a user request to turn it off. If the sibling is unavailable, locate
the installed `ponytail` skill through the host's skill catalog and read it.
Report a missing skill rather than claiming it was loaded.

Also read `../design_rules/design-guidelines/SKILL.md` relative to this skill's
directory and apply its coding preferences alongside Ponytail for this session.
In an installed layout, read `../design-guidelines/SKILL.md` instead. If neither
path is available, locate `design-guidelines` through the host's skill catalog.
Report a missing skill rather than claiming it was loaded. Honor explicit user
requests to change or disable these preferences.

When working in the AI-Skills source repository, follow its root `AGENTS.md` and
the applicable category instructions. Select a process from `swe/` for development.

Pstack is available as an engineering toolkit. When the user requests poteto-mode
or a pstack workflow, read the installed entry skill and the references it reaches.
Adapt host-specific steps only to tools actually available. The host's permissions,
the user's scope, and repository standards govern execution and delegation.

For missing installations in a source checkout, run
`python scripts/bootstrap.py` from its root. This installs the local skill tree
and portable dependencies declared in `config/skills.yaml`. Cursor's native
pstack plugin is configured separately in `.cursor/settings.json`.
An installed skill alone cannot force a host to load this startup skill; add a
startup pointer to the host's project instructions as described in the source
repository's `docs/framework.md`.
