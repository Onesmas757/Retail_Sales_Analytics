import plotly.express as px
import streamlit as st

from utils import (cohort_retention, customer_table, load_data, money, multiselect_all, section,
                   setup_page, stop_if_empty, style)

setup_page("Customer Analysis")
st.caption("Who are the customers, how much do they contribute, and how do they behave over time?")

df = load_data()
cust_all = customer_table(df)

st.sidebar.header("Filters")
years = multiselect_all("Year", sorted(df.year.unique()), "p3_year")
regions = multiselect_all("Region", sorted(df.region.unique()), "p3_region")
segments = multiselect_all("Segment", sorted(df.segment.unique()), "p3_segment")
names = ["All customers"] + sorted(df.customer_name.unique())
chosen = st.sidebar.selectbox("Customer", names, key="p3_customer")

f = df[df.year.isin(years) & df.region.isin(regions) & df.segment.isin(segments)]
if chosen != "All customers":
    f = f[f.customer_name == chosen]
stop_if_empty(f)

cust = (f.groupby(["customer_id", "customer_name"], as_index=False)
          .agg(sales=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")))
cust = cust.merge(cust_all[["customer_id", "value_segment"]], on="customer_id")

row = st.columns(5)
row[0].metric("Total Customers", f"{len(cust):,}")
row[1].metric("Sales per Customer", money(cust.sales.mean()))
row[2].metric("Orders per Customer", f"{cust.orders.mean():.1f}")
row[3].metric("Profit per Customer", money(cust.profit.mean()))
row[4].metric("Avg Order Value", f"${f.sales.sum() / f.order_id.nunique():,.2f}")
st.divider()

if chosen != "All customers":
    section(f"Orders of {chosen}", "What has this customer bought?")
    detail = (f.groupby(["order_id", "order_date"], as_index=False)
                .agg(sales=("sales", "sum"), profit=("profit", "sum"), items=("quantity", "sum")))
    st.dataframe(detail.sort_values("order_date").style.format({"sales": "${:,.2f}", "profit": "${:,.2f}"}),
                 hide_index=True)
    st.info(f"Value segment: {cust.value_segment.iloc[0]}. Choose 'All customers' in the sidebar to see the overview.")
    st.stop()

left, right = st.columns(2)
with left:
    section("Top 10 Customers", "Who contributes the most revenue, and are they profitable?")
    top = cust.nlargest(10, "sales")[["customer_name", "sales", "profit", "orders", "value_segment"]]
    top.columns = ["Customer", "Sales", "Profit", "Orders", "Segment"]
    st.dataframe(top.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}"}), hide_index=True)
with right:
    section("Customer Value Segments", "How is the customer base split, and who earns the profit?")
    seg = cust.groupby("value_segment", as_index=False).agg(customers=("customer_id", "count"),
                                                            sales=("sales", "sum"), profit=("profit", "sum"))
    seg["% of customers"] = seg.customers / seg.customers.sum() * 100
    seg["% of sales"] = seg.sales / seg.sales.sum() * 100
    seg["% of profit"] = seg.profit / seg.profit.sum() * 100
    long = seg.melt(id_vars="value_segment", value_vars=["% of customers", "% of sales", "% of profit"],
                    var_name="measure", value_name="percent")
    fig = px.bar(long, x="value_segment", y="percent", color="measure", barmode="group",
                 category_orders={"value_segment": ["High-Value", "Medium-Value", "Low-Value"]},
                 labels={"value_segment": "Segment", "percent": "Percent", "measure": ""})
    st.plotly_chart(style(fig, 330), key="chart_p3_segments")
    st.caption("High-Value: top 25% by sales with positive profit. Low-Value: bottom 25% by sales. Medium: the rest. "
               "Segments are assigned using all years.")

section("Customer Sales Distribution", "How are total sales spread across customers?")
fig = px.histogram(cust, x="sales", nbins=40, labels={"sales": "Total sales per customer (USD)"})
fig.update_layout(yaxis_title="Number of customers")
st.plotly_chart(style(fig, 330), key="chart_p3_hist")

section("Cohort Retention", "Do customers keep buying after their first purchase?")
ret = cohort_retention(df)
fig = px.imshow(ret, text_auto=".0f", aspect="auto", color_continuous_scale="Blues", zmin=0, zmax=40,
                labels={"x": "Months since first purchase", "y": "Cohort (month of first purchase)",
                        "color": "% active"})
st.plotly_chart(style(fig, 620), key="chart_p3_cohort")
st.caption("Each row is a group of customers who first bought in the same month (2014 and 2015 cohorts, all data, "
           "not affected by the sidebar filters). About 10% of a cohort buys in any given month because customers "
           "typically reorder about every four months.")
