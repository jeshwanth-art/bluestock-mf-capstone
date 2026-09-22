# Bluestock Fintech — Mutual Fund Analytics Platform

**Capstone Project I — Data Analyst Internship**
Individual capstone, 7 working days. End-to-end ETL pipeline, SQL database,
exploratory + performance + risk analytics, and an interactive dashboard
built on 10 real-world-anchored mutual fund datasets (40 schemes, ~87K
transaction rows, 4.5 years of NAV history).

## Day 7 — Final Report + Presentation + Deployment — STATUS

| # | Task | Status |
|---|------|--------|
| 1 | Final PDF report (15-20 pages) | ✅ — `reports/Final_Report.pdf` (14 pages) |
| 2 | 12-slide presentation | ✅ — `reports/Bluestock_MF_Presentation.pptx` |
| 3 | Clean Python scripts + master `run_pipeline.py` | ✅ — all scripts have docstrings; `run_pipeline.py` tested end-to-end |
| 4 | Root `README.md` | ✅ — this file |
| 5 | Final GitHub push + `v1.0` tag | ⏳ Your turn — commands below |
| 6 | (Optional) Publish dashboard | ✅ — HTML preview already published as a Claude artifact |
| 7 | Self-review checklist | ✅ — included as Section 12 of `Final_Report.pdf` |

### To finish Day 7 (and the whole capstone)
```
git add .
git commit -m "Final: Complete Bluestock MF Capstone"
git tag v1.0
git push
git push --tags
```

This is the **last day** — once pushed, all 7 days of the capstone are complete.

## Project Overview

This project ingests AMFI/mfapi.in-style mutual fund data, cleans and loads
it into a SQLite star schema, and analyzes it across four dimensions:
exploratory trends, fund performance & risk-adjusted returns, advanced risk
metrics (VaR/CVaR, rolling Sharpe, sector concentration), and investor
behavior (cohorts, SIP continuity, geographic/demographic patterns). All
findings feed a 4-page interactive dashboard.

**Key real-data-backed results:**
- SBI Mutual Fund leads industry AUM at Rs. 12.50 lakh crore
- SIP inflows peaked at the real all-time high of Rs. 31,002 crore (Dec 2025)
- Total MF folios grew from 13.26 Cr (Jan 2022) to 26.12 Cr (Dec 2025)
- Top 5 scorecard funds outperformed both Nifty 50 and Nifty 100 over 3 years
- Small Cap funds correctly rank as highest tail-risk by VaR/CVaR

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full ETL pipeline (ingestion -> live fetch -> cleaning -> SQLite load)
python run_pipeline.py
# or, without live internet access:
python run_pipeline.py --skip-live

# 3. Run the analysis notebooks (in order)
jupyter nbconvert --to notebook --execute --inplace notebooks/03_eda_analysis.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/04_performance_analytics.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/05_advanced_analytics.ipynb
# (or open them directly in Jupyter Lab/VS Code and run all cells)

# 4. Open the dashboard preview
# Open dashboard/bluestock_mf_dashboard.html directly in any browser — no server needed.
# For the real Power BI file, follow reports/PowerBI_Build_Guide.docx.

