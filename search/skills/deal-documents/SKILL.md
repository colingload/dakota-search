---
name: deal-documents
description: >-
  Generate acquisition deal documents — a buyer-side mutual NDA and a non-binding
  Letter of Intent (LOI) — for a specific deal under deal-flow/. Use when the user
  says "sign an NDA", "generate / draft an LOI", "send an LOI for {deal}", "NDA for
  {deal}", or otherwise needs a deal document drafted. Fills a tokenized template
  with terms pulled from {deal}/analysis.md and {deal}/README.md, writes a NEW dated
  draft into the deal folder, and flags any value it cannot source as [CONFIRM].
  Outputs are drafts for attorney review — NOT legal advice. Do NOT use for analyzing
  financials (that is the acquisition-analysis skill).
---

# Deal Documents — NDA & LOI generation

> ⚠️ **SCAFFOLD — not yet fully implemented.** The frontmatter trigger is live, but the
> templates and fill logic are TODO (planned build session). If invoked now, explain the
> intended behavior below and offer to build it, rather than fabricating a document.

> ⚖️ **Not legal advice.** Every document this skill produces is a draft to be reviewed by
> qualified counsel before sending or signing. This disclaimer must appear in every output.

## Intended behavior

Two documents, both written to the target deal folder `holdco/deal-flow/{deal}/`:

### `/search:nda {deal}` — buyer-side mutual NDA
1. Fill `templates/nda.template.md` (parties, confidential-info scope, permitted use, term,
   non-solicit, governing state, effective date).
2. Write `holdco/deal-flow/{deal}/correspondence/nda-{slug}-{date}.md` (never overwrite —
   new dated file each time).
3. Set `NDA signed: Y — {date}` in `{deal}/README.md`.
4. Append a one-line note to `{deal}/discussion-log.md`.

### `/search:loi {deal}` — non-binding LOI
1. Read `{deal}/analysis.md` (§1 price/SDE/multiple, §7 financing stack, §12 recommendation)
   and `{deal}/README.md` (company, broker) to source the terms.
2. Fill `templates/loi.template.md` (asset purchase; seller-note standby/subordinated tranches
   sized for the SBA equity injection; working-capital peg; exclusivity; non-binding except
   the specified sections).
3. Write `holdco/deal-flow/{deal}/loi-draft-{date}.md` (matches the existing naming
   convention; never overwrite).
4. Flag every value not found in the deal files as `[CONFIRM]` so the user fills it in.

## TODO (build session)
- [ ] Author `templates/loi.template.md` — generalize from
      `holdco/deal-flow/2026-05-28-cw-limited-flooring/loi-draft-2026-06-01.md` and the LOI
      templates in `holdco/reference/sba-lender-materials/` (SMB Law Asset Purchase LOI,
      "Copy of LOI Template - MAKE A COPY.md/.docx").
- [ ] Author `templates/nda.template.md` — standard buyer-side mutual NDA (no clean source exists).
- [ ] Distill `references/loi-guide-notes.md` from `EBIT - LOI Guide (Final).pdf` and
      `references/nda-guidance.md`.
- [ ] Implement the fill + dated-write + README/log update logic above.
- [ ] No-script fallback: this skill is pure templating (no Python) — works the same in Cowork.
