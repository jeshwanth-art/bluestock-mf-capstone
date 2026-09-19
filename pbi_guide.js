const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType,
} = require("docx");

function h1(text) { return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 100 } }); }
function h2(text) { return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 160, after: 80 } }); }
function para(text, opts={}) { return new Paragraph({ children: [new TextRun({text, ...opts})], spacing: { after: 100 } }); }
function bullet(text) { return new Paragraph({ text, bullet: { level: 0 }, spacing: { after: 40 } }); }
function code(text) { return new Paragraph({ children: [new TextRun({text, font: "Consolas", size: 19, color: "1F4E79"})], spacing: {after: 100}, shading: {type: ShadingType.CLEAR, fill: "F3F5F8"} }); }

function table(rows, colW) {
  return new Table({
    width: { size: colW.reduce((a,b)=>a+b,0), type: WidthType.DXA },
    columnWidths: colW,
    rows: rows.map((r,i) => new TableRow({ children: r.map((cell,j) => new TableCell({
      width: { size: colW[j], type: WidthType.DXA },
      shading: i===0 ? {type: ShadingType.CLEAR, fill: "1F4E79"} : undefined,
      children: [new Paragraph({ children: [new TextRun({text: cell, bold: i===0, color: i===0?"FFFFFF":"000000", size: 19})] })],
    }))}))
  });
}

