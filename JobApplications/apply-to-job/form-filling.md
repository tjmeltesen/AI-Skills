# Form Filling and Site Navigation Guide

Comprehensive reference for navigating Applicant Tracking Systems (ATS), entering form data accurately, handling portal idiosyncrasies, and avoiding data-loss traps during job application workflows.

## 1. ATS Schema Inspection & Authentication

### API-First Inspection
- **Greenhouse & Ashby**: When available, inspect application forms via their public endpoints first before initiating browser automation:
  - **Greenhouse**: `https://boards-api.greenhouse.io/v1/boards/<company>/jobs/<job-id>`
  - **Ashby**: `https://api.ashbyhq.com/posting-api/job-board/<company>`
- Inspecting schemas via API reveals required fields, custom dropdown options, and validation formats without risking unintended form submissions or DOM side effects.

### Authentication & Gateways
- **Manual Sign-in Walls**: Career portals such as Workday, Y Combinator Work at a Startup, iCIMS, and TikTok require user account creation, manual credentials, or CAPTCHA solving. Flag these to the candidate early so authentication can be completed interactively.
- **Verification Codes**: Greenhouse and other ATS platforms frequently dispatch one-time security codes via email or SMS. Escalate these immediately to the candidate rather than timing out.

---

## 2. Field Entry & Autofill Pitfalls

### Autofill Hazards
- **Greenhouse Autofill**: Do not rely on Greenhouse's automated "Autofill" feature. If a field fails validation or rejects an entry, clear the field and retype the value explicitly.
- **Ashby Resume Autofill**: Avoid using "Autofill from resume" on Ashby portals. It frequently overwrites preferred contact details or primary email addresses with raw text extracted from resume headers.
- **Ashby Unmarked Requirements**: Yes/No toggle buttons on Ashby boards often omit visual required indicators (asterisks). Inspect and answer every Yes/No toggle explicitly to prevent submission failure.
- **Workday State Persistence**: In Workday's "My Experience" section, saving one entry can silently drop or clear previously entered work history or internship entries. Always perform a verification check confirming all experience records remain intact after saving.

### Dropdown & Option Fallbacks
- **Nearest Semantic Match**: When a dropdown does not provide the candidate's exact qualification or source (e.g., a specific engineering major like Computer Engineering / ECE, or a referral source like "Other"), select the closest semantic category (e.g., "Engineering" or "Job Board > LinkedIn") and explicitly flag the substitution in the application review.
- **Education & GPA Mapping**:
  - Distinguish strictly between completed degrees and in-progress degrees.
  - If a form requires a GPA tied to an ongoing or in-progress degree with no cumulative GPA established yet, select "N/A" or "Other".
  - If a dropdown uses fixed decimal increments (e.g., 0.1 intervals) and the exact GPA is unavailable, round conservatively to the lower increment.
- **Truthfulness Guardrail**: Never claim tools, frameworks, programming languages, or domain expertise not explicitly verified in `job-work/profile.md`. Flag unverified requirements for user clarification instead of guessing.

---

## 3. Dynamic Form Volatility & Submission Safety

### Pre-Submission Verification
- **Dynamic Field Clearing**: Single-page application (SPA) forms frequently wipe input fields upon blur, validation, or DOM re-rendering events. Conduct a complete, non-reloading field-by-field verification pass immediately prior to submission.
- **Do Not Reload**: Never reload an active application page while filling out a form, as page reloads reset in-progress state and wipe user entries.

### Confirmation & Logging
- **Artifact Capture**: Immediately capture and log submission artifacts (such as a confirmation number, timestamped status log, or full-page confirmation screenshot) to record proof of application.

### Emergency Abort
- **Immediate Stop**: If the user issues a STOP command, immediately halt all automated browser actions, form interactions, and pending submissions without completing subsequent steps.

---

## 4. Continuous Runtime Improvement

Agents executing this skill must iteratively improve this document as new portal behaviors are observed:
- **Record Newly Discovered Quirks**: When encountering new ATS platforms, undocumented form field behaviors, novel validation traps, session timeouts, or auth workflows during runtime, update this document with concise, actionable instructions.
- **Strict Privacy Guardrail**: NEVER add personal names, contact info, specific candidate answers, application dates, or individual identifiers. Keep all entries strictly generalized to portal architecture, DOM behavior, and universal form-filling knowledge.
- **Maintain Structure**: Integrate new learnings under the existing numbered sections or append discrete, high-signal subsections rather than duplicating existing rules.
