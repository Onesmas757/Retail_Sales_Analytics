import numpy as np
import plotly.express as px
import streamlit as st

from utils import (CATEGORY_COLORS, load_data, multiselect_all, section, setup_page, stop_if_empty, style)

setup_page("Product Performance")
st.caption("Which products, categories and sub-categories drive sales and profit, and which need attention?")

df = load_data()

st.sidebar.header("Filters")
categories = multiselect_all("Category", sorted(df.category.unique()), "p2_category")
sub_options = sorted(df[df.category.isin(categories)].sub_category.unique())
subs = multiselect_all("Sub-Category", sub_options, "p2_sub_" + "_".join(categories))
regions = multiselect_all("Region", sorted(df.region.unique()), "p2_region")
years = multiselect_all("Year", sorted(df.year.unique()), "p2_year")

f = df[df.category.isin(categories) & df.sub_category.isin(subs) & df.region.isin(regions) & df.year.isin(years)]
stop_if_empty(f)

prod = f.groupby("product_name", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"),
                                                     qty=("quantity", "sum"))
prod["label"] = prod.product_name.str.slice(0, 40) + np.where(prod.product_name.str.len() > 40, "...", "")

left, right = st.columns(2)
with left:
    section("Top 10 Products", "Which products generate the most revenue or profit?")
    rank_by = st.radio("Rank by", ["Sales", "Profit"], horizontal=True, key="p2_rank")
    col = rank_by.lower()
    top = prod.nlargest(10, col).sort_values(col)
    fig = px.bar(top, x=col, y="label", orientation="h", hover_name="product_name",
                 labels={col: f"{rank_by} (USD)", "label": ""})
    st.plotly_chart(style(fig, 420), key="chart_p2_top")
with right:
    section("Bottom 10 Products by Profit", "Which products lose the most money?")
    bottom = prod.nsmallest(10, "profit").sort_values("profit", ascending=False)
    fig = px.bar(bottom, x="profit", y="label", orientation="h", hover_name="product_name",
                 labels={"profit": "Profit (USD)", "label": ""}, color_discrete_sequence=["#C0392B"])
    st.plotly_chart(style(fig, 420), key="chart_p2_bottom")

left, right = st.columns(2)
cat = f.groupby("category", as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))
with left:
    section("Sales by Category", "Which category brings in the most revenue?")
    fig = px.bar(cat, x="category", y="sales", color="category", color_discrete_map=CATEGORY_COLORS,
                 labels={"category": "Category", "sales": "Sales (USD)"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(style(fig, 330), key="chart_p2_cat_sales")
with right:
    section("Profit by Category", "Which category earns the most profit?")
    fig = px.bar(cat, x="category", y="profit", color="category", color_discrete_map=CATEGORY_COLORS,
                 labels={"category": "Category", "profit": "Profit (USD)"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(style(fig, 330), key="chart_p2_cat_profit")

sub = f.groupby(["category", "sub_category"], as_index=False).agg(sales=("sales", "sum"), profit=("profit", "sum"))
left, right = st.columns(2)
with left:
    section("Sales by Sub-Category", "Which sub-categories sell the most?")
    fig = px.bar(sub.sort_values("sales"), x="sales", y="sub_category", orientation="h", color="category",
                 color_discrete_map=CATEGORY_COLORS, labels={"sales": "Sales (USD)", "sub_category": ""})
    st.plotly_chart(style(fig, 470), key="chart_p2_sub_sales")
with right:
    section("Profit by Sub-Category", "Which sub-categories lose money or earn little?")
    fig = px.bar(sub.sort_values("profit"), x="profit", y="sub_category", orientation="h", color="category",
                 color_discrete_map=CATEGORY_COLORS, labels={"profit": "Profit (USD)", "sub_category": ""})
    st.plotly_chart(style(fig, 470), key="chart_p2_sub_profit")
