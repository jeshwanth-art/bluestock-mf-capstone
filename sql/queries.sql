-- Bluestock Fintech — Capstone Project I: Mutual Fund Analytics
-- Day 2 — 10 Analytical SQL Queries
-- Run against data/db/bluestock_mf.db

-- 1. Top 5 funds by AUM
SELECT scheme_name, fund_house, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month, per scheme (example: shown for one scheme code, 119551)
SELECT strftime('%Y-%m', date) AS month, amfi_code, ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
WHERE amfi_code = 119551
GROUP BY month, amfi_code
ORDER BY month;

-- 3. SIP inflow YoY growth trend (most recent 12 months with data)
SELECT month, sip_inflow_crore, yoy_growth_pct
FROM fact_sip_industry
WHERE yoy_growth_pct IS NOT NULL
ORDER BY month DESC
LIMIT 12;

-- 4. Transactions by state (total amount + count)
SELECT state, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;

-- 5. Funds with expense_ratio_pct < 1%
SELECT scheme_name, fund_house, category, expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- 6. Top 10 funds by 3-year return
SELECT scheme_name, fund_house, return_3yr_pct, sharpe_ratio
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 10;

-- 7. Total AUM growth by fund house, year over year
SELECT strftime('%Y', date) AS year, fund_house, ROUND(AVG(aum_crore), 0) AS avg_aum_crore
FROM fact_aum
GROUP BY year, fund_house
ORDER BY year, avg_aum_crore DESC;

-- 8. SIP vs Lumpsum vs Redemption split, overall
SELECT transaction_type, COUNT(*) AS num_transactions,
       SUM(amount_inr) AS total_amount_inr,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM fact_transactions), 2) AS pct_of_transactions
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;

-- 9. Sector concentration — top sectors by total portfolio weight across all equity funds
SELECT sector, ROUND(SUM(weight_pct), 2) AS total_weight_pct, COUNT(DISTINCT amfi_code) AS num_funds_holding
FROM fact_portfolio
GROUP BY sector
ORDER BY total_weight_pct DESC
LIMIT 10;

-- 10. Investor demographics — average SIP amount by age group
SELECT age_group, COUNT(*) AS num_sip_transactions, ROUND(AVG(amount_inr), 0) AS avg_sip_amount_inr
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY age_group
ORDER BY avg_sip_amount_inr DESC;
