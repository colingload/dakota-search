# Analysis Framework — the 12-section deal screen

This is the method behind Steps 3-5. The `analysis.md` template in `assets/` has
the empty structure; this file explains how to fill each section well and what
"good" looks like. Read it before running a financial analysis.

The governing idea: a CIM is a sales document. Rebuild the earnings from primary
sources, defend every adjustment, and show your number next to the seller's with
the gap explained. The gap is the analysis.

## Section-by-section

**1. Deal Snapshot.** Asking vs. our-view vs. delta for: purchase price, SDE (TTM),
EBITDA (TTM), SDE multiple, EBITDA multiple, revenue (TTM), revenue CAGR (3Y),
gross margin. Add an industry benchmark-multiple line (see below). The snapshot is
the executive's one-glance table — every number should trace to a later section.

**2. Business Quality (score 1-5).** Revenue type (recurring / project /
transactional / mixed, with %), contract length, customer count, customer
concentration (top 5 / top 10), employee count + key-person risk, competitive
moat. Project-based revenue with no contractual lock-in caps the score; recurring
or contracted revenue with diversified customers earns a 4-5.

**3. Revenue Quality.** 3 years + TTM table: revenue, YoY%, gross profit, GM%, and
adjusted EBITDA if known. Then break down concentration by customer, product/line,
and end-market; the one-time vs. recurring split; and pricing power (recent price
increases, average unit value trend). Any single-year revenue swing >15% is a
diligence-critical item — get the owner's attribution and a way to verify it
(NOAA weather data, backlog conversion, monthly signed-contract trend, etc.).

**4. Earnings Quality — the core.** Two tables. First, reported vs. CIM-adjusted vs.
our-view for revenue, COGS, gross profit, opex, owner comp, owner add-backs,
non-recurring items, adjusted EBITDA, adjusted SDE. Second, an add-back-by-add-back
table rating each for defensibility (see the catalog below). Then a written
"material concerns" block flagging anything the CIM doesn't reconcile — related-party
income, depreciation that vanished, owner draws inconsistent with the normalized
salary, pre-sale true-ups. This section is where deals are won or killed.

  - **SDE vs. EBITDA.** SDE = adjusted EBITDA + one full market replacement-manager
    salary (the buyer-operator takes the owner's seat, so they don't pay a GM). Use
    SDE for owner-operator deals under ~$1-1.5M; use adjusted EBITDA when a manager
    must be hired. Always state which you're using and why.
  - **Replacement owner comp.** The CIM normalizes owner salary to make EBITDA look
    big. Replace it with a realistic market wage for the work actually done in the
    buyer's geography (e.g., a $10M+ labor business needs a real GM, not a $150K
    figure). The delta between the CIM's normalized comp and yours is usually the
    single biggest systematic difference between your EBITDA and theirs — call it out.

**5. Working Capital & CapEx.** Net working capital (avg) and as % of revenue; the
peg/target NWC at close; maintenance capex run rate (3Y avg) vs. growth capex; A/R
and A/P aging health. Labor/service businesses carry little NWC; equipment-heavy
ones need a real maintenance-capex assumption that lenders will haircut EBITDA for.

**6. Balance Sheet.** Cash-free / debt-free? Assumed liabilities? Off-balance-sheet
items (operating leases, earnouts, multi-employer pension withdrawal liability —
this last one is a deal-killer if unquantified). Owner draws and related-party
receivables tell you how cash actually left the business.

**7. SBA Financing Fit.** Run `scripts/sba_model.py` (see `sba-model.md`). Show the
sources & uses stack, the DSCR by year at proposed terms, and the max-supportable
price at the buyer's target DSCR. State the verdict plainly: financeable at asking,
financeable only at a lower price (give the number), or not financeable.

**8. Seller & Transition.** Why selling (and is it the real reason?), urgency,
post-close involvement offered, training period, rollover-equity willingness, key
employees staying. Simultaneous retirement of both owners with no #2 in place is a
high key-person risk; a seller willing to carry a standby note and stay 12 months
is a strong signal.

