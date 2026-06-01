---
description: Generate a non-binding LOI draft for a deal (draft for counsel review)
argument-hint: "{deal}"
---

Use the **deal-documents** skill to produce an LOI for deal: **$ARGUMENTS**

Pull price/SDE/multiple/financing from `holdco/deal-flow/$ARGUMENTS/analysis.md` and company/broker
from its `README.md`, fill the LOI template, and write
`holdco/deal-flow/$ARGUMENTS/loi-draft-{date}.md` (new dated file). Flag any value you cannot source
as `[CONFIRM]`.

⚖️ Output is a non-binding draft — not legal advice. Have counsel review before sending.
