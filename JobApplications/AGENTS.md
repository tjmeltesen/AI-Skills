# JobApplications Agents

Workflow suite for managing end-to-end job hunting: resume ingestion, role shortlisting, application tracking, single-role tailoring, and batch application orchestration.

## Skill Suite

The skills in this directory operate as a sequenced pipeline sharing context through `job-work/`:

| Skill | Role | Key Input / Output |
| --- | --- | --- |
| **[`resume-parse`](resume-parse/SKILL.md)** | Initial Ingestion | Reads raw resume; writes `job-work/profile.md` once. |
| **[`job-search`](job-search/SKILL.md)** | Discovery & Scoring | Reads `job-work/profile.md` + `job-work/applied.md`; saves open roles list to `job-work/jobs.md`. |
| **[`apply-to-job`](apply-to-job/SKILL.md)** | Single Application Drafting | Reads `job-work/profile.md` + `job-work/answers.md` + URL or next pending role from `job-work/jobs.md`; logs to `job-work/applied.md`. |
| **[`apply-all`](apply-all/SKILL.md)** | Batch Application Orchestrator | Iterates over pending roles in `job-work/jobs.md`; cross-checks `job-work/applied.md`; updates profile coverage and logs to `job-work/applied.md`. |

## Workflow Sequence

1. **Step 1 - Profile Creation**:
   - Run `/resume-parse [path or pasted resume]` once at the start to generate `job-work/profile.md`.
2. **Step 2 - Search & Discover**:
   - Run `/job-search [titles, location, URL]` to evaluate postings against profile criteria.
   - Cross-checks `job-work/applied.md` to skip already applied positions and enforce company limits.
   - Saves discovered roles as a structured bulleted list to `job-work/jobs.md` (marked `- Status: pending`).
3. **Step 3 - Application Execution**:
   - **Individual Role**: Run `/apply-to-job [optional URL]` to process a single listing or the next pending role from `job-work/jobs.md`.
   - **Batch Orchestration**: Run `/apply-all [optional limit]` to process all pending roles in `job-work/jobs.md`.
   - Gathers candidate input for unmapped questions and saves approved responses to `job-work/answers.md`.
   - On approved submission, logs entry to `job-work/applied.md`, updates `job-work/profile.md` coverage history, and updates role status in `job-work/jobs.md`.

## Shared State & Guardrails

- **Shared Context Directory (`job-work/`)**:
  - `job-work/profile.md`: Single source of truth for work experience, dates, tools, metrics, and coverage history.
  - `job-work/answers.md`: Stores approved answers to recurring questions not answered by the resume.
  - `job-work/jobs.md`: Bulleted list of discovered roles with pipeline statuses (`pending`, `drafted`, `applied`).
  - `job-work/applied.md`: Historical log of all applied roles, dates, and submission statuses.
- **Truthfulness Guardrail**:
  - Only use stated facts from `job-work/profile.md`. Never infer or hallucinate qualifications, tools, or dates.
- **Approval Gate**:
  - Never submit an application directly. Always stop for user review and explicit approval.
- **Emergency Stop**:
  - Halt all automated browser actions, drafts, and submissions immediately if the user says STOP.