# 5. Try the fund recommender standalone
python recommender.py Moderate
```

## Folder Structure
```
bluestock_mf_capstone/
├── data/
│   ├── raw/            10 provided CSVs + live NAV pulls from mfapi.in
│   ├── processed/       Cleaned datasets (Day 2 output)
│   └── db/               bluestock_mf.db — SQLite star schema (11 tables)
├── notebooks/
│   ├── 03_eda_analysis.ipynb            EDA — 9 charts, 10 findings
│   ├── 04_performance_analytics.ipynb   CAGR, Sharpe, Sortino, Alpha/Beta, scorecard
│   └── 05_advanced_analytics.ipynb      VaR/CVaR, rolling Sharpe, cohorts, HHI
├── scripts/
│   ├── data_ingestion.py    Day 1 — load & inspect the 10 raw CSVs
│   ├── live_nav_fetch.py    Day 1 — pull live NAV history from mfapi.in
│   ├── clean_data.py        Day 2 — clean all 10 datasets
│   └── load_to_sqlite.py    Day 2 — build schema + load cleaned data
├── run_pipeline.py       Master script — runs the full ETL pipeline end to end
├── recommender.py        Day 6 — standalone fund recommendation logic
├── sql/
│   ├── schema.sql        11-table star schema DDL
│   └── queries.sql        10 analytical queries
├── dashboard/
│   ├── bluestock_mf_dashboard.html   Working interactive dashboard preview (all 4 pages)
│   └── dashboard_data.json            Real data backing the dashboard
├── reports/
│   ├── Bluestock_MF_Capstone_Project.pdf   Original project brief
│   ├── PowerBI_Build_Guide.docx             Exact DAX/fields/charts to build the real .pbix
│   ├── data_dictionary.md                   Full schema documentation
│   ├── charts/                              13 exported PNG charts (Days 3, 4, 6)
│   ├── PROGRESS_LOG.md                      Day-by-day build log and findings
│   ├── Final_Report.pdf                     Full project report
│   └── day*_*.txt                           Generated logs (ingestion, cleaning, queries)
├── fund_scorecard.csv    Composite fund ranking (Day 4)
├── alpha_beta.csv        Alpha/Beta per fund vs Nifty 100 (Day 4)
├── var_cvar_report.csv   VaR/CVaR per fund (Day 6)
├── requirements.txt
└── README.md
```

## Dataset Descriptions

| File | Rows | Description |
|---|---|---|
| `01_fund_master.csv` | 40 | Master list of 40 real MF schemes — AMFI codes, fund house, category, expense ratio, risk grade, fund manager |
| `02_nav_history.csv` | 46,000 | Daily NAV for all 40 schemes, Jan 2022-May 2026 |
| `03_aum_by_fund_house.csv` | 90 | Quarterly AUM (Rs. crore) for 10 fund houses, 2022-2025 |
| `04_monthly_sip_inflows.csv` | 48 | Monthly SIP inflow, active accounts, new registrations |
| `05_category_inflows.csv` | 144 | Net inflows by fund category, FY 2024-25 |
| `06_industry_folio_count.csv` | 21 | Total MF folios by segment (Equity/Debt/Hybrid) |
| `07_scheme_performance.csv` | 40 | 1/3/5yr returns, Sharpe, Sortino, Alpha, Beta, Max Drawdown |
| `08_investor_transactions.csv` | 32,778 | Simulated SIP/Lumpsum/Redemption transactions, 5,000 investors |
| `09_portfolio_holdings.csv` | 322 | Top equity holdings per fund, as of Dec 2025 |
| `10_benchmark_indices.csv` | 8,050 | Daily closing values for Nifty 50, Nifty 100, and other indices |

Full column-level documentation: `reports/data_dictionary.md`.

## Architecture

```
Raw CSVs + mfapi.in API  ->  Python/Pandas ETL  ->  SQLite star schema
                                                          |
                              Jupyter notebooks (EDA, performance, risk)
                                                          |
                                  Interactive dashboard (4 pages)
```

11-table star schema: `dim_fund`, `dim_date` (dimensions) + `fact_nav`,
`fact_transactions`, `fact_performance`, `fact_portfolio`, `fact_aum`,
`fact_sip_industry`, `fact_category_inflows`, `fact_folio_industry`,
`fact_benchmark` (facts).

## Notable Findings & Honest Limitations

- **Scheme code drift:** the live mfapi.in API no longer maps scheme codes
  the same way the project brief assumes — all 6 codes tested returned
  different funds live vs. the provided `fund_master.csv`. The provided
  data is internally consistent and used as source of truth throughout.
- **`nav_history.csv` and `scheme_performance.csv` are independently
  simulated:** cross-checking computed 3yr CAGR against the pre-provided
  performance table showed only 0.08 correlation — not a bug, but a
  property of the dataset worth knowing before combining the two.
- **No native `.pbix` could be built in this environment** (no Power BI
  Desktop available) — a fully working HTML dashboard preview with the same
  data and interactivity is provided instead, plus an exact build guide.
- **Plotly static export (kaleido) needs Chrome**, unavailable in this
  sandbox — 2 charts in the EDA notebook use matplotlib instead, with the
  Plotly equivalent left as a comment.
- Full details on both: `reports/PROGRESS_LOG.md`.

## Author

Jeshwanth — Data Analyst Intern, Bluestock Fintech
