# Reliable Job Discovery Guide

Heuristics, ATS API patterns, and verification practices for finding and scoring open positions reliably.

## 1. Direct ATS API Endpoints

Querying structured ATS endpoints is faster, less prone to scraping failures, and returns raw listing schemas without HTML noise:

### Greenhouse Public API
- **Endpoint**: `https://boards-api.greenhouse.io/v1/boards/<company>/jobs?content=true`
- **Output**: Returns full job objects, departments, locations, and raw posting content in structured JSON.

### Ashby Public API
- **Endpoint**: `https://api.ashbyhq.com/posting-api/job-board/<company>?includeCompensation=true`
- **Header Requirement**: Ashby blocks requests that omit a browser `User-Agent`. Always supply a standard browser `User-Agent` header (e.g., `Mozilla/5.0...`) when querying Ashby endpoints to avoid HTTP 403 Forbidden responses.

### Enterprise & Proprietary Portals
- Large enterprises (e.g., Google, Amazon, NVIDIA, Salesforce, Mastercard) typically manage listings through Workday or custom career portals rather than public board APIs. Search and navigate their career portals directly.

---

## 2. Verification & Listing Freshness

### Live Status Verification
- Job postings—particularly entry-level, new-grad, and early-career roles—close rapidly without warning.
- Always perform an HTTP check or verify that the posting is currently open and accepting submissions before shortlisting or presenting the role.
- Remove dead or expired postings immediately. Never invent or hallucinate postings, compensation numbers, or application links.

### Fine Print Eligibility Audit
Always audit the posting's fine print against the candidate profile before recommending:
- **Degree Level Restrictions**: Verify if the program is restricted strictly to Bachelor's candidates, accepts Master's candidates, or requires an accelerated degree format.
- **Graduation Windows**: Ensure the candidate's graduation date matches the required cohort start date (e.g., distinguishing between immediate starts, Winter/December cohorts, and Spring/Summer cohorts).
- **Work Authorization & Clearance**: Check for requirements such as US Person status (ITAR/EAR compliance), active security clearances, or strict non-sponsorship policies.

---

## 3. Application Limits & Pre-Screening

### Company Application Limits
- Track company-specific application limits and cooldown periods before submitting:
  - Some companies restrict candidates to a single active new-grad application per recruiting season.
  - Others enforce rolling caps (e.g., maximum of 3 applications within a 12-month window).
- Flag repeat applications to the same employer for candidate confirmation before proceeding.

### Mandatory Upfront Assessments
- Detect and flag roles that require immediate, pre-interview assessments (such as automatic coding challenges or take-home assignments) before recruiter or engineering review.
- Notify the candidate upfront so they can decide whether to commit time to the assessment before applying.

### Shortlist Volume & Category Balancing
- Active listings for highly specialized early-career titles (e.g., dedicated AI/Agentic Engineering roles) may be limited at any given time.
- When generating candidate shortlists, pad the selection with high-relevance general new-grad software engineering roles with AI/systems overlap, and explicitly note where padding was used.

---

## 4. Continuous Runtime Improvement

Agents executing this skill must iteratively improve this document as new discovery sources and platform behaviors are learned:
- **Record Discovery Heuristics**: When discovering new ATS API endpoints, custom request headers, query parameters, rate limits, or platform pagination mechanisms during runtime, update this document with concise, actionable instructions.
- **Strict Privacy Guardrail**: NEVER record individual candidate names, personal criteria, specific job match logs, or personal notes. Keep all entries strictly generalized to job discovery techniques, endpoint specifications, and platform mechanics.
- **Maintain Structure**: Merge new endpoints or search heuristics into the existing sections to keep the guide clear and organized.
