# Changelog

Notable changes to the Dakota Search plugin. Newest first.

## 2026-06-01 · Plugin — command renames, Gmail routine, cover letter + LOI, Offer Value

**Goal:** Tighten the deal commands and build document generation end-to-end.

**Did:**
- **Command renames:** `/search:new` → `/search:new-deal` (scaffold + pipeline row, then wait for
  inbox drops — dropped the dashboard nudge); `/search:report` → `/search:decide`;
  `/search:morning` → `/search:gmail`.
- **Gmail routine** (`/search:gmail [deal]`): fuzzy label→deal matching (closest label by name, not a
  rigid `Deals/{slug}`); pull email to backfill README headline terms + move `questions.md`
  Open→Answered; refresh `correspondence/email-timeline.md` (added to the deal template); catalog
  attachments (Gmail MCP exposes `attachment_ids` but has no get-attachment tool — catalog only).
  Documented one-deal vs. sweep-all modes + scheduling. `deal-pipeline` → PARTIAL (Gmail runs
  in-model; dashboard sync still TODO).
- **Buyer cover letter:** Dakota-branded HTML → PDF (`acquisition-analysis/assets/cover-letter.template.html`),
  auto-drafted during analyze/evaluate; recipient = broker (else `[CONFIRM]`), one tailored line from
  the thesis.
- **LOI:** plain HTML → PDF (`deal-documents/templates/loi.template.html`, matching the original
  document's look — intentionally not branded), filled section-by-section (Parties → Price/Structure →
  Terms/Timing) with sign-off via `/search:loi`. `deal-documents` → PARTIAL (LOI live; NDA scaffold).
- **Offer Value:** locked at `/search:decide` → README "Offer value (LOI basis)" + analysis §12; the
  LOI Purchase Price pulls from it, with the cash / SBA / seller-note split from the SBA model (§7).
- **Housekeeping:** removed two raw root input files (folded into templates); fixed stale references;
  updated README, `marketplace.json`, `plugin.json`.

**Next:** NDA template (last deal-document); dashboard sync (Apps Script `doPost` + `build_dashboard.py`);
flesh out the `deal-evaluator` agent; optional live sample PDF render of the cover letter + LOI.

**Commits:** `39179c6`, `ea0fa29`, `82a5336` (+ this entry) — pushed to `origin/main`.
