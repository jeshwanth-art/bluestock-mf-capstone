# Capstone Project I — Mutual Fund Analytics

Bluestock Fintech — Data Analyst Internship

## Folder Structure
```
bluestock_mf_capstone/
├── data/
│   ├── raw/            → 10 provided CSVs + live NAV pulls from mfapi.in
│   ├── processed/       → cleaned/merged datasets (Day 2)
│   └── db/               → bluestock_mf.db SQLite database (Day 2)
├── notebooks/            → Jupyter notebooks (Day 3+)
├── scripts/
│   ├── data_ingestion.py    → loads & inspects all 10 CSVs, runs quality checks
│   └── live_nav_fetch.py    → pulls live NAV history from mfapi.in
├── sql/                  → schema.sql, queries.sql (Day 2)
├── dashboard/             → Power BI / Tableau files (Day 5)
├── reports/
│   ├── Bluestock_MF_Capstone_Project.pdf   → full project brief
│   └── day1_data_quality_summary.txt        → generated Day 1 output
├── requirements.txt
└── README.md
```

## Day 1 — Project Setup + Data Ingestion (ETL) — STATUS

| # | Task | Status |
|---|------|--------|
| 1 | Folder structure created | ✅ Done |
| 2 | `requirements.txt` created | ✅ Done |
| 3 | Load all 10 CSVs, print shape/dtypes/head() | ✅ Done — see console output / rerun `python scripts/data_ingestion.py` |
| 4 | Fetch live NAV for HDFC Top 100 (125497), save as raw CSV | ✅ Done, with an important finding — see below |
| 5 | Fetch NAV for 5 key schemes | ⚠️ Script ready (`live_nav_fetch.py`) but needs to run on a machine with normal internet access — this sandbox's network is restricted |
| 6 | Explore fund_master — unique fund houses/categories/sub-categories/risk grades | ✅ Done |
| 7 | Validate AMFI codes — fund_master vs nav_history | ✅ Done — all 40 codes match |
| 8 | Git commit "Day 1: Data ingestion complete" | ⏳ Your turn — see commands below |

### Key finding — scheme code drift
Calling the **live** mfapi.in API for code `125497` today (13-Sep-2026)
returns **"SBI Small Cap Fund"**, not "HDFC Top 100" as the project brief's
NAV anchor assumes. The **provided** `01_fund_master.csv` still correctly
maps `125497` → HDFC Top 100 (internally consistent with the rest of the
dataset), so **use the provided data as source of truth**, not a fresh live
call, when working with this scheme code. `live_nav_fetch.py` now validates
the returned `scheme_name` against the expected fund and flags mismatches
automatically rather than trusting the code blindly. Full details in
`reports/day1_data_quality_summary.txt`.

### To finish Day 1

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Re-run ingestion any time (already run once, output captured):
   ```
   python scripts/data_ingestion.py
   ```
3. Fetch live NAV for all 6 schemes (run on your own machine — needs
   normal internet access):
   ```
   python scripts/live_nav_fetch.py
   ```
4. Initialize git and push:
   ```
   git init
   git add .
   git commit -m "Day 1: Data ingestion complete"
   git branch -M main
   git remote add origin <your-new-repo-url>
   git push -u origin main
   ```

## Dataset Summary (actual, verified shapes)
| File | Rows | Cols |
|---|---|---|
| 01_fund_master.csv | 40 | 15 |
| 02_nav_history.csv | 46,000 | 3 |
| 03_aum_by_fund_house.csv | 90 | 5 |
| 04_monthly_sip_inflows.csv | 48 | 6 |
| 05_category_inflows.csv | 144 | 3 |
| 06_industry_folio_count.csv | 21 | 6 |
| 07_scheme_performance.csv | 40 | 19 |
| 08_investor_transactions.csv | 32,778 | 13 |
| 09_portfolio_holdings.csv | 322 | 8 |
| 10_benchmark_indices.csv | 8,050 | 3 |

10 fund houses, 2 categories (Equity/Debt), 12 sub-categories, 5 risk
categories. Only anomaly in the provided data itself: 12 missing
`yoy_growth_pct` values in `04_monthly_sip_inflows.csv` (expected — no
prior-year data exists for the first 12 months of the series).
