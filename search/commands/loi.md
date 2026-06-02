---
description: Generate a non-binding LOI draft for a deal (draft for counsel review)
argument-hint: "{deal}"
---

Use the **deal-documents** skill to produce an LOI for deal: **$ARGUMENTS**

Fill `templates/loi.template.html` **section by section, pausing for the user to confirm
or edit each block** before moving on — (1) Parties, (2) Price & structure, (3) Terms & timing. The
**Purchase Price is the locked Offer Value** (README "Offer value (LOI basis)" / `analysis.md` §12);
the cash / SBA / seller-note split comes from the SBA model (§7); company/broker from `README.md`.
Flag anything you can't source as `[CONFIRM]`.

When the three blocks are confirmed, write `holdco/deal-flow/$ARGUMENTS/loi-draft-{date}.html` (new
dated file; never overwrite) and export `loi-draft-{date}.pdf` if a renderer is available, else tell
the user to **Print → Save as PDF**. Set `Status: LOI` in `README.md` and log a one-line note.

⚖️ Output is a non-binding draft — not legal advice. The legal boilerplate is static; have counsel
review before sending.
