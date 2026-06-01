#!/usr/bin/env python3
"""
SBA 7(a) acquisition financing model — DSCR, Sources & Uses, and max-price solve.

Mirrors the Dakota Strategy "Budget Model.xlsx" logic so its numbers reconcile
with the lender workbook. Two modes:

  forward  (default): given a purchase price and a financing structure, compute
           the Sources & Uses, SBA guaranty fee, term-loan payment, and DSCR for
           each year of adjusted EBITDA you supply.

  solve    (--solve-price): given an adjusted EBITDA and a target DSCR, compute
           the maximum business-acquisition price the cash flow supports.

KEY MECHANICS (match the workbook):
  - Debt service = SBA term loan + LOC interest-only + seller note (only if NOT
    on full standby; a full-standby seller note contributes $0 to year-1+standby
    debt service, per SBA's first-24-months-no-payments rule).
  - SBA term-loan payment = standard amortizing PMT at the SBA rate over the term.
  - LOC service is interest-only: principal * rate (annual).
  - SBA guaranty fee (loans > 12 mo): on the guaranteed portion (75% for $700K-$5M
    7(a) loans), 3.5% on the first $1,000,000 of the guaranteed portion and 3.75%
    on the balance. Smaller tiers handled too.
  - DSCR = adjusted EBITDA / total annual debt service.

Nothing here is tax or lending advice; it is an underwriting estimate to be
confirmed with the lender.
"""

import argparse
import sys


# ----------------------------- core finance helpers -----------------------------

def pmt(annual_rate, n_months, principal):
    """Monthly amortizing payment (positive number). Matches Excel PMT sign-flipped."""
    if principal <= 0 or n_months <= 0:
        return 0.0
    r = annual_rate / 12.0
    if r == 0:
        return principal / n_months
    return principal * (r * (1 + r) ** n_months) / ((1 + r) ** n_months - 1)


def sba_guaranty_fee(loan_amount):
    """SBA 7(a) guaranty fee for loans with maturity > 12 months.
    Tiers per the workbook's Guaranty Fee Calculator."""
    if loan_amount <= 0:
        return 0.0
    if loan_amount <= 150_000:
        guaranteed = loan_amount * 0.85
        return guaranteed * 0.02
    if loan_amount <= 700_000:
        guaranteed = loan_amount * 0.75
        return guaranteed * 0.03
    # $700,001 - $5,000,000: guaranteed 75%; 3.5% on first $1M of guaranteed
    # portion, 3.75% on the balance.
    guaranteed = loan_amount * 0.75
    if guaranteed <= 1_000_000:
        return guaranteed * 0.035
    return 1_000_000 * 0.035 + (guaranteed - 1_000_000) * 0.0375


def weighted_avg_term_years(business_and_me, real_estate, transaction_exp,
                            guaranty_fee, working_capital):
    """SBA maximum-term justification: blend of use-by-use max terms.
    Business acq / M&E / transaction exp / fees / WC = 10 yr; real estate = 25 yr.
    If real estate is a majority of uses the loan can stretch to 25 yr; otherwise
    round the weighted average down (matches the workbook's M18 logic)."""
    uses = {
        10: business_and_me + transaction_exp + guaranty_fee + working_capital,
        25: real_estate,
    }
    total = sum(uses.values())
    if total <= 0:
        return 10
    re_share = real_estate / total
    if re_share >= 0.51:
        return 25
    wavg = sum(term * amt for term, amt in uses.items()) / total
    return int(wavg)  # round down


def fmt(x):
    return f"${x:,.0f}"


def pct(x):
    return f"{x*100:.1f}%"


# ----------------------------- sources & uses -----------------------------

