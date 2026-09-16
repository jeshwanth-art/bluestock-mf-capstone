"""
Bluestock Fintech — Capstone Project I: Mutual Fund Analytics
Day 2 — Load cleaned data into SQLite

Creates data/db/bluestock_mf.db from sql/schema.sql, then loads every
cleaned CSV in data/processed/ into its matching table. Verifies row
counts against source CSVs after loading.
"""

import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

PROCESSED_DIR = "data/processed"
DB_PATH = "data/db/bluestock_mf.db"
SCHEMA_PATH = "sql/schema.sql"


def build_schema():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())
    conn.close()
    print(f"Schema created at {DB_PATH}")


def build_dim_date(engine):
    """Derive dim_date from the full date range seen across NAV + benchmark data."""
    nav = pd.read_csv(f"{PROCESSED_DIR}/nav_history_clean.csv", parse_dates=["date"])
    bench = pd.read_csv(f"{PROCESSED_DIR}/benchmark_indices_clean.csv", parse_dates=["date"])
    all_dates = pd.concat([nav["date"], bench["date"]]).drop_duplicates().sort_values()

    dim_date = pd.DataFrame({"date": all_dates.dt.strftime("%Y-%m-%d")})
    dim_date["year"] = all_dates.dt.year.values
    dim_date["month"] = all_dates.dt.month.values
    dim_date["quarter"] = all_dates.dt.quarter.values
    dim_date["is_weekday"] = (all_dates.dt.dayofweek < 5).astype(int).values

    dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
    return len(dim_date)


def load_table(engine, csv_name: str, table_name: str, rename: dict = None) -> int:
    df = pd.read_csv(f"{PROCESSED_DIR}/{csv_name}")
    if rename:
        df = df.rename(columns=rename)
    df.to_sql(table_name, engine, if_exists="append", index=False)
    return len(df)


def main():
    build_schema()
    engine = create_engine(f"sqlite:///{DB_PATH}")

    counts = {}
    counts["dim_fund"] = load_table(engine, "fund_master_clean.csv", "dim_fund")
    counts["dim_date"] = build_dim_date(engine)
    counts["fact_nav"] = load_table(engine, "nav_history_clean.csv", "fact_nav")
    counts["fact_transactions"] = load_table(
        engine, "investor_transactions_clean.csv", "fact_transactions",
        rename={"transaction_date": "transaction_date"})
    counts["fact_performance"] = load_table(
        engine, "scheme_performance_clean.csv", "fact_performance")
    counts["fact_portfolio"] = load_table(
        engine, "portfolio_holdings_clean.csv", "fact_portfolio")
    counts["fact_aum"] = load_table(
        engine, "aum_by_fund_house_clean.csv", "fact_aum")
    counts["fact_sip_industry"] = load_table(
        engine, "monthly_sip_inflows_clean.csv", "fact_sip_industry")
    counts["fact_category_inflows"] = load_table(
        engine, "category_inflows_clean.csv", "fact_category_inflows")
    counts["fact_folio_industry"] = load_table(
        engine, "industry_folio_count_clean.csv", "fact_folio_industry")
    counts["fact_benchmark"] = load_table(
        engine, "benchmark_indices_clean.csv", "fact_benchmark")

    print("\n--- Rows loaded per table ---")
    for table, n in counts.items():
        print(f"  {table:<24} {n:>7} rows")

    # Verification: row counts match source CSVs (fact_transactions renamed col
    # doesn't change row count, so straightforward comparison holds)
    print("\n--- Verification against source CSVs ---")
    verify_pairs = [
        ("fund_master_clean.csv", "dim_fund"),
        ("nav_history_clean.csv", "fact_nav"),
        ("investor_transactions_clean.csv", "fact_transactions"),
        ("scheme_performance_clean.csv", "fact_performance"),
        ("portfolio_holdings_clean.csv", "fact_portfolio"),
        ("aum_by_fund_house_clean.csv", "fact_aum"),
        ("monthly_sip_inflows_clean.csv", "fact_sip_industry"),
        ("category_inflows_clean.csv", "fact_category_inflows"),
        ("industry_folio_count_clean.csv", "fact_folio_industry"),
        ("benchmark_indices_clean.csv", "fact_benchmark"),
    ]
    conn = sqlite3.connect(DB_PATH)
    all_match = True
    for csv_name, table in verify_pairs:
        csv_rows = len(pd.read_csv(f"{PROCESSED_DIR}/{csv_name}"))
        db_rows = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        match = "OK" if csv_rows == db_rows else "MISMATCH"
        if csv_rows != db_rows:
            all_match = False
        print(f"  {table:<24} CSV={csv_rows:>7}  DB={db_rows:>7}  [{match}]")
    conn.close()

    print(f"\nAll row counts match source CSVs: {all_match}")
    print(f"Database ready at {DB_PATH}")


if __name__ == "__main__":
    main()
