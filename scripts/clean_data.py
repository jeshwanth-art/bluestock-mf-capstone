"""
Bluestock Fintech — Capstone Project I: Mutual Fund Analytics
Day 2 — Data Cleaning

Cleans and validates the 10 provided datasets and writes cleaned copies to
data/processed/. Focus areas per the task brief:
  - nav_history: parse dates, sort by amfi_code+date, forward-fill missing
    NAV (holidays/weekends), remove duplicates, validate NAV > 0
  - investor_transactions: standardise transaction_type, validate amount > 0,
    check KYC status values, fix date formats
  - scheme_performance: validate return values are numeric, flag negative
    Sharpe ratios, check expense_ratio range (0.1%-2.5%)
The other 7 datasets are also loaded, de-duplicated, and re-saved as
processed copies so every table in the SQLite DB comes from a consistent
data/processed/ source.
"""

import os
import pandas as pd

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

LOG_PATH = "reports/day2_cleaning_log.txt"
log_lines = []


def log(msg: str):
    print(msg)
    log_lines.append(msg)


def clean_nav_history() -> pd.DataFrame:
    df = pd.read_csv(f"{RAW_DIR}/02_nav_history.csv")
    before = len(df)

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["amfi_code", "date"]).reset_index(drop=True)

    dupes = df.duplicated(subset=["amfi_code", "date"]).sum()
    df = df.drop_duplicates(subset=["amfi_code", "date"])

    non_positive = (df["nav"] <= 0).sum()
    df = df[df["nav"] > 0]

    # Forward-fill any missing NAV on business days per scheme (holidays)
    filled_rows = 0
    filled_frames = []
    for code, grp in df.groupby("amfi_code"):
        grp = grp.set_index("date").sort_index()
        full_range = pd.bdate_range(grp.index.min(), grp.index.max())
        reindexed = grp.reindex(full_range)
        added = reindexed["nav"].isna().sum()
        filled_rows += added
        reindexed["nav"] = reindexed["nav"].ffill()
        reindexed["amfi_code"] = code
        reindexed.index.name = "date"
        filled_frames.append(reindexed.reset_index())

    df = pd.concat(filled_frames, ignore_index=True)
    df["daily_return_pct"] = (
        df.sort_values(["amfi_code", "date"])
          .groupby("amfi_code")["nav"]
          .pct_change() * 100
    )

    log(f"clean nav_history: {before} -> {len(df)} rows "
        f"(removed {dupes} exact duplicates, {non_positive} NAV<=0 rows, "
        f"forward-filled {filled_rows} missing weekday NAVs)")

    df.to_csv(f"{PROCESSED_DIR}/nav_history_clean.csv", index=False)
    return df


def clean_investor_transactions() -> pd.DataFrame:
    df = pd.read_csv(f"{RAW_DIR}/08_investor_transactions.csv")
    before = len(df)

    df["transaction_type"] = df["transaction_type"].str.strip().str.title()
    valid_types = {"Sip", "Lumpsum", "Redemption"}
    bad_types = (~df["transaction_type"].isin(valid_types)).sum()
    df["transaction_type"] = df["transaction_type"].replace(
        {"Sip": "SIP"})

    non_positive = (df["amount_inr"] <= 0).sum()
    df = df[df["amount_inr"] > 0]

    df["transaction_date"] = pd.to_datetime(df["transaction_date"],
                                             errors="coerce")
    bad_dates = df["transaction_date"].isna().sum()
    df = df.dropna(subset=["transaction_date"])

    valid_kyc = {"Verified", "Pending"}
    bad_kyc = (~df["kyc_status"].isin(valid_kyc)).sum()

    dupes = df.duplicated().sum()
    df = df.drop_duplicates()

    log(f"clean investor_transactions: {before} -> {len(df)} rows "
        f"(standardised transaction_type, {bad_types} non-standard type "
        f"values found, {non_positive} amount<=0 rows removed, "
        f"{bad_dates} unparseable dates removed, {bad_kyc} unexpected "
        f"kyc_status values found, {dupes} exact duplicates removed)")

    df.to_csv(f"{PROCESSED_DIR}/investor_transactions_clean.csv", index=False)
    return df


def clean_scheme_performance() -> pd.DataFrame:
    df = pd.read_csv(f"{RAW_DIR}/07_scheme_performance.csv")
    before = len(df)

    numeric_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
                     "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio",
                     "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct",
                     "expense_ratio_pct"]
    non_numeric_flagged = 0
    for col in numeric_cols:
        coerced = pd.to_numeric(df[col], errors="coerce")
        non_numeric_flagged += coerced.isna().sum() - df[col].isna().sum()
        df[col] = coerced

    neg_sharpe = df[df["sharpe_ratio"] < 0]
    out_of_range_expense = df[~df["expense_ratio_pct"].between(0.1, 2.5)]

    dupes = df.duplicated(subset=["amfi_code"]).sum()
    df = df.drop_duplicates(subset=["amfi_code"])

    log(f"clean scheme_performance: {before} -> {len(df)} rows "
        f"({non_numeric_flagged} non-numeric values coerced, "
        f"{len(neg_sharpe)} negative Sharpe ratio scheme(s): "
        f"{neg_sharpe['scheme_name'].tolist()}, "
        f"{len(out_of_range_expense)} scheme(s) with expense_ratio_pct "
        f"outside 0.1%-2.5%, {dupes} duplicate amfi_codes removed)")

    df.to_csv(f"{PROCESSED_DIR}/scheme_performance_clean.csv", index=False)
    return df


def passthrough_clean(raw_filename: str, out_filename: str, subset=None) -> pd.DataFrame:
    """De-dup and null-check a simpler dataset, save to processed/."""
    df = pd.read_csv(f"{RAW_DIR}/{raw_filename}")
    before = len(df)
    dupes = df.duplicated(subset=subset).sum()
    df = df.drop_duplicates(subset=subset)
    null_counts = df.isnull().sum()
    nulls = null_counts[null_counts > 0].to_dict()

    log(f"clean {raw_filename}: {before} -> {len(df)} rows "
        f"({dupes} duplicates removed, nulls: {nulls or 'none'})")

    df.to_csv(f"{PROCESSED_DIR}/{out_filename}", index=False)
    return df


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    log("BLUESTOCK FINTECH — CAPSTONE PROJECT I: MUTUAL FUND ANALYTICS")
    log("Day 2 Data Cleaning Log")
    log("=" * 60)

    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()

    passthrough_clean("01_fund_master.csv", "fund_master_clean.csv",
                       subset=["amfi_code"])
    passthrough_clean("03_aum_by_fund_house.csv", "aum_by_fund_house_clean.csv")
    passthrough_clean("04_monthly_sip_inflows.csv", "monthly_sip_inflows_clean.csv",
                       subset=["month"])
    passthrough_clean("05_category_inflows.csv", "category_inflows_clean.csv")
    passthrough_clean("06_industry_folio_count.csv", "industry_folio_count_clean.csv",
                       subset=["month"])
    passthrough_clean("09_portfolio_holdings.csv", "portfolio_holdings_clean.csv")
    passthrough_clean("10_benchmark_indices.csv", "benchmark_indices_clean.csv")

    with open(LOG_PATH, "w") as f:
        f.write("\n".join(log_lines))
    log(f"\nCleaning log saved to {LOG_PATH}")
    log(f"All cleaned CSVs saved to {PROCESSED_DIR}/")


if __name__ == "__main__":
    main()