def build_structure(args):
    """Return a dict describing the full Sources & Uses + debt service."""
    price = args.price
    real_estate = args.real_estate
    me_purchase = args.me_purchase

    # Equity / seller note / SBA as % of the acquisition price (matches the
    # workbook's S&U, where Sr Debt + Seller + Equity sum to the price).
    equity = price * args.equity_pct
    seller_note = price * args.seller_note_pct
    sba_loan = price - equity - seller_note  # SBA covers the remainder

    # Transaction expenses + guaranty fee are additional uses. By default they are
    # financed into the SBA loan (common for 7a working-capital-inclusive deals).
    transaction_exp = args.transaction_expenses
    if args.finance_fees:
        # gross the SBA loan up to cover fees + requested working capital
        base = sba_loan
        # iterate because guaranty fee depends on loan size
        for _ in range(50):
            gfee = sba_guaranty_fee(base + transaction_exp + args.working_capital)
            new = sba_loan + transaction_exp + gfee + args.working_capital
            if abs(new - base) < 1.0:
                base = new
                break
            base = new
        sba_loan = base
        guaranty_fee = sba_guaranty_fee(sba_loan)
        working_capital = args.working_capital
    else:
        guaranty_fee = sba_guaranty_fee(sba_loan)
        working_capital = args.working_capital

    total_sources = sba_loan + seller_note + equity
    total_uses = price + real_estate + me_purchase + transaction_exp + guaranty_fee + working_capital

    # SBA term
    if args.sba_term_months:
        term_months = args.sba_term_months
    else:
        term_months = weighted_avg_term_years(
            price + me_purchase, real_estate, transaction_exp, guaranty_fee, working_capital
        ) * 12

    # debt service
    sba_pay_m = pmt(args.sba_rate, term_months, sba_loan)
    sba_annual = sba_pay_m * 12
    loc_annual = args.loc * args.loc_rate  # interest-only
    seller_pay_m = pmt(args.seller_rate, args.seller_term_months, seller_note)
    seller_annual = 0.0 if args.seller_standby else seller_pay_m * 12

    total_ds_standby = sba_annual + loc_annual          # year 1 (seller on standby)
    total_ds_full = sba_annual + loc_annual + seller_pay_m * 12  # after standby

    return {
        "price": price, "real_estate": real_estate, "me_purchase": me_purchase,
        "equity": equity, "seller_note": seller_note, "sba_loan": sba_loan,
        "transaction_exp": transaction_exp, "guaranty_fee": guaranty_fee,
        "working_capital": working_capital,
        "total_sources": total_sources, "total_uses": total_uses,
        "term_months": term_months, "sba_rate": args.sba_rate,
        "sba_pay_m": sba_pay_m, "sba_annual": sba_annual,
        "loc_annual": loc_annual,
        "seller_pay_m": seller_pay_m, "seller_annual": seller_annual,
        "seller_standby": args.seller_standby,
        "total_ds_standby": total_ds_standby, "total_ds_full": total_ds_full,
    }


# ----------------------------- reporting -----------------------------

def print_structure(s, ebitda_years, target_dscr):
    line = "=" * 64
    print(line)
    print("SOURCES & USES")
    print(line)
    print(f"  {'Sources':28}{'$':>14}{'% of price':>12}")
    print(f"  {'SBA 7(a) term loan':28}{fmt(s['sba_loan']):>14}{pct(s['sba_loan']/s['price']):>12}")
    print(f"  {'Seller note (standby)' if s['seller_standby'] else 'Seller note':28}{fmt(s['seller_note']):>14}{pct(s['seller_note']/s['price']):>12}")
    print(f"  {'Buyer equity':28}{fmt(s['equity']):>14}{pct(s['equity']/s['price']):>12}")
    print(f"  {'Total sources':28}{fmt(s['total_sources']):>14}")
    print()
    print(f"  {'Uses':28}{'$':>14}")
    print(f"  {'Business acquisition':28}{fmt(s['price']):>14}")
    if s['real_estate']:
        print(f"  {'Real estate':28}{fmt(s['real_estate']):>14}")
    if s['me_purchase']:
        print(f"  {'M&E purchase':28}{fmt(s['me_purchase']):>14}")
    print(f"  {'Transaction expenses':28}{fmt(s['transaction_exp']):>14}")
    print(f"  {'SBA guaranty fee':28}{fmt(s['guaranty_fee']):>14}")
    print(f"  {'Working capital':28}{fmt(s['working_capital']):>14}")
    print(f"  {'Total uses':28}{fmt(s['total_uses']):>14}")
    print()
    print(line)
    print("DEBT SERVICE")
    print(line)
    yrs = s['term_months'] / 12
    print(f"  SBA term loan: {fmt(s['sba_loan'])} @ {pct(s['sba_rate'])} / {s['term_months']}mo ({yrs:.1f}yr)")
    print(f"    Monthly payment: {fmt(s['sba_pay_m'])}   Annual: {fmt(s['sba_annual'])}")
    if s['loc_annual']:
        print(f"  LOC interest-only annual: {fmt(s['loc_annual'])}")
    if s['seller_standby']:
        print(f"  Seller note: FULL STANDBY -> $0 service during standby")
        print(f"    (post-standby annual would be {fmt(s['seller_pay_m']*12)})")
    else:
        print(f"  Seller note annual: {fmt(s['seller_annual'])}")
    print(f"  Total annual debt service (yr 1, standby): {fmt(s['total_ds_standby'])}")
    if not s['seller_standby'] or s['total_ds_full'] != s['total_ds_standby']:
        print(f"  Total annual debt service (post-standby):  {fmt(s['total_ds_full'])}")
    print()
    print(line)
    print(f"DSCR  (adjusted EBITDA / debt service; SBA floor 1.25x, target {target_dscr}x)")
    print(line)
    print(f"  {'Year':>10}{'Adj EBITDA':>16}{'DSCR (standby)':>18}{'DSCR (full)':>14}")
    for label, e in ebitda_years:
        d_sb = e / s['total_ds_standby'] if s['total_ds_standby'] else float('inf')
        d_fl = e / s['total_ds_full'] if s['total_ds_full'] else float('inf')
        flag = "  <-- below target" if d_sb < target_dscr else ""
        print(f"  {label:>10}{fmt(e):>16}{d_sb:>17.2f}x{d_fl:>13.2f}x{flag}")
    print()


