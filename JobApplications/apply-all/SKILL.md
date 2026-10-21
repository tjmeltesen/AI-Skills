---
name: apply-all
description: >-
  Batch process and draft applications for open roles in job-work/jobs.md.
  Cross-checks job-work/applied.md to avoid duplicate applications and enforce
  cooldown limits. References and updates profile coverage history over time.
  Stops for user review and approval before submitting.
trigger: /apply-all
argument-hint: "[optional limit count or company filter]"
compatibility: Requires job-work/jobs.md, job-work/applied.md, job-work/profile.md, and job-work/answers.md
role: "Batch Application Orchestrator"
allowed-tools:
  - read_file
  - write_file
  - edit_file
enable-write-tools: true
enable-subagent-tools: false
paths:
  - "job-work/jobs.md"
  - "job-work/applied.md"
  - "job-work/profile.md"
  - "job-work/answers.md"
  - "JobApplications/apply-to-job/form-filling.md"
requires:
  skills:
    - apply-to-job
    - job-search
version: "1.0.0"
author: "TJ Meltesen"
license: "MIT"
category: "career"
repository: "https://github.com/tjmeltesen/AI-Skills"
tags:
  - jobs
  - career
  - application
  - batch
  - orchestration
metadata:
  short-description: "Batch application workflow with profile coverage tracking"
---

# Apply all

Batch orchestrator for discovered postings listed in `job-work/jobs.md`. Iterates through pending positions, drafts tailored application answers using `apply-to-job` standards, checks `job-work/applied.md` to prevent duplicate submissions, and updates `job-work/profile.md` coverage to track company limits and pipeline progress over time.

Always stops for user review and explicit approval before submitting any application materials.

## Commands

Text after the command is an optional batch size limit or company filter.

| Runtime | Command |
| --- | --- |
| Claude Code | `/apply-all [limit or filter]` |
| Cursor | `/apply-all [limit or filter]` |
| Grok Build, Grok Bot | `/apply-all [limit or filter]` |
| Codex, ChatGPT | `$apply-all` then limit or filter |

If no argument is given, processes all pending roles in `job-work/jobs.md`.

## Shared state

- **Discovered roles**: `job-work/jobs.md`. Bulleted list of open postings written by `job-search`.
- **Applied tracking**: `job-work/applied.md`. Log of submitted applications read to prevent duplicate applications and enforce company cooldowns.
- **Candidate profile**: `job-work/profile.md`. Single source of truth for resume facts; tracks application history and coverage over time.
- **Answer cache**: `job-work/answers.md`. Shared approved answers for non-resume recurring questions.
- **Navigation guide**: `JobApplications/apply-to-job/form-filling.md`. General ATS quirks, field entry guidelines, and verification rules.

## Steps

1. Read `job-work/jobs.md`. If missing or containing no pending roles, stop and prompt the user to run `/job-search` first.
2. Read `job-work/applied.md` (if present) and `job-work/profile.md`. Load all previously applied companies, URLs, and cooldown dates.
3. Filter `job-work/jobs.md` for entries marked `- Status: pending`. Exclude any role already logged in `job-work/applied.md` or where company application limits (e.g. annual limits or single-application limits) are reached.
4. For each eligible pending role (up to the requested batch limit):
   a. Extract title, company, location, and listing URL.
   b. Inspect listing questions and group by semantic meaning.
   c. Match answers against `job-work/profile.md` and `job-work/answers.md`.
   d. Flag any unmapped questions or required essay drafts for user review.
   e. Present the batch drafts in the reply.
5. Stop and wait for explicit user approval.
6. Upon user approval:
   a. For approved roles being submitted, follow portal guidelines in `JobApplications/apply-to-job/form-filling.md`.
   b. Log each completed submission into `job-work/applied.md` with company, title, date, URL, and status.
   c. Update `job-work/profile.md` under `## Application history` to maintain reliable coverage over time.
   d. Update the role's status in `job-work/jobs.md` from `pending` to `applied`.
7. Return a summary of processed applications, remaining pending roles, and company cooldown statuses.

## Batch reply format

```markdown
# Batch Draft Review

Roles queued: {count}

## 1. {Title} — {Company}
- URL: {URL}
- Location: {Location}
- Answers from profile:
  - {Question}: "{Answer}"
- Answers from shared cache:
  - {Question}: "{Answer}"
- Needs user input:
  - {Question}: [Draft proposal]

---

## Approval Gate
- [ ] Stated facts match candidate profile
- [ ] Answers match shared answer cache
- [ ] No company application limits exceeded
- [ ] User approved submitting this batch
```

## Rules

- Never submit an application without explicit user approval.
- Always cross-check `job-work/applied.md` before drafting to ensure no company is double-applied.
- Update `job-work/applied.md` immediately upon approved submission.
- Update `job-work/profile.md` application history to maintain coverage tracking across sessions.
- Update `job-work/jobs.md` entry statuses to reflect pipeline progress (`pending` -> `drafted` -> `applied`).
- If the user says STOP, immediately halt all batch automation.
- During runtime, update `JobApplications/apply-to-job/form-filling.md` with any newly discovered ATS behaviors.
