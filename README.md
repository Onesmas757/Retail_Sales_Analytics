# Retail Sales Analytics Dashboard

NexAfrica Data Analysis Internship, Task 1. An end-to-end analysis of the Superstore Sales dataset (January 2014 to December 2017): data cleaning, KPIs, SQL, customer segmentation, cohort analysis, discount and profitability analysis, and a 4-page interactive dashboard.

## Business problem
How is the business performing across products, customers, regions and time, which areas need attention, and what should management do about it?

## Key findings
- Sales grew 29.5% in 2016 and 20.4% in 2017, and peak every September, November and December (43% of sales).
- **Discounts above 20% lose money.** 1,392 order lines lost $135,364, equal to 47% of total profit. Deeper discounts did not make orders bigger.
- Central discounts the most (24% average) and has the weakest margin (7.9%). Furniture earns a 2.5% margin.
- 252 high-selling products lose a combined $72,632.
- 22% of customers (High-Value) deliver 78% of profit. The customer base is loyal, but new customers fell from 595 in 2014 to 11 in 2017.

## Tools
Python (pandas, NumPy, Matplotlib, Seaborn, Plotly), SQLite, Jupyter, Streamlit.

## Project structure
```text
01_Raw_Data/        superstore_raw.csv (never edited)
02_Cleaned_Data/    superstore_cleaned.csv / .xlsx, data_dictionary.csv, cleaning documentation
03_Analysis/        notebooks 01 to 05, queries.sql, schema.sql, sql_findings.md, analysis.xlsx, charts/
04_Dashboard/       app.py, utils.py, pages/, KPI_definitions.md, screenshots/
05_Report/          executive_summary.pdf
06_Presentation/    final_presentation.pptx
```

## Notebooks (run in order)
1. `cleaning.ipynb`: inspection, cleaning, calculated fields, data dictionary
2. `eda_kpis.ipynb`: KPIs, trends, regions, categories, EDA
3. `sql_analysis.ipynb`: SQLite database and 13 SQL queries
4. `products_customers.ipynb`: product analysis, customer metrics, segmentation
5. `cohort_discount_profit.ipynb`: cohorts, discounts, profitability groups, recommendations

## How to run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

jupyter lab                       # open the notebooks in 03_Analysis/

cd 04_Dashboard
streamlit run app.py              # dashboard at http://localhost:8501
```

## Dashboard pages
1. **Executive Overview:** 7 KPI cards, sales trend, sales by region and category, profit by category
2. **Product Performance:** top and bottom 10 products, category and sub-category sales and profit
3. **Customer Analysis:** customer KPIs, top customers, value segments, sales distribution, cohort retention
4. **Business Insights:** key findings and recommendations

## Limitations
One retailer, data ends in 2017, no cost or marketing data, and some 2014 "new" customers may have bought before the data begins. Segment thresholds are judgement-based.
