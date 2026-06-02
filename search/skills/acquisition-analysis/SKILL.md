---
name: acquisition-analysis
description: >-
  Analyze a small business acquisition target end-to-end for a self-funded /
  SBA 7(a) buyer — rebuild the P&L from messy CIMs and scanned tax returns,
  validate every add-back, compute adjusted SDE/EBITDA, model the SBA financing
  stack and DSCR, score the deal, and produce a go/no-go memo. Use this whenever
  the user is evaluating a company to buy: a CIM or teaser arrives, a broker
  sends financials, or the user says things like "new prospect," "run the
  financial analysis on {deal}," "organize the {deal} inbox," "surface the
  analysis report," "what's the adjusted SDE / EBITDA," "does this deal cover
  debt service," "what DSCR does this support," "what can I pay for this," "is
  this financeable," "score this deal," "log this session," or drops a folder of
  P&Ls, tax returns, or QuickBooks exports for an acquisition. Trigger even when
  the words "SBA," "DSCR," or "add-back" aren't used — any owner-operator buy-side
  diligence on a lower-middle-market business is in scope. Do NOT use for selling
  a business, public-equity research, or personal budgeting.
---

# Acquisition Analysis — Self-Funded / SBA 7(a) Deal Screen

This skill runs the **Dakota Strategy ETA acquisition screen**: the repeatable process for taking a new acquisition target from a pile of broker documents to a defensible go/no-go decision. The buyer is an operator-buyer acquiring **one** blue-collar / essential-services small business with SBA 7(a) financing, not a fund doing dozens of deals. The bar is high and personal — this is the buyer's career and their personal guarantee on the loan.

## Operating principles (these define good work here)

The whole method rests on one idea: **never take the seller's number at face value — rebuild it from primary sources and defend every adjustment.** A CIM exists to sell a business; the adjusted EBITDA in it is the seller's best case. Your job is to reconstruct the real owner-benefit cash flow a buyer would actually inherit, then test whether it services SBA debt with margin to spare.

Concretely, hold to these:

- **Value on adjusted SDE / EBITDA, rebuilt from the bottom up.** Start from the tax return or accountant P&L (primary source), not the CIM bridge. Add back only what you can document and would survive a lender's quality-of-earnings review.
- **Always show your view vs. the seller's, with the delta and the reason.** Every headline number (SDE, EBITDA, multiple, price) gets two columns and an explained gap. The gap *is* the analysis.
- **Reconcile across documents.** CIM vs. tax return vs. QuickBooks vs. bank statements should tie within rounding. Where they don't, that discrepancy is a finding — surface it, don't smooth it over.
- **Add-backs are guilty until proven innocent.** A normalized owner salary, a "one-time" expense, related-party income, or a sudden pre-sale true-up each needs a source document. Flag aggressive or undocumented add-backs explicitly and re-derive a conservative buyer-adjusted number without them.
- **Financeability is a gate, not a footnote.** A deal that doesn't clear DSCR at realistic terms is dead regardless of how nice the business is. Model the stack and compute the max price the cash flow supports.
- **Preserve the diligence trail.** Never edit seller-provided files. Analysis lives in `analysis.md`; questions in `questions.md`; session history in `discussion-log.md`. Append, don't overwrite — flag what changed when re-running on new info.

When the user's framing conflicts with these, follow their lead but say what you'd flag — they own the decision and the guarantee.

## Folder convention

One subfolder per target, named `YYYY-MM-DD-{slug}`, cloned from `_template/`. Inside each deal:

```
{deal}/
├── README.md          # snapshot: headline terms, thesis, current question
├── analysis.md        # the 12-section analysis (the core deliverable)
├── questions.md       # broker/seller Q&A log (open -> answered)
├── discussion-log.md  # append-only session log, newest first
├── cim/               # CIM, teaser, NDA — seller marketing
├── financials/        # P&Ls, tax returns, QB exports, bank stmts (+ working/)
├── correspondence/    # broker emails, call notes
└── inbox/             # raw dumps before sorting
```

The canonical templates ship in this skill's `assets/` folder. If the user already has a `_template/` and a `pipeline.md` in their deal-flow root, use theirs; otherwise seed from `assets/`. Dates are `YYYY-MM-DD`, always today's date when creating a folder.

## The workflow

This is a seven-step loop. The user drives it with short phrases; each step has a clear input and output. Steps 3-5 are the analytical core and where most of the value is — do them thoroughly.

### Step 0 — New prospect

**Trigger:** "New prospect: {Company Name}" (or any sign a new target is entering the pipeline).

Clone `_template/` (or `assets/`) to `YYYY-MM-DD-{slug}/`, prefill name + date in `README.md`, `analysis.md`, `questions.md`, and add a row to `pipeline.md` (Phase: Prospect, metrics TBD).

### Step 1 — Raw dump (the user)

The user drops everything into `{deal}/inbox/` — CIM/teaser PDFs, P&Ls, tax returns, broker emails, screenshots, call notes. Naming doesn't matter; you'll rename on organize.

### Step 2 — Organize the inbox

**Trigger:** "Organize the {deal} inbox."

Read every file in `inbox/`, classify each into `cim/`, `financials/`, or `correspondence/`, and rename to convention (`pnl-2024-annual.pdf`, `tax-return-2023.pdf`, `cim-{broker}.pdf`). **Never edit the originals.** Post a "what I found / what's missing" summary against the standard diligence checklist in `questions.md`.

