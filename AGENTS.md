# AI-Skills

AI-Skills is a modular repository of composable agent skills and workflows following the open Agent Skills specification.

## Repository Overview

Skills are organized into specialized domain folders at the repository root:

- **[`JobApplications/`](JobApplications/AGENTS.md)**: Skills for parsing resumes, shortlisting job postings, and tailoring job applications.
- **[`swe/`](swe/AGENTS.md)**: Software Engineering Process Models, spanning modern Agentic SDLCs (A-SDLC, Spec-Driven Dev, MetaGPT Multi-Agent SOP, SWE-Agent Loop) and classical literature foundations (Waterfall, V-Model, Spiral, Scrum, Cleanroom).

## Agent Guidelines & Standards

When developing, editing, or executing skills in this repository:

1. **Folder & File Convention**:
   - Each skill lives in its own directory: `<Category>/<skill-name>/SKILL.md`.
   - The directory name must match the frontmatter `name` in lowercase kebab-case.
2. **Skill Frontmatter**:
   - Every `SKILL.md` must begin with YAML frontmatter containing `name` and a model-facing `description` stating trigger conditions.
3. **Validation**:
   - Run `python scripts/validate-skills.py` locally before committing. All PRs must pass the `validate-skills` CI check.
4. **Pull Requests**:
   - PRs must follow the format in `.github/pull_request_template.md` (Summary visual/diff, Evidence before/after, Merge Danger assessment).
5. **Process Selection Critique (Agentic-First)**:
   - When initiating software development, the agent must evaluate and critique the task to select the best process model from `swe/`, prioritizing modern agentic frameworks (`swe-agent-loop`, `spec-driven-dev`, `multi-agent-sop`, `agentic-sdlc`) first, falling back to classical models (`v-model`, `waterfall`, `spiral-model`, `cleanroom`, `scrum`) only when specific external constraints dictate. State the selection and justification before writing code.
