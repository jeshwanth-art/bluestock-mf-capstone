"""
Bluestock Fintech — Capstone Project I: Mutual Fund Analytics
Day 1 — Data Ingestion

Loads all 10 provided CSV datasets, prints shape/dtypes/head() for each,
explores fund_master (fund houses, categories, sub-categories, risk
grades), and validates that every AMFI code in fund_master also appears
in nav_history — writing a short data quality summary.

Column names below match the actual schema in
reports/Bluestock_MF_Capstone_Project.pdf (Appendix 8).
"""

import glob
import os
import pandas as pd

RAW_DATA_DIR = "data/raw"
FUND_MASTER_FILE = "01_fund_master.csv"
NAV_HISTORY_FILE = "02_nav_history.csv"

REPORT_PATH = "reports/day1_data_quality_summary.txt"


def load_all_csvs(raw_dir: str) -> dict:
    """Load every CSV in raw_dir, printing shape/dtypes/head() for each."""
    csv_paths = sorted(glob.glob(os.path.join(raw_dir, "*.csv")))
    frames = {}
    for path in csv_paths:
        name = os.path.basename(path)
        print(f"\n{'=' * 60}\n{name}\n{'=' * 60}")
        df = pd.read_csv(path)
        print("Shape:", df.shape)
        print("\nDtypes:\n", df.dtypes)
        print("\nHead:\n", df.head())
        frames[name] = df
    return frames


def note_anomalies(frames: dict) -> list:
    """Basic anomaly scan: nulls, duplicate rows, out-of-range values."""
    notes = []
    for name, df in frames.items():
        null_cols = df.columns[df.isnull().any()].tolist()
        if null_cols:
            null_counts = df[null_cols].isnull().sum().to_dict()
            notes.append(f"{name}: missing values -> {null_counts}")

        dupes = df.duplicated().sum()
        if dupes:
            notes.append(f"{name}: {dupes} duplicate rows")

    # Domain-specific checks called out in the project brief
    fm = frames.get(FUND_MASTER_FILE)
    if fm is not None and "expense_ratio_pct" in fm.columns:
        out_of_range = fm[~fm["expense_ratio_pct"].between(0.1, 2.5)]
        if not out_of_range.empty:
            notes.append(f"{FUND_MASTER_FILE}: {len(out_of_range)} scheme(s) "
                          f"with expense_ratio_pct outside the expected "
                          f"0.1%-2.5% range")

    nav = frames.get(NAV_HISTORY_FILE)
    if nav is not None and "nav" in nav.columns:
        non_positive = nav[nav["nav"] <= 0]
        if not non_positive.empty:
            notes.append(f"{NAV_HISTORY_FILE}: {len(non_positive)} rows "
                          f"with NAV <= 0")

    perf = frames.get("07_scheme_performance.csv")
    if perf is not None and "sharpe_ratio" in perf.columns:
        neg_sharpe = perf[perf["sharpe_ratio"] < 0]
        if not neg_sharpe.empty:
            notes.append(f"07_scheme_performance.csv: {len(neg_sharpe)} "
                          f"scheme(s) with negative Sharpe ratio: "
                          f"{neg_sharpe['scheme_name'].tolist()}")

    return notes


def explore_fund_master(frames: dict) -> pd.DataFrame:
    """Print unique fund houses, categories, sub-categories, risk grades."""
    fm = frames[FUND_MASTER_FILE]
    print(f"\n{'=' * 60}\nFUND MASTER EXPLORATION\n{'=' * 60}")
    for col in ["fund_house", "category", "sub_category", "risk_category"]:
        uniques = sorted(fm[col].dropna().unique().tolist())
        print(f"\n{col} ({len(uniques)} unique values): {uniques}")
    return fm


def validate_amfi_codes(frames: dict, fund_master: pd.DataFrame) -> list:
    """Confirm every scheme code in fund_master exists in nav_history."""
    nav = frames[NAV_HISTORY_FILE]
    fm_codes = set(fund_master["amfi_code"].dropna().unique())
    nav_codes = set(nav["amfi_code"].dropna().unique())
    missing = fm_codes - nav_codes

    notes = []
    if missing:
        notes.append(f"{len(missing)} scheme code(s) in fund_master have NO "
                      f"matching rows in nav_history: {sorted(missing)}")
    else:
        notes.append(f"All {len(fm_codes)} scheme codes in fund_master have "
                      f"matching entries in nav_history ({len(nav_codes)} "
                      f"unique codes present there). No missing codes found.")

    orphan_codes = nav_codes - fm_codes
    if orphan_codes:
        notes.append(f"{len(orphan_codes)} scheme code(s) appear in "
                      f"nav_history but NOT in fund_master: "
                      f"{sorted(orphan_codes)}")
    return notes


def main():
    os.makedirs("reports", exist_ok=True)

    frames = load_all_csvs(RAW_DATA_DIR)
    anomaly_notes = note_anomalies(frames)
    fund_master = explore_fund_master(frames)
    validation_notes = validate_amfi_codes(frames, fund_master)

    summary_lines = [
        "BLUESTOCK FINTECH — CAPSTONE PROJECT I: MUTUAL FUND ANALYTICS",
        "Day 1 Data Quality Summary",
        "=" * 60,
        "",
        f"Files loaded: {len(frames)}",
        "",
        "Anomalies found:",
    ]
    summary_lines += [f"  - {n}" for n in anomaly_notes] or ["  - None found"]
    summary_lines += ["", "AMFI code validation (fund_master vs nav_history):"]
    summary_lines += [f"  - {n}" for n in validation_notes]

    summary_text = "\n".join(summary_lines)
    with open(REPORT_PATH, "w") as f:
        f.write(summary_text)

    print(f"\n{summary_text}")
    print(f"\nData quality summary saved to {REPORT_PATH}")


if __name__ == "__main__":
    main()
