-- Bluestock Fintech — Capstone Project I: Mutual Fund Analytics
-- Day 2 — SQLite Star Schema
-- 2 dimension tables + 8 fact tables (data/processed/*.csv -> these tables)

DROP TABLE IF EXISTS dim_fund;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_portfolio;
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS fact_sip_industry;
DROP TABLE IF EXISTS fact_category_inflows;
DROP TABLE IF EXISTS fact_folio_industry;
DROP TABLE IF EXISTS fact_benchmark;

-- ===== DIMENSION TABLES =====

CREATE TABLE dim_fund (
    amfi_code           INTEGER PRIMARY KEY,
    fund_house          TEXT,
    scheme_name         TEXT,
    category            TEXT,
    sub_category        TEXT,
    plan                TEXT,
    launch_date         TEXT,
    benchmark           TEXT,
    expense_ratio_pct   REAL,
    exit_load_pct       REAL,
    min_sip_amount      INTEGER,
    min_lumpsum_amount  INTEGER,
    fund_manager        TEXT,
    risk_category       TEXT,
    sebi_category_code  TEXT
);

CREATE TABLE dim_date (
    date_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT UNIQUE NOT NULL,
    year        INTEGER,
    month       INTEGER,
    quarter     INTEGER,
    is_weekday  INTEGER
);

-- ===== FACT TABLES =====

CREATE TABLE fact_nav (
    amfi_code        INTEGER,
    date             TEXT,
    nav              REAL,
    daily_return_pct REAL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_transactions (
    tx_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id          TEXT,
    transaction_date     TEXT,
    amfi_code            INTEGER,
    transaction_type     TEXT,
    amount_inr           INTEGER,
    state                TEXT,
    city                 TEXT,
    city_tier             TEXT,
    age_group             TEXT,
    gender                TEXT,
    annual_income_lakh    REAL,
    payment_mode          TEXT,
    kyc_status            TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_performance (
    amfi_code            INTEGER PRIMARY KEY,
    scheme_name           TEXT,
    fund_house             TEXT,
    category                TEXT,
    plan                    TEXT,
    return_1yr_pct          REAL,
    return_3yr_pct          REAL,
    return_5yr_pct          REAL,
    benchmark_3yr_pct       REAL,
    alpha                   REAL,
    beta                    REAL,
    sharpe_ratio             REAL,
    sortino_ratio            REAL,
    std_dev_ann_pct          REAL,
    max_drawdown_pct         REAL,
    aum_crore                REAL,
    expense_ratio_pct        REAL,
    morningstar_rating       INTEGER,
    risk_grade               TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_portfolio (
    amfi_code           INTEGER,
    stock_symbol         TEXT,
    stock_name            TEXT,
    sector                TEXT,
    weight_pct            REAL,
    market_value_cr       REAL,
    current_price_inr     REAL,
    portfolio_date        TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_aum (
    date          TEXT,
    fund_house     TEXT,
    aum_lakh_crore REAL,
    aum_crore       REAL,
    num_schemes     INTEGER,
    PRIMARY KEY (date, fund_house)
);

CREATE TABLE fact_sip_industry (
    month                       TEXT PRIMARY KEY,
    sip_inflow_crore             REAL,
    active_sip_accounts_crore    REAL,
    new_sip_accounts_lakh        REAL,
    sip_aum_lakh_crore           REAL,
    yoy_growth_pct               REAL
);

CREATE TABLE fact_category_inflows (
    month              TEXT,
    category            TEXT,
    net_inflow_crore     REAL,
    PRIMARY KEY (month, category)
);

CREATE TABLE fact_folio_industry (
    month                 TEXT PRIMARY KEY,
    total_folios_crore     REAL,
    equity_folios_crore     REAL,
    debt_folios_crore       REAL,
    hybrid_folios_crore     REAL,
    others_folios_crore     REAL
);

CREATE TABLE fact_benchmark (
    date         TEXT,
    index_name    TEXT,
    close_value    REAL,
    PRIMARY KEY (date, index_name)
);

-- ===== INDEXES for fast query performance =====
CREATE INDEX idx_fact_nav_amfi_date ON fact_nav(amfi_code, date);
CREATE INDEX idx_fact_tx_amfi ON fact_transactions(amfi_code);
CREATE INDEX idx_fact_tx_date ON fact_transactions(transaction_date);
CREATE INDEX idx_fact_tx_state ON fact_transactions(state);
CREATE INDEX idx_fact_portfolio_amfi ON fact_portfolio(amfi_code);
CREATE INDEX idx_fact_benchmark_index ON fact_benchmark(index_name);
