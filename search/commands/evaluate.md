---
description: Quick go/no-go read on a deal (independent second opinion)
argument-hint: "{deal}"
---

Give a fast go/no-go read on deal: **$ARGUMENTS**

If `holdco/deal-flow/$ARGUMENTS/analysis.md` already exists, summarize the decision: thesis,
financial verdict (adjusted SDE, multiple, DSCR, financeability), top red flags, fit score, and
recommended next action. Otherwise run a lightweight version of the **acquisition-analysis** screen.

For an independent check, you may invoke the **deal-evaluator** agent (read-only) for a second
opinion before concluding.

Also draft the buyer cover letter to `holdco/deal-flow/$ARGUMENTS/correspondence/cover-letter-{date}.html`
(branded HTML → save/export as PDF; see the acquisition-analysis skill's "Buyer cover letter"). Draft to
review before sending.
