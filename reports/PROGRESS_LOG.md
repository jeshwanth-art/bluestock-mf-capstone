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

## Day 6 — Advanced Analytics + Risk Metrics — STATUS

| # | Task | Status |
|---|------|--------|
| 1 | Historical VaR (95%) + CVaR, all 40 funds | ✅ — `var_cvar_report.csv` |
| 2 | Rolling 90-day Sharpe Ratio (5 funds) | ✅ — `reports/charts/12_rolling_sharpe.png` |
| 3 | Investor cohort analysis (by first-tx year) | ✅ |
| 4 | SIP continuation / at-risk analysis (6+ SIP investors, >35 day gap) | ✅ |
| 5 | Fund recommendation logic (risk appetite → top 3 by Sharpe) | ✅ — `recommender.py` (also runs standalone) |
| 6 | Sector concentration (HHI) | ✅ — `reports/charts/13_sector_concentration_hhi.png` |
| 7 | 5 key insights documented | ✅ |

**Notebook:** `notebooks/05_advanced_analytics.ipynb` — fully executed, 0 errors.

**Real findings worth noting:** VaR/CVaR correctly rank Small Cap funds as
highest tail-risk (as expected from real risk theory — Axis, ABSL, SBI, and
Nippon Small Cap funds all show the worst 95% VaR). Rolling Sharpe ratios
swing between roughly -5 and +7 across the sample period for every fund
tested, showing a single point-in-time Sharpe figure can be misleading.

### To finish Day 6
```
git add .
git commit -m "Day 6: Advanced analytics, risk metrics, and fund recommender"
git push
```

## Day 5 — Dashboard Development (Power BI / Tableau) — STATUS

| # | Task | Status |
|---|------|--------|
| 1 | Connect to data, verify all tables | ✅ — covered in `reports/PowerBI_Build_Guide.docx` |
| 2 | Page 1 — Industry Overview (KPIs, AUM trend, AUM by AMC) | ✅ — working preview + build guide |
| 3 | Page 2 — Fund Performance (scatter, scorecard table, NAV vs benchmark) | ✅ — working preview + build guide |
| 4 | Page 3 — Investor Analytics (state, split, age, monthly volume) | ✅ — working preview + build guide |
| 5 | Page 4 — SIP & Market Trends (dual-axis, heatmap, top 5) | ✅ — working preview + build guide |
| 6 | Interactivity (slicers, tooltips, drill-through) | ✅ — real, working filters on all 3 filterable pages; click-to-drill on the scorecard table |
| 7 | Export to .pbix / PDF / PNG | ⚠️ — see limitation below |

**Important — read before submitting Day 5:** this environment cannot run
Power BI Desktop, so a real `.pbix` file could not be generated here. Instead:

1. **`dashboard/bluestock_mf_dashboard.html`** — a fully working, real-data
   interactive dashboard (all 4 pages, live filters, drill-through, tooltips)
   built with the actual project data. Open it in any browser to see and use
   exactly what the final Power BI dashboard should contain — also published
   at the link Claude shared in the delivering conversation.
2. **`reports/PowerBI_Build_Guide.docx`** — exact fields, chart types, DAX
   measures, and slicer setup for every page, so recreating this as a real
   `.pbix` in Power BI Desktop is a fast, guided build rather than guesswork.

**You still need to:** open Power BI Desktop, follow the build guide, save
as `bluestock_mf_dashboard.pbix`, and export `Dashboard.pdf` + 4 page PNGs
from the real Power BI file for final submission.

### To finish Day 5
```
git add .
git commit -m "Day 5: Dashboard preview (HTML) and Power BI build guide"
git push
```
Then build the real .pbix locally per the guide before final submission.

## Day 4 — Fund Performance Analytics — STATUS

| # | Task | Status |
|---|------|--------|
| 1 | Daily returns for all 40 funds | ✅ — distribution validated, no outliers |
| 2 | CAGR (1yr/3yr/5yr) comparison table | ✅ |
| 3 | Sharpe Ratio, ranked (Rf = 6.5%) | ✅ |
| 4 | Sortino Ratio (downside deviation) | ✅ |
| 5 | Alpha & Beta vs Nifty 100 (OLS regression) | ✅ — `alpha_beta.csv` |
| 6 | Maximum Drawdown + worst drawdown date range | ✅ |
| 7 | Fund Scorecard (composite, 0-100) | ✅ — `fund_scorecard.csv` |
| 8 | Benchmark comparison chart + tracking error | ✅ — top 5 funds beat both Nifty 50 and Nifty 100 over 3yrs |

