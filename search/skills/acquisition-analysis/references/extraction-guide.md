# Extraction Guide — getting clean numbers out of messy financials

Broker financials arrive as scanned tax returns, QuickBooks PDF dumps, and CIM
tables of varying quality. The analysis is only as good as the numbers under it, so
extraction is its own discipline. The goal: a small, trustworthy set of figures per
year that tie across documents.

## What you actually need per year (3 years + TTM)

From the **tax return** (the primary source — Form 1120-S for an S-corp, 1065 for a
partnership, Schedule C for a sole prop):

- Gross revenue (1120-S Line 1a / 1c)
- COGS (Form 1125-A total; Line 2)
- Officer compensation (1120-S Line 7) and salaries/wages (Line 8)
- Depreciation (Line 14) and any Section 179 / amortization in the statements
- Interest expense (Line 13)
- Net ordinary business income (Line 21 / 22) — the "OBI"
- Rents (Line 11) — watch for related-party rent
- Other income / deductions statements (where ERC, gains, management fees hide)
- Schedule L (balance sheet), Schedule M-1 (book-tax reconciliation), Schedule M-2
  (distributions / owner draws)

From the **CIM**: the adjusted-EBITDA bridge (Appendix), the add-back schedule, and
the revenue-by-customer / by-line detail.

## Extraction order of operations

1. **Try text extraction first.** Many tax-return PDFs have a text layer. Pull it
   (`pdftotext -layout`, or read the PDF directly) and look for the line items above.
   Save the raw text next to the PDF (e.g., `tax-return-2023.txt`) so you don't
   re-extract.
2. **Fall back to vision-on-images for scans.** Scanned or image-only returns won't
   OCR cleanly, and getting a single digit wrong corrupts the whole model. Render the
   specific pages you need to PNGs and read them with vision:

   ```
   pdftoppm -png -r 200 -f <page> -l <page> input.pdf out_prefix
   ```

   Render the first page of the return (the income/deductions summary), Schedule L,
   Schedule M-1/M-2, Form 1125-A, and any "Statement 1/2" continuation pages that
   itemize Other Income/Deductions. Read the numbers off the images. Keep the page
   images in a `working/_tax-pages/` or `_extracted-pages/` folder.
3. **QuickBooks PDF P&L/BS:** same approach — render to images if the columns don't
   come through as clean text. Watch for cash- vs. accrual-basis labeling.

## Reconciliation discipline — the non-negotiable step

Once extracted, **prove the documents agree**. Build a small table per year:
CIM revenue vs. 1120-S Line 1a; CIM OBI vs. tax-return net income; CIM adjusted
EBITDA vs. your rebuilt number. They should tie within rounding / OCR noise (a $10
difference on a multi-million revenue line is immaterial; a $350K difference is a
finding). Where the CIM and the return diverge, name the cause — ERC backed out,
related-party income added, a gain excluded — and decide whether the buyer inherits
it. A clean reconciliation is what lets you (and the lender) trust the adjusted
EBITDA; an unreconciled one is a red flag in its own right.

## Common traps

- **Officer comp vs. Rents.** On the 1120-S these are adjacent lines (7 and 11);
  it's easy to grab the wrong one off a scan. Cross-check against the M-2
  distributions and any officer-comp statement.
- **Vanishing depreciation.** $0 D&A on an asset-heavy business usually means the
  books aren't closed or it was omitted to inflate EBITDA — flag it, don't bank it.
- **Multi-entity deals.** When two entities operate as one (e.g., an installer + a
  holding co.), extract each separately and eliminate intercompany management fees on
  consolidation, or you'll double-count.
- **TTM vs. fiscal year.** Be explicit about the period each figure covers and how
  many months — the DSCR model prorates the replacement-manager salary by months
  covered.
