"""Shared helpers for the Retail Sales Analytics Dashboard."""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "02_Cleaned_Data" / "superstore_cleaned.csv"

# One consistent look across all pages
NAVY = "#1F4E79"
CATEGORY_COLORS = {"Technology": "#1F4E79", "Furniture": "#E07B39", "Office Supplies": "#4C9F70"}
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = [NAVY, "#E07B39", "#4C9F70", "#8E6BBF", "#C0392B"]

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def setup_page(title):
    st.set_page_config(page_title=title, page_icon="📊", layout="wide")
    st.title(title)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date", "ship_date"])
    df["postal_code"] = df["postal_code"].astype(str).str.zfill(5)
    return df


def money(x):
    return f"-${abs(x):,.0f}" if x < 0 else f"${x:,.0f}"


def section(title, question):
    """Every chart answers a business question; show it under the title."""
    st.subheader(title)
    st.caption(question)


def style(fig, height=380):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=40, b=10), title=None)
    return fig


def multiselect_all(label, options, key):
    """Sidebar filter that starts with everything selected."""
    options = list(options)
    return st.sidebar.multiselect(label, options, default=options, key=key)


def stop_if_empty(df):
    if df.empty:
        st.warning("No data matches the selected filters. Please widen the filters in the sidebar.")
        st.stop()


def kpi_cards(f):
    """The 7 required KPIs for the (filtered) data."""
    sales, profit = f.sales.sum(), f.profit.sum()
    orders = f.order_id.nunique()
    row1 = st.columns(4)
    row1[0].metric("Total Sales", money(sales))
    row1[1].metric("Total Profit", money(profit))
    row1[2].metric("Total Orders", f"{orders:,}")
    row1[3].metric("Total Customers", f"{f.customer_id.nunique():,}")
    row2 = st.columns(3)
    row2[0].metric("Quantity Sold", f"{int(f.quantity.sum()):,}")
    row2[1].metric("Profit Margin", f"{profit / sales * 100:.1f}%")
    row2[2].metric("Average Order Value", f"${sales / orders:,.2f}")


@st.cache_data
def customer_table(df):
    """One row per customer with value segment. Segments use the full data so a customer keeps one label."""
    c = (df.groupby(["customer_id", "customer_name"])
           .agg(sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
           .reset_index())
    hi, lo = c.sales.quantile(0.75), c.sales.quantile(0.25)

    def segment(r):
        if r.sales >= hi and r.profit > 0:
            return "High-Value"
        if r.sales <= lo:
            return "Low-Value"
        return "Medium-Value"

    c["value_segment"] = c.apply(segment, axis=1)
    return c


@st.cache_data
def cohort_retention(df):
    """Monthly cohort retention (%) for the 2014 and 2015 cohorts, months 0 to 24."""
    d = df[["customer_id", "order_date"]].copy()
    d["order_month"] = d.order_date.dt.to_period("M")
    d["cohort_month"] = d.groupby("customer_id")["order_month"].transform("min")
    d["period"] = (d["order_month"] - d["cohort_month"]).apply(lambda x: x.n)
    counts = d.groupby(["cohort_month", "period"]).customer_id.nunique().unstack(fill_value=0)
    last = d.order_month.max()
    max_period = pd.Series({c: (last - c).n for c in counts.index})
    ret = counts.div(counts[0], axis=0) * 100
    for p in ret.columns:
        ret.loc[max_period < p, p] = np.nan
    ret = ret.loc[:"2015-12", 0:24]
    ret.index = ret.index.astype(str)
    return ret
