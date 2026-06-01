---
description: New prospect — clone the deal template, prefill, add a pipeline row
argument-hint: "{Company Name}"
---

Use the **acquisition-analysis** skill, Step 0 (New prospect), for: **$ARGUMENTS**

Clone `holdco/deal-flow/_template/` → `holdco/deal-flow/YYYY-MM-DD-{slug}/` using today's date,
prefill the company name + date in `README.md`, `analysis.md`, and `questions.md`, and add a row to
`holdco/deal-flow/pipeline.md` (Phase: Prospect, metrics TBD).

When done, suggest `/search:dashboard` to sync the new deal to the dashboard.
