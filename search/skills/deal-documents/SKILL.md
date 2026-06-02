---
name: deal-documents
description: >-
  Generate acquisition deal documents — a buyer-side mutual NDA and a non-binding
  Letter of Intent (LOI) — for a specific deal under deal-flow/. Use when the user
  says "sign an NDA", "generate / draft an LOI", "send an LOI for {deal}", "NDA for
  {deal}", or otherwise needs a deal document drafted. Fills a tokenized template
  (clean HTML → PDF) with terms pulled from {deal}/analysis.md and {deal}/README.md — the
  LOI section by section with your sign-off — writes a NEW dated draft into the deal folder, and
  flags any value it cannot source as [CONFIRM].
  Outputs are drafts for attorney review — NOT legal advice. Do NOT use for analyzing
  financials (that is the acquisition-analysis skill).
---

# Deal Documents — NDA & LOI generation

> ⚠️ **PARTIAL.** The **LOI runs in-model now** (`/search:loi`) — HTML template +
> the section-by-section fill below, exported to PDF the same way. The **NDA is still a
> scaffold** (template + fill logic TODO); if it's invoked, explain the intended behavior and offer
> to build it rather than fabricating a document.

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

### `/search:loi {deal}` — non-binding LOI (section-by-section, with your sign-off)
Clean, standard HTML letter from `templates/loi.template.html`, filled **section by section** so the user
verifies each block before moving on. Output is `{deal}/loi-draft-{date}.html` → export PDF (same as
the cover letter). Anything that can't be sourced is written as `[CONFIRM]`.

**Sources.** `{deal}/README.md` (company, broker, **Offer value (LOI basis)**) and
`{deal}/analysis.md` (§7 financing stack, §12 decision + locked value). The Purchase Price **is** the
locked Offer Value; the cash / SBA / seller-note split comes from the SBA model in §7. Buyer name +
contact are static (Colin Gload).

**Fill flow — three blocks. Attempt each field, then ask the user to confirm/edit before continuing:**
1. **Parties** — `{{RECIPIENT_NAME}}` + `{{TO_BLOCK}}` (README Broker/Seller; else `[CONFIRM]`),
   `{{COMPANY_NAME}}`, `{{BUYER_ENTITY}}` (acquisition NewCo), `{{SELLER_ENTITY}}` (Company, LLC).
2. **Price & structure** (from the locked Value + §7 SBA model) — `{{PURCHASE_PRICE}}` (= Offer
   Value), `{{MULTIPLE}}` (= price ÷ SDE), `{{SDE}}`, `{{CASH_AT_CLOSE}}`/`{{CASH_PCT}}`,
   `{{SELLER_NOTE}}`/`{{SELLER_NOTE_PCT}}`, `{{STANDBY_TRANCHE}}`, `{{SUBORD_TRANCHE}}` +
   `{{SUBORD_TERM}}` + `{{SUBORD_RATE}}`. Sanity-check that cash + seller note = Purchase Price.
3. **Terms & timing** (standard defaults — confirm or tweak) — `{{DATE}}` (today),
   `{{ACCEPTANCE_DEADLINE}}` (~5 BD out), `{{EXCLUSIVITY_DAYS}}` (60–90), `{{TRANSITION_DAYS}}`
   (60–90), `{{NONCOMPETE_GEO}}` + `{{NONCOMPETE_YEARS}}` (5). Section 9 timeline ships with standard
   targets — flag if the deal needs different ones.

After the three blocks: write `loi-draft-{date}.html` (never overwrite); export `loi-draft-{date}.pdf`
if a renderer is available (headless Chrome/Edge `--print-to-pdf`, weasyprint, pandoc) else tell the
user to **Print → Save as PDF**; set `Status: LOI` in `README.md`; append a one-line note to
`discussion-log.md`. The legal boilerplate (Sections 1, 5, 6, 10, 11, 12) is **static** — don't edit
it without counsel.

**Deal-by-deal variations** (what changes per deal): ① Parties — recipient, company, buyer entity,
seller entity. ② Price/structure — Purchase Price (the Value), SDE, multiple, cash/SBA/seller-note
split, standby vs. subordinated tranches, note term + rate. ③ Terms/timing — LOI date, acceptance
deadline, exclusivity, transition, non-compete geography + years. Everything else is boilerplate.

## TODO (build session)
- [x] LOI — `templates/loi.template.html` + the section-by-section fill above. Runs in-model.
- [ ] Author `templates/nda.template.html` — buyer-side mutual NDA (HTML → PDF).
- [ ] Implement the NDA fill + dated-write + README/log update logic.
- [ ] Optional: distill `references/loi-guide-notes.md` and `references/nda-guidance.md` from the
      reference materials.
- [ ] No-script note: filling is pure templating (no Python) — works the same in Cowork; PDF export
      needs a renderer (headless browser / weasyprint / pandoc), else Print → Save as PDF.