**9. Operating Thesis — first 100 days.** 30-day quick wins, 60-day systems/controls
to install, 90+-day growth levers, required hires. Keep it concrete and tied to
what the diligence actually revealed.

**10. Risks & Red Flags.** Severity-ranked (H/M/L) table with a mitigation for each.
Pull the financial red flags from Section 4, the concentration risks from Section 3,
and the transition risks from Section 8.

**11. Dakota Fit Scorecard (score /35).** Seven criteria, 1-5 each — rubric below.

**12. Decision.** Pass / More info / Submit IOI-LOI / Walk after LOI, with the
reason, the next action, owner, and due date. If recommending a price, state it and
tie it to the DSCR math.

## Add-back defensibility catalog

Rate every add-back. Green = include, Yellow = include only with documentation,
Red = exclude from the conservative buyer-adjusted number.

| Add-back | Default rating | Test |
|----------|----------------|------|
| Owner W-2 salary above market replacement | Green (the excess) | Replace with market GM wage; add back only the difference |
| Owner personal expenses run through the co. (auto, travel, meals, insurance) | Yellow | Needs itemization + documentation; haircut undocumented portions |
| One-time / non-recurring (legal settlement, move, IT build) | Yellow | Get the invoice; confirm it truly won't recur |
| Related-party / management-fee income | Red | Buyer does not inherit it; strip it out entirely |
| Related-party rent below market | Red (adjust down) | Buyer pays market rent post-close; this REDUCES earnings |
| ERC / PPP / COVID grants | Red | One-time government money; never recurring |
| Gain on sale of assets (Form 4797) | Red | Non-operating; exclude |
| Depreciation / amortization | Green (add back to EBITDA) | But confirm it's real; $0 D&A on an asset-heavy co. is a red flag, not a gift |
| "Normalized" owner comp the CIM invents | Yellow | Only credible if it matches the actual workload and market |
| Discretionary bonuses to family on payroll | Yellow | Add back only if those roles genuinely go away |

When in doubt, compute two numbers: the CIM's adjusted EBITDA and a conservative
buyer-adjusted EBITDA that includes only 100%-verifiable add-backs. Present both.

## Multiple benchmarks (lower-middle-market, owner-operated)

These are screening anchors, not appraisals — sub-$3M EBITDA blue-collar / essential
services typically transacts in these ranges; adjust for the specific business.

- **Home/trade services (plumbing, HVAC, electrical, roofing, landscaping):** ~3-5x
  SDE / ~3.5-5x EBITDA. Recurring service contracts push toward the top.
- **Specialty / project construction (post-frame, installers):** ~3-5x adj EBITDA;
  a premium (6x+) requires recurring revenue, customer diversification, or strategic
  synergy. Residential-heavy, project-based, owner-dependent caps the multiple.
- **Recurring-revenue services (security/guarding, monitoring, route-based):** ~3.5-5x
  SDE; contracted recurring revenue supports the higher end.
- **General rule:** more recurring + more diversified + less owner-dependent = higher
  multiple. Declining revenue, concentration, or a simultaneous-retirement transition
  argues the multiple down hard.

## Dakota Fit Scorecard rubric (1-5 each, /35 total)

1. **Industry fit** (blue-collar / essential services): 5 = squarely in thesis;
   1 = outside it.
2. **Size fit** ($500K-$2M SDE sweet spot): 5 = in the band; 1 = far above/below.
3. **Geography:** 5 = local/operable; 1 = remote/hard to run.
4. **Recurring / defensible revenue:** 5 = contracted recurring, diversified; 1 = 100%
   project, concentrated.
5. **Owner transition feasibility:** 5 = strong #2, seller stays, clean handoff; 1 =
   both owners retiring at once, no bench.
6. **SBA financeability:** 5 = clears target DSCR with room at asking; 1 = fails DSCR
   even at a discount.
7. **Value-creation upside:** 5 = obvious operational/growth levers; 1 = already
   optimized or structurally limited.

Total maps roughly: 28-35 strong / pursue; 21-27 conditional / depends on price and
diligence; below 21 likely pass. The score is a discipline, not an oracle — the
written thesis and the DSCR verdict carry more weight than the number.
