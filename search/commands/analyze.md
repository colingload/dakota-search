---
description: Run the financial analysis + risk/operating thesis on a deal
argument-hint: "{deal}"
---

Use the **acquisition-analysis** skill, Steps 3–4, for deal: **$ARGUMENTS**

Rebuild the P&L from primary sources, compute adjusted SDE/EBITDA (your view vs. the seller's),
model the SBA stack + DSCR, then populate the risk register and operating thesis. Update
`holdco/deal-flow/$ARGUMENTS/analysis.md` (§1–11), produce `financials-side-by-side.html`, and draft
the buyer cover letter to `correspondence/cover-letter-{date}.html` (branded → save as PDF; see the
skill's "Buyer cover letter").

When done, suggest `/search:decide $ARGUMENTS` and `/search:dashboard`.