**Notebook:** `notebooks/04_performance_analytics.ipynb` — fully executed, 0 errors.

**Important finding — read before using `fact_performance` alongside computed
metrics:** cross-checking this notebook's independently computed 3-year CAGR
against the pre-provided `fact_performance.return_3yr_pct` column showed only
**0.08 correlation** across all 40 funds. After testing and ruling out an
as-of-date mismatch and a simple-vs-compounded-return mismatch, the most
likely explanation is that `nav_history.csv` and `scheme_performance.csv` are
two **independently simulated** datasets sharing the same fund list, not one
mathematically derived from the other. Full investigation is in the notebook
(Section 9) — prefer NAV-derived metrics over `fact_performance` for any
further analysis in Days 5-7.

### To finish Day 4
```
git add .
git commit -m "Day 4: Fund performance analytics, scorecard, and benchmark comparison"
git push
```

## Day 3 — Exploratory Data Analysis (EDA) — STATUS

| # | Task | Status |
|---|------|--------|
| 1 | NAV trend analysis (all 40 schemes, 2022-2026) | ✅ |
| 2 | AUM growth bar chart by fund house | ✅ — confirms SBI at real Rs. 12.50L Cr |
| 3 | SIP inflow time-series | ✅ — confirms real Rs. 31,002 Cr Dec-2025 peak |
| 4 | Category inflow heatmap | ✅ |
| 5 | Investor demographics (age, SIP box plot, gender) | ✅ |
| 6 | Geographic distribution (state, T30 vs B30) | ✅ |
| 7 | Folio count growth | ✅ — confirms real 13.26 Cr → 26.12 Cr growth |
| 8 | NAV return correlation matrix | ✅ — genuine finding: correlations are weak/near-zero, not strongly positive as real markets show (see notebook) |
| 9 | Sector allocation donut | ✅ — Banking (19.2%), IT (13.4%), Pharma (12.0%) top 3 |
| 10 | 10 key findings documented in notebook | ✅ |

**Notebook:** `notebooks/03_eda_analysis.ipynb` — fully executed, 0 errors, all
9 charts also exported as PNGs to `reports/charts/` for the final report.

**Note on charts 3 and 7:** the task asked for Plotly for these two, but this
sandbox has no internet access to install Chrome (required by Plotly's static
image export via kaleido) — matplotlib was used instead for reliable
execution. The equivalent Plotly one-liner is left as a comment in each cell;
swap it in if you want the interactive version and have Chrome available.

### To finish Day 3
```
git add .
git commit -m "Day 3: EDA notebook with 9 charts and key findings"
git push
```

## Day 2 — Data Cleaning + SQL Database Design — STATUS

All done and verified against your real data:

| # | Task | Status |
|---|------|--------|
| 1 | Clean `nav_history.csv` (dates, sort, forward-fill, dedupe, validate) | ✅ 46,000 rows — 0 duplicates, 0 invalid NAV, 0 missing weekday NAVs found |
| 2 | Clean `investor_transactions.csv` | ✅ 32,778 rows — 0 issues found (data was already clean) |
| 3 | Clean `scheme_performance.csv` | ✅ 40 rows — 0 non-numeric, 0 negative Sharpe, 0 out-of-range expense ratios |
| 4 | Design SQLite star schema | ✅ `sql/schema.sql` — 2 dim tables + 9 fact tables, with indexes |
| 5 | Load all cleaned datasets into SQLite | ✅ `data/db/bluestock_mf.db` — all 10 tables, row counts verified against source CSVs |
| 6 | Write 10 SQL queries | ✅ `sql/queries.sql` — all run successfully, sample output in `reports/day2_query_results.txt` |
| 7 | Data dictionary | ✅ `reports/data_dictionary.md` |
| 8 | Git commit "Day 2: Cleaned data + SQLite DB loaded" | ⏳ Your turn |

### To finish Day 2
```
git add .
git commit -m "Day 2: Cleaned data + SQLite DB loaded"
git push
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
   (Already done for this project — see Day 2 section above for the next commit.)

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
