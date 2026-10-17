import pandas as pd
import plotly.express as px
import streamlit as st

from utils import (CATEGORY_COLORS, MONTH_ORDER, kpi_cards, load_data, multiselect_all, section,
                   setup_page, stop_if_empty, style)

setup_page("Retail Sales Analytics: Executive Overview")
st.caption("Superstore sales, January 2014 to December 2017. Use the filters in the sidebar to explore.")

df = load_data()

st.sidebar.header("Filters")
years = multiselect_all("Year", sorted(df.year.unique()), "p1_year")
regions = multiselect_all("Region", sorted(df.region.unique()), "p1_region")
categories = multiselect_all("Category", sorted(df.category.unique()), "p1_category")

f = df[df.year.isin(years) & df.region.isin(regions) & df.category.isin(categories)]
stop_if_empty(f)

kpi_cards(f)
st.divider()

# 1. Sales trend
section("Sales Trend", "How are sales changing over time, and when are the peaks?")
measure = st.radio("Measure", ["Sales", "Profit", "Quantity"], horizontal=True, key="p1_measure")
col = {"Sales": "sales", "Profit": "profit", "Quantity": "quantity"}[measure]
monthly = f.groupby("year_month_sort", as_index=False)[col].sum()
fig = px.line(monthly, x="year_month_sort", y=col, markers=True,
              labels={"year_month_sort": "Month", col: measure})
st.plotly_chart(style(fig), key="chart_p1_trend")

# 2 and 3. Region and category
left, right = st.columns(2)
with left:
    section("Sales by Region", "Which regions generate the most sales?")
    reg = f.groupby("region", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))
    reg["margin_pct"] = reg.profit / reg.sales * 100
    fig = px.bar(reg.sort_values("sales", ascending=False), x="region", y="sales",
                 hover_data={"profit": ":,.0f", "margin_pct": ":.1f"},
                 labels={"region": "Region", "sales": "Sales (USD)"})
    st.plotly_chart(style(fig), key="chart_p1_region")
with right:
    section("Sales by Category", "Which product categories bring in the most revenue?")
    cat = f.groupby("category", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))
    fig = px.bar(cat.sort_values("sales", ascending=False), x="category", y="sales", color="category",
                 color_discrete_map=CATEGORY_COLORS, labels={"category": "Category", "sales": "Sales (USD)"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(style(fig), key="chart_p1_cat_sales")

# 4. Profit by category
section("Profit by Category", "Which categories are profitable, and which earn little despite high sales?")
cat["margin_pct"] = cat.profit / cat.sales * 100
left, right = st.columns([2, 1])
with left:
    fig = px.bar(cat.sort_values("profit", ascending=False), x="category", y="profit", color="category",
                 color_discrete_map=CATEGORY_COLORS, labels={"category": "Category", "profit": "Profit (USD)"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(style(fig), key="chart_p1_cat_profit")
with right:
    show = cat[["category", "sales", "profit", "margin_pct"]].sort_values("sales", ascending=False)
    show.columns = ["Category", "Sales", "Profit", "Margin %"]
    st.dataframe(show.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}", "Margin %": "{:.1f}"}),
                 hide_index=True)
