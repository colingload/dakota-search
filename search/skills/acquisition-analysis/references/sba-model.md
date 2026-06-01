# SBA Financing Model — how to run it

`scripts/sba_model.py` is the financing engine for Section 7. It mirrors the Dakota
"Budget Model.xlsx" logic so its DSCR, Sources & Uses, and guaranty fee reconcile
with the lender workbook. It answers the two questions that decide a deal:

1. **At this price and structure, what's the DSCR?** (forward mode)
2. **What's the most I can pay and still clear my target DSCR?** (`--solve-price`)

Nothing here is lending advice — it's an underwriting estimate to confirm with the
lender. Always note that in the writeup.

## The math it replicates

- **Sources** = SBA 7(a) term loan + seller note + buyer equity, as % of the
  acquisition price. Default stack is **80 / 10 / 10** (matches the workbook).
- **Uses** = business acquisition + real estate + M&E + transaction expenses + SBA
  guaranty fee + working capital.
- **Debt service** = SBA term-loan payment (amortizing PMT) + LOC interest-only +
  seller-note payment. A **full-standby seller note contributes $0** during the
  standby period (SBA's first-24-months-no-payments rule), so year-1 DSCR uses
  only the SBA loan + LOC. The tool prints both the standby DSCR and the
  post-standby DSCR so you see the step-down.
- **SBA guaranty fee:** guaranteed portion is 75% for $700K-$5M 7(a) loans; fee is
  3.5% on the first $1M of the guaranteed portion and 3.75% on the balance (smaller
  tiers handled too).
- **DSCR** = adjusted EBITDA / total annual debt service. SBA floor is 1.25x; the
  workbook's display threshold is 1.5x; the buyer generally wants comfortable room.

## Defaults (override as the deal requires)

SBA rate 8.5%, SBA term 120 months, equity 10%, seller note 10% at 6% / 60mo on full
standby, transaction expenses $26,000, target DSCR 1.5x, LOC $0. The workbook's TGI
deal used a 117-month SBA amortization and a $200K interest-only LOC — pass
`--sba-term-months 117 --loc 200000` to reproduce it exactly.

## Usage

Forward (DSCR at a given price), with a labeled multi-year EBITDA stream; the last
value is the year-1 gate:

```
python scripts/sba_model.py --price 3600000 \
  --ebitda "2023=505656,2024=774106,2025=837261" \
  --sba-term-months 117 --loc 200000
```

Solve for the max supportable price at a target DSCR:

```
python scripts/sba_model.py --ebitda 837261 --solve-price --target-dscr 1.5 \
  --sba-term-months 117 --loc 200000
```

Other useful flags: `--no-seller-standby` (seller note amortizes from day one),
`--finance-fees` (gross the SBA loan up to fund fees + working capital),
`--real-estate` / `--me-purchase` (separate use lines, which also affect the
auto weighted-average term if you set `--sba-term-months 0`), `--equity-pct`,
`--seller-note-pct`, `--sba-rate`, `--seller-rate`, `--seller-term-months`,
`--working-capital`. Run `--help` for the full list.

## Feeding it good inputs

The EBITDA you pass should be the **conservative buyer-adjusted EBITDA** from Section
4 — not the CIM number — so the DSCR reflects reality. Run it at both the CIM EBITDA
and your buyer-adjusted EBITDA to show the lender the range. If a deal only clears
DSCR on the CIM number, say so explicitly; that's a finding.

## The formal deliverable

The script produces the numbers for `analysis.md` Section 7 and the chat summary.
The **lender-facing deliverable is still the populated Budget Model.xlsx** — the
script is the fast, deterministic check that the workbook's DSCR is right and that
the price makes sense before you spend time in Excel. When the user wants the formal
workbook, populate their existing Budget Model.xlsx (P&L tab line items, Sources &
Uses inputs) with the same figures; the script's output should tie to it.