const doc = new Document({
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 900, bottom: 900, left: 1000, right: 1000 } } },
    children: [
      new Paragraph({ children: [new TextRun({text: "Power BI Build Guide", bold: true, size: 32})], alignment: AlignmentType.CENTER, spacing: {after: 40} }),
      new Paragraph({ children: [new TextRun({text: "Bluestock Fintech — Capstone Project I: Mutual Fund Analytics, Day 5", size: 20, color: "555555"})], alignment: AlignmentType.CENTER, spacing: {after: 200} }),

      para("This guide gives exact fields, chart types, DAX measures, and slicers needed to recreate the dashboard preview (bluestock_mf_dashboard.html) as a real Power BI Desktop file (bluestock_mf_dashboard.pbix). A working, real-data preview of every page is available at the published dashboard link so you know exactly what each page should look like before building."),

      h1("0. Connect Power BI to the Data"),
      bullet("Open Power BI Desktop → Get Data → SQLite database → point to data/db/bluestock_mf.db"),
      bullet("If the SQLite ODBC connector isn't available, use Get Data → Text/CSV and import each file from data/processed/ instead (10 tables)"),
      bullet("In Model view, create relationships: dim_fund[amfi_code] (1) → fact_nav[amfi_code] (*), fact_transactions[amfi_code] (*), fact_performance[amfi_code] (*, 1:1), fact_portfolio[amfi_code] (*)"),
      bullet("Mark dim_date as a Date Table (Model view → dim_date → Mark as date table), relate to fact_nav[date] and fact_benchmark[date]"),
      bullet("Verify all tables loaded: check row counts in the Data view match reports/data_dictionary.md"),

      h1("1. Page 1 — Industry Overview"),
      h2("KPI Cards"),
      table([
        ["Card", "Value / DAX Measure"],
        ["Total Industry AUM", "Static text card: \"Rs. 81 Lakh Crore\" (real AMFI figure, not derivable from the 40-fund sample — see note below)"],
        ["SIP Inflows", "Total SIP Inflow (Latest) = CALCULATE(SUM(fact_sip_industry[sip_inflow_crore]), FILTER(fact_sip_industry, fact_sip_industry[month] = MAX(fact_sip_industry[month])))"],
        ["Folios", "Static text card: \"26.12 Crore\" (real AMFI Dec-2025 figure)"],
        ["# Schemes", "Static text card: \"1,908\" (real industry-wide figure; this project samples 40)"],
      ], [3120, 6240]),
      para("Note: the brief's KPI targets (Rs.81L Cr AUM, 1,908 schemes) are real, published industry-wide totals — not computable from this project's 40-fund sample. Use static text cards for these two, and label them clearly as industry context so reviewers don't read them as derived from the sample data.", {italics: true, size: 19, color: "777777"}),

      h2("Charts"),
      bullet("Line chart: Industry AUM trend — Axis: fact_aum[date], Values: Sum(fact_aum[aum_crore]), filtered/grouped by date"),
      bullet("Bar chart: AUM by fund house — Axis: dim_fund[fund_house] or fact_aum[fund_house], Values: Average(fact_aum[aum_crore]) filtered to Year = 2025, sorted descending"),

      h1("2. Page 2 — Fund Performance"),
      h2("Key Measures"),
      code("Sharpe Ratio = AVERAGE(fact_performance[sharpe_ratio])"),
      code("3Yr Return % = AVERAGE(fact_performance[return_3yr_pct])"),
      code("Fund Score = [computed in Python — import fund_scorecard.csv as its own table and relate on amfi_code]"),
      h2("Visuals"),
      bullet("Scatter chart: X = fact_performance[return_3yr_pct], Y = fact_performance[std_dev_ann_pct], Size = fact_performance[aum_crore], Legend = dim_fund[category]"),
      bullet("Table: import fund_scorecard.csv as a new table, show scheme_name, fund_score, cagr_3yr_pct, sharpe_ratio_computed, sorted by fund_score descending"),
      bullet("Line chart: NAV vs benchmark — Axis: fact_nav[date], Values: fact_nav[nav] for the fund(s) selected via slicer, plus a second line for fact_benchmark[close_value] filtered to NIFTY50 (use a disconnected NIFTY table or a measure with a fund/benchmark toggle)"),
      bullet("Slicers: dim_fund[fund_house], dim_fund[category], dim_fund[plan] — set to filter the scatter and table visuals"),
      bullet("Drill-through: right-click a scorecard table row → Drill through → set up a NAV Detail page filtered to that amfi_code (Power BI's native drill-through feature)"),

      h1("3. Page 3 — Investor Analytics"),
      bullet("Bar chart (horizontal): Axis = fact_transactions[state], Values = Sum(fact_transactions[amount_inr]), sorted descending"),
      bullet("Donut chart: Legend = fact_transactions[transaction_type], Values = Sum(fact_transactions[amount_inr])"),
      bullet("Bar chart: Axis = fact_transactions[age_group], Values = AVERAGE(fact_transactions[amount_inr]) filtered to transaction_type = \"SIP\""),
      bullet("Line chart: Axis = fact_transactions[transaction_date] (by month), Values = Sum(fact_transactions[amount_inr])"),
      bullet("Slicers: fact_transactions[state], fact_transactions[age_group], fact_transactions[city_tier]"),

      h1("4. Page 4 — SIP & Market Trends"),
      bullet("Combo chart (dual axis): Axis = fact_sip_industry[month], Column values = fact_sip_industry[sip_inflow_crore] (left axis), Line values = fact_benchmark[close_value] filtered to NIFTY50 (right axis)"),
      bullet("Matrix/heatmap: Rows = fact_category_inflows[category], Columns = fact_category_inflows[month], Values = Sum(fact_category_inflows[net_inflow_crore]) — apply conditional formatting (background color scale) to the Values cells"),
      bullet("Bar chart: Top 5 categories by SUM(net_inflow_crore) for FY 2024-25, Top N filter = 5"),
      code("SIP Accounts YoY % = DIVIDE(MAX(fact_sip_industry[active_sip_accounts_crore]) - MIN(fact_sip_industry[active_sip_accounts_crore]), MIN(fact_sip_industry[active_sip_accounts_crore]))"),

      h1("5. Formatting, Branding & Export"),
      bullet("Theme: navy (#10243E) primary, gold (#D4A94C) accent, blue (#2E86AB) secondary — matches the dashboard preview"),
      bullet("Add a Bluestock logo/wordmark text box to each page header"),
      bullet("Enable tooltips on all visuals (Format → Tooltip → On) — default Power BI tooltips are sufficient"),
      bullet("File → Export → Export to PDF for Dashboard.pdf"),
      bullet("File → Export → Export this page as image (PNG) for each of the 4 pages, or use the built-in \"Export data\" / snapshot for the final report"),
      bullet("Save the file as bluestock_mf_dashboard.pbix"),
    ],
  }],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync("/home/claude/bluestock_mf_capstone/reports/PowerBI_Build_Guide.docx", buf); console.log("done"); });
