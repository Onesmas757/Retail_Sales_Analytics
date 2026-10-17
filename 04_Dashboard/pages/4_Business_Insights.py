import pandas as pd
import plotly.express as px
import streamlit as st

from utils import (MONTH_ORDER, discount_bands, load_data, product_quadrants, section, setup_page, style)

setup_page("Business Insights")
st.caption("What the analysis found and what management should do about it. "
           "Figures cover all years and regions (January 2014 to December 2017).")

df = load_data()
total_profit = df.profit.sum()

# ------------------------------------------------------------------ numbers used in the text
bands = discount_bands(df)
over20 = df[df.discount > 0.20]
over20_loss = over20.profit.sum()

region = df.groupby("region").agg(avg_discount=("discount", "mean")).reset_index()
region["pct_lines_over_20"] = (df.assign(o=df.discount > 0.20).groupby("region").o.mean() * 100).values
central = region[region.region == "Central"].iloc[0]
west = region[region.region == "West"].iloc[0]

furn = df[df.category == "Furniture"]
furn_over20 = furn[furn.discount > 0.20].profit.sum()
furn_up_to20 = furn[furn.discount <= 0.20].profit.sum()

quad = product_quadrants(df)
hslp = quad[quad.group == "High sales / Low profit"].iloc[0]

df["cohort_year"] = df.groupby("customer_id").order_date.transform("min").dt.year
new_by_year = df.drop_duplicates("customer_id").groupby("cohort_year").size().rename("new_customers").reset_index()
n14, n17 = new_by_year.iloc[0, 1], new_by_year.iloc[-1, 1]
df["is_first_month"] = df.order_date.dt.to_period("M") == df.groupby("customer_id").order_date.transform("min").dt.to_period("M")
sales17 = df[df.year == 2017]
new_share_2017 = sales17[sales17.is_first_month].sales.sum() / sales17.sales.sum() * 100

active = df.groupby(["cohort_year", "year"]).customer_id.nunique().unstack()
c14 = (active.loc[2014] / active.loc[2014, 2014] * 100).rename("pct_active").reset_index()
c14.columns = ["year", "pct_active"]

m = df.groupby(["month", "month_name"]).sales.sum().reset_index()
peak_share = m[m.month.isin([9, 11, 12])].sales.sum() / m.sales.sum() * 100

# ------------------------------------------------------------------ findings
st.header("Key Findings")


def finding(n, title, text, fig, key):
    left, right = st.columns([5, 6])
    with left:
        st.subheader(f"Finding {n}: {title}")
        st.write(text)
    with right:
        st.plotly_chart(style(fig, 310), key=f"chart_p4_{key}")
    st.divider()


fig = px.bar(bands, x="band", y="margin_pct", text_auto=".1f",
             labels={"band": "Discount band", "margin_pct": "Profit margin (%)"})
finding(1, "Discounts above 20% destroy profit",
        f"Margin falls from {bands.margin_pct.iloc[0]:.1f}% with no discount to {bands.margin_pct.iloc[2]:.1f}% at 11-20%, "
        f"and turns negative above 20%. The {len(over20):,} lines discounted by more than 20% "
        f"({len(over20) / len(df) * 100:.0f}% of all lines) lost ${-over20_loss:,.0f}, equal to "
        f"{-over20_loss / total_profit * 100:.0f}% of the profit the whole business made. "
        "Units per order line stay at 3.7 to 4.0 at every discount level, so there is no sign that "
        "deeper discounts make orders bigger.", fig, "discount")

fig = px.bar(region, x="region", y="avg_discount", text_auto=".0%",
             labels={"region": "Region", "avg_discount": "Average discount"})
fig.update_yaxes(tickformat=".0%")
finding(2, "Central over-discounts",
        f"Central gives an average discount of {central.avg_discount * 100:.0f}% against {west.avg_discount * 100:.0f}% in the West, "
        f"and {central.pct_lines_over_20:.1f}% of its lines are discounted by more than 20% (West: {west.pct_lines_over_20:.1f}%). "
        "This is the most likely reason for Central's weak 7.9% profit margin.", fig, "region")