def solve_price(args, ebitda):
    """Binary-search the max business-acquisition price that holds target DSCR
    in year 1 (seller note on standby). Returns the price."""
    lo, hi = 0.0, max(ebitda * 50, 1_000_000)
    for _ in range(100):
        mid = (lo + hi) / 2
        a = argparse.Namespace(**vars(args))
        a.price = mid
        s = build_structure(a)
        dscr = ebitda / s['total_ds_standby'] if s['total_ds_standby'] else float('inf')
        if dscr > args.target_dscr:
            lo = mid
        else:
            hi = mid
    return lo


# ----------------------------- cli -----------------------------

def parse_ebitda(spec):
    """'2023=505656,2024=774106,2025=837261' or '837261' -> list of (label, val)."""
    out = []
    for i, part in enumerate(spec.split(",")):
        part = part.strip()
        if "=" in part:
            label, val = part.split("=", 1)
            out.append((label.strip(), float(val.replace("$", "").replace(",", ""))))
        else:
            out.append((f"yr{i+1}", float(part.replace("$", "").replace(",", ""))))
    return out


def main():
    p = argparse.ArgumentParser(
        description="SBA 7(a) acquisition financing model — DSCR, Sources & Uses, max-price solve.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--ebitda", required=True,
                   help="Adjusted EBITDA. Single number, or labeled list "
                        "'2024=774106,2025=837261'. The LAST value is used for the "
                        "year-1 DSCR gate and the price solve.")
    p.add_argument("--price", type=float, default=None,
                   help="Business acquisition price (forward mode).")
    p.add_argument("--solve-price", action="store_true",
                   help="Solve for max supportable price at --target-dscr instead.")
    p.add_argument("--target-dscr", type=float, default=1.5,
                   help="Target DSCR (workbook threshold 1.5x; SBA floor 1.25x).")
    # structure
    p.add_argument("--equity-pct", type=float, default=0.10)
    p.add_argument("--seller-note-pct", type=float, default=0.10)
    p.add_argument("--seller-standby", action="store_true", default=True,
                   help="Seller note on full standby (no payments during standby). Default on.")
    p.add_argument("--no-seller-standby", dest="seller_standby", action="store_false")
    # SBA term loan
    p.add_argument("--sba-rate", type=float, default=0.085, help="SBA note rate (decimal).")
    p.add_argument("--sba-term-months", type=int, default=120,
                   help="SBA amortization (months). Use 0 for auto weighted-avg term.")
    # seller note
    p.add_argument("--seller-rate", type=float, default=0.06)
    p.add_argument("--seller-term-months", type=int, default=60)
    # line of credit (interest-only)
    p.add_argument("--loc", type=float, default=0.0, help="LOC principal (interest-only service).")
    p.add_argument("--loc-rate", type=float, default=0.085)
    # other uses
    p.add_argument("--real-estate", type=float, default=0.0)
    p.add_argument("--me-purchase", type=float, default=0.0)
    p.add_argument("--transaction-expenses", type=float, default=26000.0)
    p.add_argument("--working-capital", type=float, default=0.0)
    p.add_argument("--finance-fees", action="store_true",
                   help="Gross the SBA loan up to finance transaction expenses + WC.")
    args = p.parse_args()

    if args.sba_term_months == 0:
        args.sba_term_months = None  # triggers auto weighted-avg term

    ebitda_years = parse_ebitda(args.ebitda)
    gate_ebitda = ebitda_years[-1][1]

    if args.solve_price:
        max_price = solve_price(args, gate_ebitda)
        a = argparse.Namespace(**vars(args)); a.price = max_price
        s = build_structure(a)
        print()
        print("#" * 64)
        print(f"MAX SUPPORTABLE PRICE @ DSCR {args.target_dscr}x")
        print(f"  Gate adjusted EBITDA: {fmt(gate_ebitda)}")
        print(f"  => Max business-acquisition price: {fmt(max_price)}")
        print(f"     Implied multiple of gate EBITDA: {max_price/gate_ebitda:.2f}x")
        print("#" * 64)
        print()
        print_structure(s, ebitda_years, args.target_dscr)
        return

    if args.price is None:
        p.error("Provide --price for forward mode, or use --solve-price.")

    s = build_structure(args)
    print()
    print("#" * 64)
    print(f"SBA FINANCING MODEL — acquisition price {fmt(args.price)}")
    print(f"  Asking multiple of last-year adj EBITDA: {args.price/gate_ebitda:.2f}x")
    print("#" * 64)
    print()
    print_structure(s, ebitda_years, args.target_dscr)


if __name__ == "__main__":
    main()
