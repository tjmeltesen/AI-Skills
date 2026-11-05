# Cross-agent framework

## Startup and installation contract

Ponytail is bundled at `core/ponytail/` with its MIT license. It therefore installs
with this repository through `npx skills add .` without a second network fetch.
`core/session-start/SKILL.md` loads it and the coding preferences in
`core/design_rules/design-guidelines/SKILL.md` before work starts. Root `AGENTS.md` is the
shared entry point; Claude Code, Gemini CLI, and Cursor have thin host adapters.

These are host integrations, not properties of a model. A model behind an unrelated
API or chat UI does not discover local skills automatically. Startup pointers
instruct compatible hosts to read the skill; they are not executable lifecycle
hooks and cannot guarantee obedience by every model.

For another project, add this instruction to its `AGENTS.md`, to `CLAUDE.md` for
Claude Code, to `GEMINI.md` for Gemini CLI, and to an always-applied Cursor rule:

> At session start and after context reset, locate and read the installed
> `session-start` skill, then apply it before handling the task.

Keep a concrete installed file path in that instruction if the host cannot resolve
skill names. The installed startup skill reaches the sibling `ponytail` and
`design-guidelines` skills; install both alongside `session-start`. User level
changes and requests to change or disable either policy take precedence.

## Bootstrap

`scripts/bootstrap.py` consumes `config/skills.yaml` and runs the documented
`npx skills add` commands without a shell. `--copy` avoids Windows symlink privilege
requirements. Each command must succeed before the next runs; failures exit nonzero.
Re-running refreshes selected skills and can overwrite their installed copies,
so edit authored files here and rerun rather than editing generated copies.

```bash
python scripts/bootstrap.py --check
python scripts/bootstrap.py --dry-run
python scripts/bootstrap.py
python scripts/bootstrap.py --agent codex --agent gemini-cli
python scripts/bootstrap.py --global
```

Project installation targets this checkout; `--global` targets user skill directories.
The manifest selects four agents explicitly instead of installing to every agent.
Installed copies are ignored by Git and the authored skill validator. The CLI's
`skills-lock.json` records portable dependency installs; keep it when generated.
Remote pstack currently tracks `main`; review updates before using them. No package
manager install hook is implied by this YAML file.

The bootstrap normalizes this repository's local lock sources to `.` so the lock
does not depend on a particular machine's checkout path. Codex, Gemini CLI, and
Cursor share `.agents/skills` in the current CLI layout: portable pstack copies can
therefore also be visible to Cursor. Prefer its native plugin entry points there.

## Pstack

Cursor's native plugin is enabled in `.cursor/settings.json` using the structure
[published by upstream](https://github.com/cursor/plugins/blob/main/pstack/automations/benny/FOR_AGENTS.md).
If the host has not resolved it, run these commands in Cursor chat:

```text
/add-plugin pstack
/setup-pstack
```

The bootstrap installs all portable pstack skills for Claude Code, Codex, and Gemini
CLI, including `poteto-mode`'s sibling skills and playbooks. Installing only
`poteto-mode` would leave its cross-skill references unresolved. It is available on
request; Ponytail and design guidelines are the always-loaded policies. Pstack's upstream `poteto-mode` is
explicit-invocation-only and has its own workflow assumptions, so availability does
not silently make it the default process selector.

Claude Code also has a native plugin adapter. To use that instead of portable
skills, omit `claude-code` from the pstack installation's `agents` in the manifest,
remove any previously installed portable pstack copies, then run in Claude Code:

```text
/plugin marketplace add cursor/plugins
/plugin install pstack@cursor-plugins
/pstack:setup-pstack
```

Invoke its native mode as `/pstack:poteto-mode`. Follow
[upstream installation guidance](https://github.com/cursor/plugins/tree/main/pstack)
for plugin updates. The portable path distributes instructions; it does not install
native subagent registrations, hooks, MCP connections, or Cursor features. Codex
and Gemini need host-appropriate tools and delegation when a playbook requires
them. Report an unavailable capability rather than claiming a workflow succeeded.
`cursor-team-kit` is a separate upstream companion for `deslop`, `control-cli`,
and `control-ui`; it is not installed by this bootstrap. Install it when using
workflows requiring those tools. No automations or model subscriptions are enabled.

Repository process selection still applies. Use pstack's task-specific techniques
within the selected `swe/` process and the current user's authorized scope.

## Where YAML belongs

| Location | Purpose | Reader |
| --- | --- | --- |
| `config/skills.yaml` | Install sources, target agents, startup paths | Our bootstrap script; startup paths are validated, while host pointers load the startup skill |
| `<Category>/<skill>/SKILL.md` frontmatter | Portable name, trigger description, supported metadata | Skill-capable hosts |
| `<Category>/<skill>/agents/openai.yaml` | Optional Codex UI metadata and invocation policy | Hosts supporting this metadata; not a cross-host startup hook |
| `.cursor/rules/*.mdc` frontmatter | Rule description, globs, `alwaysApply` | Cursor |
| `.github/workflows/*.yml` | Validation commands and CI jobs | GitHub Actions |

Use the manifest for install changes and the startup skill for behavioral changes.
Arbitrary YAML files have no effect until a script or host reads them. Native plugin
settings stay in the host's JSON format. Prefer shared Agent Skills fields for
portable instructions; existing host-specific fields need not work everywhere.

## Upstream provenance

Ponytail's `SKILL.md` and `LICENSE` were copied unmodified from
[DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) on 2026-11-04.
Update the bundled skill and license together after reviewing upstream changes.
The native Ponytail plugin additionally offers lifecycle hooks and host features;
this integration uses its portable instructions.

Installation flags and agent identifiers were checked against the official
[skills CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)
and [supported agents](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).
