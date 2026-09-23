# Capstone Project I — Mutual Fund Analytics

Bluestock Fintech — Data Analyst Internship
**Status: Complete** (Day 1 → Day 7, all 8 project objectives met)

An end-to-end mutual fund analytics platform: ETL pipeline → SQLite star
schema → EDA → performance & risk metrics → interactive Power BI dashboard
→ final report and presentation. Covers 40 real mutual fund schemes,
~46,000 NAV records, ~32,000 investor transactions, and 4+ years of AUM/SIP
history sourced from AMFI India and mfapi.in.

## Folder Structure
```
bluestock_mf_capstone/
├── data/
│   ├── raw/            → 10 provided CSVs + live NAV pulls from mfapi.in
│   ├── processed/       → 10 cleaned/merged CSVs (Day 2)
│   └── db/               → bluestock_mf.db — 11-table SQLite star schema (Day 2)
├── notebooks/
│   ├── 03_eda_analysis.ipynb              → EDA, 9 charts + 10 findings (Day 3)
│   ├── 04_performance_analytics.ipynb     → CAGR, Sharpe, Sortino, Alpha/Beta (Day 4)
│   └── 05_advanced_analytics.ipynb        → VaR/CVaR, cohorts, recommender, HHI (Day 6)
├── scripts/
│   ├── data_ingestion.py    → loads & inspects all 10 raw CSVs, runs quality checks
│   └── live_nav_fetch.py    → pulls live NAV history from mfapi.in, validates scheme names
├── sql/
│   ├── schema.sql            → 11-table star schema DDL
│   └── queries.sql           → 10 analytical queries
├── dashboard/
│   └── bluestock_mf_dashboard.pbix   → 4-page interactive Power BI dashboard (Day 5)
├── reports/
│   ├── Final_Report.pdf                    → full project report
│   ├── Bluestock_MF_Presentation.pptx      → 12-slide summary deck
│   ├── PowerBI_Build_Guide.pdf             → exact DAX measures/fields per dashboard page
│   ├── data_dictionary.md                  → column-level docs for every DB table
│   ├── charts/                             → 13 exported PNG charts (EDA + performance + risk)
│   ├── PROGRESS_LOG.md                     → original day-by-day build log
│   └── Bluestock_MF_Capstone_Project.pdf   → original project brief
├── fund_scorecard.csv, alpha_beta.csv, var_cvar_report.csv   → key Day 4/6 output tables
├── recommender.py             → risk-appetite-based fund recommender
├── run_pipeline.py            → master script, runs the full ETL end-to-end
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## How to run the ETL pipeline

Run everything end-to-end with one command:
```bash
python run_pipeline.py
```
Or step by step:
```bash
python scripts/data_ingestion.py     # load + validate the 10 raw CSVs
python scripts/live_nav_fetch.py     # optional: refresh live NAV data from mfapi.in
```
Cleaned output lands in `data/processed/`, and `data/db/bluestock_mf.db`
holds the loaded SQLite database. Query it directly with the queries in
`sql/queries.sql`.

## How to open the dashboard

Open `dashboard/bluestock_mf_dashboard.pbix` in Power BI Desktop. It has
4 pages — Industry Overview, Fund Performance, Investor Analytics, and SIP
& Market Trends — each with interactive slicers. `reports/PowerBI_Build_Guide.pdf`
documents every DAX measure and chart field used, if you want to rebuild
or extend it.

## Key finding — scheme code drift

Calling the **live** mfapi.in API for code `125497` returns a different
fund than the project brief's NAV anchor assumes (scheme codes get
reassigned over time on the live API). The **provided** `01_fund_master.csv`
is internally consistent with the rest of the dataset, so it's used as the
source of truth rather than a fresh live call for this project. `live_nav_fetch.py`
validates the returned `scheme_name` against the expected fund and flags
mismatches automatically. Full details in `reports/day1_data_quality_summary.txt`.

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

## Day-by-day build log

See `reports/PROGRESS_LOG.md` for the original Day 1 → Day 7 task-by-task
history, including the scheme-code-drift investigation and the Day 4 finding
that `nav_history.csv` and `scheme_performance.csv` are independently
simulated (not mathematically derived from each other).
