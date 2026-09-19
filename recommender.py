"""
Bluestock Fintech — Capstone Project I: Mutual Fund Analytics
Day 6 — Simple Fund Recommendation Logic

Standalone version of the recommend_funds() function developed in
notebooks/05_advanced_analytics.ipynb, so it can be run or imported
independently of the notebook.

Usage:
    python recommender.py Low
    python recommender.py Moderate
    python recommender.py High
"""

import sys
import sqlite3
import pandas as pd

DB_PATH = "data/db/bluestock_mf.db"

RISK_MAP = {
    "Low": ["Low"],
    "Moderate": ["Moderate", "Moderately High"],
    "High": ["High", "Very High"],
}


def recommend_funds(risk_appetite: str, top_n: int = 3, db_path: str = DB_PATH) -> pd.DataFrame:
    """
    Maps a simple risk appetite (Low / Moderate / High) to the dataset's
    risk_category values and returns the top-N funds by Sharpe ratio
    within that risk band.
    """
    if risk_appetite not in RISK_MAP:
        raise ValueError(f"risk_appetite must be one of {list(RISK_MAP.keys())}")

    conn = sqlite3.connect(db_path)
    fund = pd.read_sql("SELECT * FROM dim_fund", conn)
    perf = pd.read_sql("SELECT * FROM fact_performance", conn)
    conn.close()

    eligible = fund[fund["risk_category"].isin(RISK_MAP[risk_appetite])]
    merged = eligible.merge(perf[["amfi_code", "sharpe_ratio", "return_3yr_pct"]], on="amfi_code")

    return (merged.sort_values("sharpe_ratio", ascending=False)
                  .head(top_n)[["scheme_name", "fund_house", "risk_category",
                                 "sharpe_ratio", "return_3yr_pct"]])


if __name__ == "__main__":
    appetite = sys.argv[1] if len(sys.argv) > 1 else None

    if appetite and appetite in RISK_MAP:
        print(f"=== Recommendations for {appetite} risk appetite ===")
        print(recommend_funds(appetite).to_string(index=False))
    else:
        print("No valid risk appetite given — showing all three:\n")
        for a in RISK_MAP:
            print(f"=== Recommendations for {a} risk appetite ===")
            print(recommend_funds(a).to_string(index=False))
            print()
