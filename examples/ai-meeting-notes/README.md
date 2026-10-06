# Example: AI Meeting Notes SaaS

## Initial idea

> I want to build an AI meeting notes SaaS.

## Coding-first path

A coding agent can immediately produce auth, database schema, transcription integration, dashboard and deployment. Those artifacts can all be technically competent while the product thesis remains untested.

## Product Pro Max path

### 1. idea-pressure-test

Expose unknowns:

- Which meeting segment is underserved?
- Why would users switch?
- Is transcription the pain, or is follow-up/action work the pain?
- Who is buyer versus user?

Gate: **WARN**.

### 2. problem-validation

Require evidence of repeated pain, current workaround, consequence and switching/payment signal.

With no customer evidence: **FAIL → research**.

### 3. customer-research

Suppose interviews reveal that small recruiting agencies manually turn interview notes into candidate scorecards.

That is stronger evidence than "people need better meeting notes".

### 4. icp-positioning

Narrow ICP:

> Recruiting agencies with 5–30 recruiters conducting structured interviews and manually producing candidate summaries.

### 5. mvp-scope

Build now:

- capture/import interview transcript;
- generate scorecard against role rubric;
- reviewer correction;
- export/share.

Explicitly not building:

- generic meeting assistant;
- calendar platform;
- knowledge base;
- broad analytics;
- mobile app.

## Lesson

The best output may be less code. The system should discover that before implementation cost compounds.
