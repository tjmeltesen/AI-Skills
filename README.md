# AI-Skills

A shared skill tree for Claude Code, Gemini CLI, Codex, and Cursor.
Authored skills live in `<Category>/<skill-name>/SKILL.md`.

## Set up this checkout

Requires Python with `requirements.txt` installed, Node.js 22.20+, npm, and Git.

```bash
python -m pip install -r requirements.txt
python scripts/bootstrap.py --dry-run
python scripts/bootstrap.py
```

The bootstrap installs this tree (including Ponytail) for all four hosts and
pstack's portable skills for Claude Code, Codex, and Gemini. Cursor uses its
native pstack plugin, enabled by `.cursor/settings.json`; if it does not resolve,
run `/add-plugin pstack` in Cursor, then `/setup-pstack`.

Ponytail is loaded at session start through `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
and Cursor's always-applied rule. The user can change its level or turn it off.

## Install the skill tree elsewhere

```bash
npx skills add tjmeltesen/AI-Skills -g
```

From this checkout, use `npx skills add . -g`, or `python scripts/bootstrap.py --global`
to also install portable pstack dependencies. In Windows PowerShell, use `npx.cmd`
if script execution policy blocks `npx`.

`skills add` copies skills; it does not execute our bootstrap, install native
plugins, or copy root instruction files. For automatic startup in another project,
add a pointer to the installed `session-start` skill in that project's host
instructions. See [framework setup and YAML locations](docs/framework.md).

Validate authored skills with `python scripts/validate-skills.py`.
