# Data Dictionary — Bluestock Fintech Mutual Fund Analytics

Documents every table in `data/db/bluestock_mf.db`, sourced from the
cleaned CSVs in `data/processed/`. All original data sourced from AMFI
India, mfapi.in, and NSE/BSE public data per the project brief.

## dim_fund (40 rows)
Source: `01_fund_master.csv` → `fund_master_clean.csv`

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (PK) | AMFI unique scheme code |
| fund_house | TEXT | AMC name |
| scheme_name | TEXT | Full official AMFI scheme name |
| category | TEXT | Equity / Debt |
| sub_category | TEXT | Large Cap / Mid Cap / Small Cap / Liquid / etc. |
| plan | TEXT | Regular or Direct |
| launch_date | TEXT | Fund launch date (YYYY-MM-DD) |
| benchmark | TEXT | Official benchmark index |
| expense_ratio_pct | REAL | Annual expense ratio % |
| exit_load_pct | REAL | Exit load % |
| min_sip_amount | INTEGER | Minimum SIP investment (INR) |
| min_lumpsum_amount | INTEGER | Minimum lumpsum investment (INR) |
| fund_manager | TEXT | Primary fund manager |
| risk_category | TEXT | SEBI risk category |
| sebi_category_code | TEXT | Internal SEBI category code |

## dim_date (1,150 rows)
Derived from the union of dates in `fact_nav` and `fact_benchmark`.

| Column | Type | Description |
|---|---|---|
| date_id | INTEGER (PK) | Surrogate key |
| date | TEXT (UNIQUE) | Calendar date (YYYY-MM-DD) |
| year | INTEGER | Year |
| month | INTEGER | Month (1-12) |
| quarter | INTEGER | Quarter (1-4) |
| is_weekday | INTEGER | 1 = Mon-Fri, 0 = weekend |

## fact_nav (46,000 rows)
Source: `02_nav_history.csv` → `nav_history_clean.csv` (forward-filled,
deduplicated, daily_return_pct computed)

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (FK → dim_fund) | Scheme code |
| date | TEXT | NAV date |
| nav | REAL | NAV in Rs. |
| daily_return_pct | REAL | Day-over-day % change in NAV |

## fact_transactions (32,778 rows)
Source: `08_investor_transactions.csv` → `investor_transactions_clean.csv`

| Column | Type | Description |
|---|---|---|
| tx_id | INTEGER (PK) | Surrogate key |
| investor_id | TEXT | Unique investor ID |
| transaction_date | TEXT | Date of transaction |
| amfi_code | INTEGER (FK → dim_fund) | Fund invested in |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | INTEGER | Transaction amount (INR) |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| city_tier | TEXT | T30 / B30 |
| age_group | TEXT | Age bracket |
| gender | TEXT | Male / Female |
| annual_income_lakh | REAL | Annual income (Rs. lakh) |
| payment_mode | TEXT | UPI / Net Banking / Mandate / Cheque |
| kyc_status | TEXT | Verified / Pending |

## fact_performance (40 rows)
Source: `07_scheme_performance.csv` → `scheme_performance_clean.csv`

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (PK, FK → dim_fund) | Scheme code |
| scheme_name, fund_house, category, plan | TEXT | Fund identifiers |
| return_1yr_pct / 3yr / 5yr | REAL | Trailing returns |
| benchmark_3yr_pct | REAL | Benchmark 3yr CAGR |
| alpha, beta | REAL | Risk-adjusted return metrics |
| sharpe_ratio, sortino_ratio | REAL | Risk-adjusted return ratios |
| std_dev_ann_pct | REAL | Annualised std dev of returns |
| max_drawdown_pct | REAL | Worst peak-to-trough decline |
| aum_crore | REAL | Scheme-level AUM (Rs. crore) |
| expense_ratio_pct | REAL | Annual expense ratio |
| morningstar_rating | INTEGER | 1-5 star rating |
| risk_grade | TEXT | Risk grade |

## fact_portfolio (322 rows)
Source: `09_portfolio_holdings.csv` → `portfolio_holdings_clean.csv`

| Column | Type | Description |
|---|---|---|
| amfi_code | INTEGER (FK → dim_fund) | Fund holding the stock |
| stock_symbol, stock_name | TEXT | Stock identifiers |
| sector | TEXT | Sector classification |
| weight_pct | REAL | % weight in the fund's portfolio |
| market_value_cr | REAL | Market value of holding (Rs. crore) |
| current_price_inr | REAL | Stock price (INR) |
| portfolio_date | TEXT | As-of date |

## fact_aum (90 rows)
Source: `03_aum_by_fund_house.csv` → `aum_by_fund_house_clean.csv`

| Column | Type | Description |
|---|---|---|
| date | TEXT | Quarter-end date |
| fund_house | TEXT | AMC name |
| aum_lakh_crore | REAL | AUM in Rs. lakh crore |
| aum_crore | REAL | AUM in Rs. crore |
| num_schemes | INTEGER | Number of schemes offered |

## fact_sip_industry (48 rows)
Source: `04_monthly_sip_inflows.csv` → `monthly_sip_inflows_clean.csv`

| Column | Type | Description |
|---|---|---|
| month | TEXT (PK) | YYYY-MM |
| sip_inflow_crore | REAL | Total SIP inflow (Rs. crore) |
| active_sip_accounts_crore | REAL | Active SIP accounts (crore) |
| new_sip_accounts_lakh | REAL | New SIP registrations (lakh) |
| sip_aum_lakh_crore | REAL | Total SIP AUM (Rs. lakh crore) |
| yoy_growth_pct | REAL | YoY growth % (null for first 12 months — no prior-year baseline) |

## fact_category_inflows (144 rows)
Source: `05_category_inflows.csv` → `category_inflows_clean.csv`

| Column | Type | Description |
|---|---|---|
| month | TEXT | YYYY-MM |
| category | TEXT | Fund category (Large Cap, Mid Cap, etc.) |
| net_inflow_crore | REAL | Net inflow (Rs. crore) |

## fact_folio_industry (21 rows)
Source: `06_industry_folio_count.csv` → `industry_folio_count_clean.csv`

| Column | Type | Description |
|---|---|---|
| month | TEXT (PK) | YYYY-MM |
| total_folios_crore | REAL | Total MF folios (crore) |
| equity_folios_crore | REAL | Equity folios (crore) |
| debt_folios_crore | REAL | Debt folios (crore) |
| hybrid_folios_crore | REAL | Hybrid folios (crore) |
| others_folios_crore | REAL | Other folios (crore) |

## fact_benchmark (8,050 rows)
Source: `10_benchmark_indices.csv` → `benchmark_indices_clean.csv`

| Column | Type | Description |
|---|---|---|
| date | TEXT | Trading date |
| index_name | TEXT | e.g. NIFTY50, NIFTY100, BSE SmallCap |
| close_value | REAL | Daily closing value |

## Data Quality Notes (Day 1 + Day 2)
- All 40 `amfi_code` values in `dim_fund` have matching rows in `fact_nav` —
  no orphan or missing codes.
- Only genuine anomaly in the provided data: 12 null `yoy_growth_pct`
  values in `fact_sip_industry`, expected since no prior-year data exists
  for the series' first 12 months.
- No duplicate rows, no negative amounts/NAVs, no out-of-range expense
  ratios or negative Sharpe ratios found anywhere in the dataset.
- Live mfapi.in API scheme-code mismatch documented separately in
  `reports/day1_data_quality_summary.txt` — does not affect this
  database, which is built entirely from the provided (internally
  consistent) CSVs.
