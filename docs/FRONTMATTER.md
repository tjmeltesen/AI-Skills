# Complete Guide to YAML Frontmatter Options for Agent Skills & CLI Rules

This reference documents the YAML frontmatter options, directives, and metadata fields supported across major AI CLI assistants, agent runners, and coding environments (including the open **[agentskills.io](https://agentskills.io)** standard, **Anthropic Claude Code**, **Google Antigravity**, **Cursor Rules (`.mdc`)**, **Windsurf / Cascade**, and **OpenHands/OpenDevin**).

---

## Table of Contents
1. [Architecture & Progressive Disclosure](#architecture--progressive-disclosure)
2. [Open Agent Skills Standard (`agentskills.io`)](#1-open-agent-skills-standard-agentskillsio)
3. [CLI & Autonomy Controls (Claude Code, Antigravity)](#2-cli--autonomy-controls-claude-code-antigravity)
4. [IDE & Context Rules (Cursor, Windsurf / Cascade)](#3-ide--context-rules-cursor-windsurf--cascade)
5. [Execution Context & Subagent Dispatch](#4-execution-context--subagent-dispatch)
6. [Tool Access & Least-Privilege Guardrails](#5-tool-access--least-privilege-guardrails)
7. [Dependencies & Environment Requirements](#6-dependencies--environment-requirements)
8. [Package & Registry Metadata](#7-package--registry-metadata)
9. [Comprehensive Master Reference Table](#8-comprehensive-master-reference-table)
10. [Production-Ready Boilerplates](#9-production-ready-boilerplates)

---

## Architecture & Progressive Disclosure

In modern AI agent platforms, skills are packaged in modular directories containing a primary `SKILL.md` (or `.mdc` in Cursor):

```text
skills/my-skill-name/
├── SKILL.md             # Required: YAML frontmatter + Markdown instructions
├── scripts/             # Optional: Bash/Python helpers executed by the agent
├── references/          # Optional: Secondary manuals loaded on-demand
└── assets/              # Optional: Templates, schemas, or static files
```

### The Progressive Disclosure Lifecycle:
1. **Startup Discovery**: When initializing, the agent scans available skills and loads **only** the YAML frontmatter (`name` and `description`).
2. **Context Preservation**: The main instruction body and referenced files are withheld from the active LLM context window to prevent token bloat and attention degradation.
3. **Dynamic Activation**: When the agent's semantic matcher or the human (via a slash command) triggers the skill, the full Markdown body and relevant helper pointers are loaded into the prompt context.

---

## 1. Open Agent Skills Standard (`agentskills.io`)

The [agentskills.io](https://agentskills.io) open standard defines portable, cross-platform skills supported across Anthropic Claude, Microsoft Visual Studio, GitHub, and open-source agent runtimes.

```yaml
---
name: dataset-publishing
description: Publish datasets to Hugging Face Hub. Use when uploading datasets, creating dataset cards, or managing dataset versions.
license: Apache-2.0
compatibility: Requires Python 3.8+ and huggingface_hub >= 0.16
metadata:
  author: ml-platform-team
  version: "1.0.0"
allowed-tools: "Bash(hf:*) Python(huggingface_hub:*)"
---
```

### Standard Specification Fields:

* **`name`** *(string, required)*:
  * **Constraints**: 1–64 characters. Lowercase letters (`a-z`), numbers (`0-9`), and single hyphens (`-`). Must not start or end with a hyphen, and cannot contain consecutive hyphens (`--`).
  * **Requirement**: Must match the parent folder name exactly (`skills/<name>/SKILL.md`).
* **`description`** *(string, required)*:
  * **Constraints**: 1–1024 characters.
  * **Purpose**: Explains both **what** the skill does and **explicitly when** the model should invoke it. Used by the agent's semantic router.
* **`license`** *(string, optional)*:
  * An SPDX license identifier (e.g., `MIT`, `Apache-2.0`, `GPL-3.0`) or a relative path pointing to a bundled `LICENSE` file.
* **`compatibility`** *(string, optional)*:
  * **Constraints**: Max 500 characters.
  * Details system prerequisites, required runtimes, network access needs, or specific OS dependencies (e.g., `Requires Docker daemon and Linux x86_64`).
* **`metadata`** *(mapping/object, optional)*:
  * Arbitrary key-value string pairs for auxiliary attributes like `author`, `version`, `category`, etc.
* **`allowed-tools`** *(string or list, optional)*:
  * Space-delimited string or array defining pre-approved tool execution scopes or namespaces (e.g., `"Bash(npm:*) Git(*)"`).

---

## 2. CLI & Autonomy Controls (Claude Code, Antigravity)

These properties control how interactive terminal assistants display autocompletions and manage autonomous execution vs. human-gated actions.

```yaml
---
name: deploy-staging
description: Deploy current branch to staging cluster.
disable-model-invocation: true
argument-hint: "[target-service] [--dry-run]"
trigger: /deploy
---
```

* **`disable-model-invocation`** *(boolean, optional, default: `false`)*:
  * **`true`**: The agent is strictly prohibited from autonomously activating this skill. It can **only** be triggered manually when the user types the slash command (`/deploy-staging`).
  * **Why use it**: 
    1. Prevents high-consequence operations (deployments, git resets, migrations) from running without explicit human intent.
    2. Strips the skill description from the agent's baseline system prompt, incurring **zero continuous token load**.
* **`argument-hint`** *(string, optional)*:
  * Autocomplete / placeholder hint displayed in the terminal UI when the user types the slash command (e.g., `[issue-number]`, `<branch-name>`, or `"Focus area for next session"`).
* **`trigger` / `triggers`** *(string or array of strings, optional)*:
  * Custom slash-command aliases or regex keywords that map to this skill (e.g., `trigger: /graphify` or `triggers: ["/audit", "security review"]`).
* **`user-invoked`** *(boolean, optional)*:
  * Direct synonym for `disable-model-invocation: true` in several CLI distributions.

---

## 3. IDE & Context Rules (Cursor, Windsurf / Cascade)

IDE-based coding assistants use frontmatter to define how and when coding standards, linters, and architectural constraints are attached to code generation.

### Cursor (`.cursor/rules/*.mdc`)
Cursor uses `.mdc` files in the `.cursor/rules/` directory with three primary frontmatter properties:

```yaml
---
description: "Guidelines and safety checks for database migrations"
globs: "src/migrations/**/*.sql, prisma/migrations/**/*.sql"
alwaysApply: false
---
```

* **`description`** *(string)*:
  * Semantic summary used by Cursor's AI when operating in "Apply Intelligently" mode.
* **`globs`** *(string)*:
  * Comma-separated glob patterns specifying which files must be open or active in context for the rule to automatically trigger (e.g., `*.ts, src/components/**`).
* **`alwaysApply`** *(boolean)*:
  * If `true`, the rule is unconditionally loaded into the context of **every** interaction across the entire project.

### Windsurf / Cascade (`.windsurf/rules/*.md`)
Windsurf uses frontmatter to govern rule loading modes and character budgets:

```yaml
---
trigger: glob
globs: "src/api/**/*.ts"
description: "Authentication and authorization middleware constraints"
---
```

* **`trigger`** *(string, enum)*:
  * `always_on`: Injected on every prompt turn (subject to workspace character limits).
  * `glob`: Injected only when interacting with files matching `globs`.
  * `model_decision`: The agent dynamically decides whether to load the rule based on `description`.
  * `manual`: Only loaded when explicitly mentioned by the user with `@rule-name`.
* **`globs`** *(string)*: Glob path filter for `trigger: glob`.

---

## 4. Execution Context & Subagent Dispatch

For advanced agent platforms (like Antigravity, OpenHands, and Agent DAG orchestrators), skills can declare how child sessions or subagents are configured.

```yaml
---
name: deep-refactor
description: Multi-file architectural refactoring
model: pro
context: fresh
workspace: branch
role: "Refactoring Architect"
timeout: 600
is-daemon: false
---
```

* **`model`** *(string, optional)*:
  * Model tier or specific LLM override for running this skill (e.g., `inherit`, `flash`, `pro`, `claude-3-7-sonnet`, `gemini-2.5-pro`, `gpt-4o`).
* **`context`** *(string, enum: `inherit`, `fresh`, `fork`)*:
  * `fresh`: Creates an isolated session with clean context and no history clutter.
  * `fork`: Clones the parent conversation up to the invocation point.
  * `inherit`: Runs inline within the current active session.
* **`workspace`** *(string, enum: `inherit`, `branch`, `share`)*:
  * `inherit`: Executes directly in the active project working tree.
  * `branch`: Spins up an isolated git worktree or branch to prevent dirtying the main working tree.
  * `share`: Shares underlying repository state across concurrent agents.
* **`role`** *(string, optional)*:
  * Formal persona or title assigned to the executing subagent (e.g., `"Security Auditor"`).
* **`timeout` / `timeout-seconds`** *(integer, optional)*:
  * Maximum execution limit in seconds before interrupting long-running steps.
* **`is-daemon`** *(boolean, optional, default: `false`)*:
  * Indicates whether the skill spawns an unmonitored persistent background task (e.g., file watcher, dev server).

---

## 5. Tool Access & Least-Privilege Guardrails

Enforces security boundaries and sandboxing by restricting the agent's capabilities while the skill is active.

```yaml
---
name: investigate-logs
description: Read and analyze production log files without modifying the system
tools:
  - read_file
  - search_web
enable-write-tools: false
enable-mcp-tools: true
enable-subagent-tools: false
---
```

* **`tools` / `allowed-tools`** *(list of strings or space-separated string)*:
  * Explicit whitelist of callable tools (e.g., `[read_file, run_command]`).
* **`disallowed-tools` / `disable-tools`** *(list of strings)*:
  * Explicit tool blacklist (e.g., `[write_file, edit_file]`).
* **`enable-write-tools`** *(boolean, optional)*:
  * Quickly enables or revokes permission to create files, edit files, or execute destructive shell commands.
* **`enable-mcp-tools`** *(boolean, optional)*:
  * Toggles access to external Model Context Protocol (MCP) servers.
* **`enable-subagent-tools`** *(boolean, optional)*:
  * Grants or restricts permission to invoke or define child subagents.

---

## 6. Dependencies & Environment Requirements

Declares system binaries, environment variables, or other dependent skills required for execution.

```yaml
---
name: playwright-test-runner
description: Execute Playwright end-to-end integration tests
requires:
  bins:
    - npx
    - playwright
  mcp:
    - github-mcp
  skills:
    - setup-pre-commit
env:
  NODE_ENV: "test"
  CI: "true"
---
```

* **`requires` / `dependencies`** *(mapping or list)*:
  * `bins`: CLI binaries that must be present in `$PATH`.
  * `mcp`: Named MCP servers that must be connected.
  * `skills`: Sibling skills that must exist in the workspace.
* **`env`** *(mapping of string key-values)*:
  * Environment variables required or injected into the execution shell.

---

## 7. Package & Registry Metadata

Used by skill package managers (such as Claw, AgentSmith, ClawHub, and internal enterprise registries) for version tracking and catalog searches.

```yaml
---
version: "2.1.0"
author: "Security Team <secops@example.com>"
maintainer: "Jane Doe (@jdoe)"
license: "Apache-2.0"
homepage: "https://github.com/example/skills"
repository: "https://github.com/example/skills.git"
tags:
  - security
  - audit
  - secrets
category: "devops"
---
```

* **`version`** *(string)*: Semantic versioning string (`MAJOR.MINOR.PATCH`).
* **`author` / `maintainer`** *(string)*: Package author, team, or email.
* **`homepage` / `repository`** *(string)*: Source control or documentation URLs.
* **`tags` / `keywords`** *(list of strings)*: Discoverability labels for skill repositories.
* **`category`** *(string)*: Broad classification (`testing`, `refactoring`, `workflow`, `database`, `swe`, `career`).

---

## 8. Comprehensive Master Reference Table

| YAML Frontmatter Key | Type | Systems / Standard | Primary Purpose |
| :--- | :--- | :--- | :--- |
| **`name`** | String | Universal (`agentskills.io`, Claude, Antigravity) | Unique identifier (max 64 chars, kebab-case); must match folder name. |
| **`description`** | String | Universal | Semantic description defining what it does and **when** to trigger. |
| **`disable-model-invocation`** | Boolean | Claude Code, Antigravity, Open Agents | Blocks autonomous invocation; makes skill slash-command only (`/<name>`). |
| **`argument-hint`** | String | Claude Code, Antigravity | UI placeholder/help text shown in terminal autocomplete for parameters. |
| **`trigger` / `triggers`** | String / Array | CLI Agents, Cascade, Windsurf | Explicit slash commands, aliases, or keyword patterns to activate skill. |
| **`allowed-tools`** | String / Array | `agentskills.io`, Claude, Antigravity | Whitelist of permitted tools or sandboxed command namespaces. |
| **`disable-tools`** | Array | Antigravity, OpenHands | Blacklist of prohibited tools during execution. |
| **`enable-write-tools`** | Boolean | Antigravity, Multi-Agent CLI | Toggles filesystem modification and destructive bash access. |
| **`enable-mcp-tools`** | Boolean | Antigravity, Claude Code | Toggles access to external Model Context Protocol tool endpoints. |
| **`enable-subagent-tools`** | Boolean | Antigravity, Swarm | Toggles permission to spawn subagents. |
| **`globs`** | String / Array | Cursor (`.mdc`), Windsurf (`.md`) | Filepath patterns that auto-attach or scope the rule. |
| **`alwaysApply`** | Boolean | Cursor (`.mdc`) | Injects rule into every single chat session across the repository. |
| **`compatibility`** | String | `agentskills.io` | Max 500 chars describing runtime, OS, and network requirements. |
| **`model`** | String | Antigravity, OpenHands, Workflows | Specific model override (e.g., `flash`, `pro`, `claude-3-7-sonnet`). |
| **`context`** | Enum | Multi-Agent CLI | Context window isolation (`inherit`, `fresh`, `fork`). |
| **`workspace`** | Enum | Antigravity, Orca | Filesystem isolation strategy (`inherit`, `branch`, `share`). |
| **`role`** | String | Agent Runners | Subagent persona/job title. |
| **`timeout`** | Integer | Agent Runners | Timeout duration in seconds. |
| **`requires`** | Mapping | Agent Skills / Plugins | Dependencies (`bins`, `mcp`, `skills`). |
| **`env`** | Mapping | Agent Skills / CLI | Required or injected environment variables. |
| **`metadata`** | Mapping | `agentskills.io` | Arbitrary custom metadata key-values. |
| **`license`** | String | `agentskills.io`, Package Registries | SPDX license code (e.g., `MIT`, `Apache-2.0`). |
| **`version`** | String | Package Registries | Semver release tag (e.g., `1.0.0`). |
| **`tags` / `keywords`** | Array | Package Registries | Search and categorization labels. |
| **`category`** | String | Package Registries | Taxonomy classification. |

---

## 9. Production-Ready Boilerplates

### Pattern 1: Pure Open Agent Skills Standard (`agentskills.io`)
*Strictly portable across web APIs (`claude.ai`), IDEs, and CLI runners.*

```markdown
---
name: huggingface-model-upload
description: Upload PyTorch model checkpoints to Hugging Face Hub. Use whenever the user requests publishing or backing up trained models.
license: Apache-2.0
compatibility: Requires Python 3.10+, torch >= 2.0, and huggingface_hub >= 0.19
metadata:
  version: "1.0.0"
  author: "ML Operations"
allowed-tools: "Bash(python:*) Bash(git:*)"
---

# Instructions
1. Verify model weights exist in `checkpoints/`.
2. Format the model card according to `references/card-template.md`.
3. Push using the helper script `scripts/upload.py`.
```

---

### Pattern 2: Interactive Slash-Command (Claude Code / Antigravity)
*Human-gated with zero baseline context load; auto-prompts user for arguments.*

```markdown
---
name: db-migrate
description: Run database migrations and generate schema diffs.
disable-model-invocation: true
argument-hint: "[--dry-run] [target-version]"
trigger: /migrate
---

# Database Migration Runbook
When the user executes `/migrate`, follow these steps:

1. Inspect pending migration files in `prisma/migrations/`.
2. If `--dry-run` is present, execute `npx prisma migrate diff`.
3. Otherwise, apply migrations with `npx prisma migrate deploy`.
```

---

### Pattern 3: Scoped Workspace Rule (Cursor `.mdc`)
*Automatically activates when editing files matching glob patterns.*

```markdown
---
description: "React server component architecture and data fetching guidelines"
globs: "src/app/**/*.tsx, src/components/**/*.tsx"
alwaysApply: false
---

# React Server Component Standards
- Default to Server Components unless client-side state (`useState`, `useEffect`) is mandatory.
- Never import client-only packages inside server-rendered routes.
```

---

### Pattern 4: Sandboxed Heavy Runner with Subagent Isolation
*Clones a branch worktree, enforces least-privilege tool use, and isolates context.*

```markdown
---
name: security-audit
description: Exhaustive dependency vulnerability and secret audit across git history.
workspace: branch
context: fresh
model: pro
timeout: 1200
role: "AppSec Vulnerability Auditor"
enable-write-tools: false
enable-mcp-tools: true
allowed-tools:
  - run_command
  - read_file
requires:
  bins:
    - trivy
    - gitleaks
---

# Security Audit Protocol
1. Scan git history for committed secrets using `gitleaks detect`.
2. Inspect package dependencies using `trivy fs .`.
3. Generate an audit report artifact at `audit-report.md`.
```