fur = pd.DataFrame({"lines": ["Discount up to 20%", "Discount above 20%"], "profit": [furn_up_to20, furn_over20]})
fig = px.bar(fur, x="lines", y="profit", text_auto=",.0f",
             labels={"lines": "Furniture order lines", "profit": "Profit (USD)"})
finding(3, "Furniture is held back by discounting",
        f"Furniture lines with discounts up to 20% earned ${furn_up_to20:,.0f}, but lines discounted above 20% lost "
        f"${-furn_over20:,.0f}. Heavy discounts erase about {-furn_over20 / furn_up_to20 * 100:.0f}% of the profit "
        "Furniture would otherwise make. Tables is the worst case: 55% of its lines are discounted above 20% "
        "and it loses $17,725 overall.", fig, "furniture")

q = quad.melt(id_vars="group", value_vars=["% of sales", "% of profit"], var_name="measure", value_name="percent")
fig = px.bar(q, x="group", y="percent", color="measure", barmode="group",
             labels={"group": "", "percent": "Percent", "measure": ""})
finding(4, "Some high sellers lose money",
        f"{int(hslp.products)} products sell above the median but earn below the median profit. Together they "
        f"bring {hslp['% of sales']:.1f}% of sales and lose ${-hslp.profit:,.0f}. Revenue rankings hide this, profit "
        "rankings show it. Examples: the Cubify CubeX 3D printers, the Lexmark MX611dhe laser printer and "
        "several conference tables.", fig, "quadrant")

fig = px.bar(new_by_year, x="cohort_year", y="new_customers", text_auto=True,
             labels={"cohort_year": "Year of first purchase", "new_customers": "New customers"})
finding(5, "New customer acquisition has almost stopped",
        f"New customers fell from {n14} in 2014 to {n17} in 2017, and returning customers produced "
        f"{100 - new_share_2017:.0f}% of 2017 sales. Growth currently depends entirely on the existing customer base. "
        "(The data starts in 2014, so some 2014 'new' customers may have bought before.)", fig, "acquisition")

fig = px.bar(c14, x="year", y="pct_active", text_auto=".0f",
             labels={"year": "Year", "pct_active": "% of 2014 customers active"})
finding(6, "The customer base is loyal",
        "Monthly retention looks low (about 10%) because customers reorder roughly every four months (median 128 days). "
        f"Measured yearly, {c14.pct_active.iloc[1]:.0f}% to {c14.pct_active.iloc[3]:.0f}% of the customers who started in "
        "2014 are active in each later year, and 98.5% of all customers have ordered at least twice.", fig, "loyalty")

fig = px.bar(m, x="month_name", y="sales", category_orders={"month_name": MONTH_ORDER},
             labels={"month_name": "Month", "sales": "Sales (USD, all years)"})
finding(7, "Sales are strongly seasonal",
        f"September, November and December bring in {peak_share:.0f}% of all sales, while January and February "
        "bring in under 7%. The business has also grown strongly since 2015 (sales +29% in 2016 and +20% in 2017).",
        fig, "seasonal")

# ------------------------------------------------------------------ recommendations
st.header("Recommendations")
recs = [
    ("Cap discounts at 20% and require approval above it",
     f"This targets the ${-over20_loss:,.0f} lost on heavily discounted lines. The data shows deeper discounts do not make orders bigger."),
    ("Review discounting in the Central region",
     "Start with Binders, Tables and Machines, and with products sold at 50% to 80% off."),
    ("Reprice or review the high-sales, low-profit products",
     "Raise prices, cut discounts or renegotiate supplier cost, and consider dropping the worst loss-makers such as the Cubify CubeX printers."),
    ("Review Furniture, especially Tables and Bookcases",
     "Furniture earns a margin of only 2.5%, and Tables and Bookcases lose money overall."),
    ("Restart customer acquisition and protect the core customers",
     "Set a target for new customers (about 50 a month in 2014) and offer loyalty benefits to the High-Value segment, which delivers 78% of profit."),
]
for i, (title, why) in enumerate(recs, 1):
    st.markdown(f"**{i}. {title}.** {why}")
