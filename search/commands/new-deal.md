---
description: New Deal — clone the deal template, prefill, add a pipeline row, then wait for inbox drops
argument-hint: "{Company Name}"
---

Use the **acquisition-analysis** skill, Step 0 (New prospect), for: **$ARGUMENTS**

Clone `holdco/deal-flow/_template/` → `holdco/deal-flow/YYYY-MM-DD-{slug}/` using today's date,
prefill the company name + date in `README.md`, `analysis.md`, and `questions.md`, and add a row to
`holdco/deal-flow/pipeline.md` (Phase: Prospect, metrics TBD).

When done, confirm the folder + pipeline row are created, then stop and tell the user the deal is
ready: **drop everything — CIM/teaser, P&Ls, tax returns, broker emails — into `{deal}/inbox/`.**
Once files are in, the next step is `/search:organize {deal}`.