### Step 3 — Financial analysis (the core)

**Trigger:** "Run the financial analysis on {deal}."

This is the heart of the skill. It has three parts; read `references/analysis-framework.md` for the full method and `references/extraction-guide.md` for getting clean numbers out of scanned returns and QuickBooks dumps.

1. **Extract & reconcile.** Pull revenue, COGS, officer comp, depreciation, interest, and net income for 3 years + TTM from the primary source (tax returns / accountant P&L), and tie them to the CIM. Scanned PDFs that won't OCR cleanly should be rendered to images and read with vision — see the extraction guide. Build a reconciliation table proving the documents agree (or showing exactly where they don't).
2. **Rebuild earnings.** Reconstruct the P&L, then compute **adjusted EBITDA** and **adjusted SDE** with every add-back itemized and rated for defensibility. Replace the seller's normalized owner comp with a realistic market replacement-manager salary for the work actually done. Strip out related-party income, ERC, gains on asset sales, and other non-operating items. Produce **your number next to the seller's number** with the delta explained.
3. **Model the financing.** Run `scripts/sba_model.py` to compute the SBA 7(a) + seller-note + equity stack, the DSCR by year, and the maximum purchase price the cash flow supports at the buyer's target DSCR. This is the #1 thing the user wants right — the script mirrors their Budget Model.xlsx logic so the numbers reconcile. See `references/sba-model.md`.

Populate `analysis.md` section 1 (snapshot), section 3 (revenue quality), section 4 (earnings quality), section 5 (working capital & capex), section 6 (balance sheet), section 7 (SBA financing fit), and section 2 (business quality). Also produce `financials-side-by-side.html` from `assets/financials-side-by-side.template.html` — the Dakota-branded 3-year comparison of cash P&L, balance sheet, and tax return, with anomaly callouts and the H-priority diligence questions.

**Output:** Adjusted SDE/EBITDA (your view vs. seller's), multiple range vs. comps, DSCR at proposed and max-supportable terms, and a clear "is this financeable" verdict.

### Step 4 — Risk & operating thesis

**Trigger:** "Continue with risks and operating thesis" (or runs automatically after Step 3).

Populate `analysis.md` section 8 (seller & transition — why selling, urgency, post-close involvement, training, key-employee retention), section 9 (first-100-days operating thesis), section 10 (severity-ranked risk register with mitigations), and section 11 (Dakota fit scorecard — 7 criteria scored 1-5, total /35). Scorecard rubric is in `references/analysis-framework.md`.

### Step 5 — Decision & report

**Trigger:** "Surface the analysis report for {deal}" (or runs automatically after Step 4).

Populate `analysis.md` section 12 with the recommendation (Pass / More info / Submit IOI-LOI / Walk after LOI). Post an **executive summary** to chat: one-paragraph thesis, 3-5 key insights, 3-5 top concerns, the financial verdict (adjusted SDE, multiple, DSCR, financeability), open H/M/L diligence questions, and the recommended next action with owner and due date. Move H-priority asks into the `questions.md` Open table and update the `pipeline.md` row (fit score, SDE estimate, phase, next action).

### Step 6 — Iterate on new info

**Trigger:** "I added new docs to {deal} inbox — re-run analysis."

Re-run Steps 2-5. Update `analysis.md` in place — **append and flag changes, don't overwrite** prior findings or manual notes. Move answered items in `questions.md` from Open -> Answered with the source.

### Step 7 — Log the session

**Trigger:** "log" (or "log this").

Append a dated entry (newest at top) to `{deal}/discussion-log.md`: topic, key findings (substantive numbers/mechanisms/anomalies — skip ephemeral chat), deliverables produced, broker correspondence (paraphrased Q's/A's), and decisions/next steps. The log lets the user pick a deal back up cold weeks later or brief a partner.

## Bundled resources

Read these as needed — don't load everything up front:

- `references/analysis-framework.md` — the 12-section analysis template, the add-back defensibility catalog, the Dakota fit scorecard rubric, multiple benchmarks, and what "good" looks like for each section. **Read this for Step 3 and Step 4.**
- `references/sba-model.md` — how the SBA financing model works (sources & uses, guaranty-fee tiers, weighted-average term, full-standby seller notes, DSCR), and how to run `scripts/sba_model.py`. **Read this for Step 3 part 3.**
- `references/extraction-guide.md` — getting clean numbers out of scanned tax returns, QuickBooks PDF exports, and CIM tables; the vision-on-images fallback; reconciliation discipline. **Read this when financials won't OCR cleanly.**
- `scripts/sba_model.py` — the SBA financing calculator. Computes DSCR by year, sources & uses, guaranty fee, and the max-supportable price solve. Run `python scripts/sba_model.py --help`.
- `assets/` — the canonical deal-folder templates (`analysis.md`, `questions.md`, `discussion-log.md`, `README.md`) and the `financials-side-by-side.template.html`.

## Command cheat sheet

| Stage | Say |
|-------|-----|
| New deal | "New prospect: {name}" or `/search:new-deal {name}` |
| Files dropped | "Organize the {deal} inbox" |
| Financials | "Run the financial analysis on {deal}" |
| Risk + thesis | "Continue with risks and operating thesis" |
| Full report | "Surface the analysis report for {deal}" |
| New info | "I added new docs to {deal} inbox — re-run analysis" |
| Compare two | "Compare {deal A} and {deal B} on the fit scorecard" |
| Save session | "log" |
