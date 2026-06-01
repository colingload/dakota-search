---
description: Run the financial analysis + risk/operating thesis on a deal
argument-hint: "{deal}"
---

Use the **acquisition-analysis** skill, Steps 3–4, for deal: **$ARGUMENTS**

Rebuild the P&L from primary sources, compute adjusted SDE/EBITDA (your view vs. the seller's),
model the SBA stack + DSCR, then populate the risk register and operating thesis. Update
`holdco/deal-flow/$ARGUMENTS/analysis.md` (§1–11) and produce `financials-side-by-side.html`.

When done, suggest `/search:report $ARGUMENTS` and `/search:dashboard`.
