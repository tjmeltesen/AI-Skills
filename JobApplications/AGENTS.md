# JobApplications Agents

Workflow suite for managing end-to-end job hunting: resume ingestion, role shortlisting, and application drafting.

## Skill Suite

The skills in this directory operate as a sequenced pipeline sharing context through `job-work/`:

| Skill | Role | Key Input / Output |
| --- | --- | --- |
| **[`resume-parse`](resume-parse/SKILL.md)** | Initial Ingestion | Reads raw resume; writes `job-work/profile.md` once. |
| **[`job-search`](job-search/SKILL.md)** | Discovery & Scoring | Reads `job-work/profile.md` + job listing; shortlists matches. |
| **[`apply-to-job`](apply-to-job/SKILL.md)** | Application Drafting | Reads `job-work/profile.md` + `job-work/answers.md`; drafts responses. |

## Workflow Sequence

1. **Step 1 - Profile Creation**:
   - Run `/resume-parse [path or pasted resume]` once at the start.
   - Do not re-parse the resume unless the user explicitly requests an update.
2. **Step 2 - Search & Match**:
   - Run `/job-search [titles, location, URL]` to evaluate postings against stated profile criteria.
3. **Step 3 - Draft Application**:
   - Run `/apply-to-job [listing]` to match questions by meaning and generate draft responses.

## Shared State & Guardrails

- **Shared Context Directory (`job-work/`)**:
  - `job-work/profile.md`: Single source of truth for work experience, dates, tools, and metrics.
  - `job-work/answers.md`: Stores approved answers to recurring questions not answered by the resume.
- **Truthfulness Guardrail**:
  - Only use stated facts from `job-work/profile.md`. Never infer or hallucinate qualifications, tools, or dates.
- **Approval Gate**:
  - Never submit an application directly. Always stop for user review and explicit approval.
