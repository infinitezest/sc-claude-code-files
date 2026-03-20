"""
E-Commerce Sales Dashboard

A Streamlit dashboard for interactive e-commerce sales analysis.
Run from the lesson7_files directory:
    streamlit run dashboard.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from calendar import month_abbr

from data_loader import (
    load_and_prepare,
    filter_delivered,
    filter_by_date_range,
    add_delivery_speed,
)
import business_metrics as bm


# ---------------------------------------------------------------------------
# Page configuration and custom CSS
# ---------------------------------------------------------------------------
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.markdown(
    """
    <style>
    /* KPI card styling - theme aware */
    div[data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid rgba(128,128,128,0.2);
        border-radius: 8px;
        padding: 14px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* Bottom row card styling - theme aware */
    .bottom-card {
        background: var(--secondary-background-color);
        border: 1px solid rgba(128,128,128,0.2);
        border-radius: 8px;
        padding: 24px 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .bottom-card .card-value {
        font-size: 36px;
        font-weight: 700;
        color: var(--text-color);
        line-height: 1.2;
    }
    .bottom-card .card-label {
        font-size: 14px;
        color: var(--text-color);
        opacity: 0.6;
        margin-top: 6px;
    }
    .bottom-card .card-trend {
        font-size: 14px;
        margin-top: 6px;
        font-weight: 500;
    }
    .bottom-card .card-stars {
        font-size: 24px;
        color: #F5A623;
        margin-top: 4px;
        letter-spacing: 2px;
    }
    .trend-positive { color: #2e7d32; }
    .trend-negative { color: #c62828; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Load data (cached across reruns)
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    datasets, sales_all = load_and_prepare("ecommerce_data")
    sales_delivered = filter_delivered(sales_all)
    return datasets, sales_delivered


datasets, sales_delivered = load_data()
orders = datasets["orders"]
products = datasets["products"]
customers = datasets["customers"]
reviews = datasets["reviews"]

available_years = sorted(sales_delivered["year"].unique())


# ---------------------------------------------------------------------------
# Header: title (left) + date-range filter (right)
# ---------------------------------------------------------------------------
header_l, header_r = st.columns([3, 2])
with header_l:
    st.markdown("# E-Commerce Sales Dashboard")
with header_r:
    f1, f2, f3 = st.columns(3)
    with f1:
        analysis_year = st.selectbox(
            "Year",
            available_years,
            index=len(available_years) - 1,
        )
    with f2:
        start_month = st.selectbox(
            "From",
            range(1, 13),
            format_func=lambda m: month_abbr[m],
            index=0,
        )
    with f3:
        end_month = st.selectbox(
            "To",
            range(1, 13),
            format_func=lambda m: month_abbr[m],
            index=11,
        )

if start_month > end_month:
    st.error("Start month must be on or before end month.")
    st.stop()

comparison_year = analysis_year - 1
current_label = (
    f"{month_abbr[start_month]}-{month_abbr[end_month]} {analysis_year}"
)
previous_label = (
    f"{month_abbr[start_month]}-{month_abbr[end_month]} {comparison_year}"
)


# ---------------------------------------------------------------------------
# Filter data for selected periods
# ---------------------------------------------------------------------------
sales_current = filter_by_date_range(
    sales_delivered, analysis_year, start_month, analysis_year, end_month
)
sales_previous = filter_by_date_range(
    sales_delivered, comparison_year, start_month, comparison_year, end_month
)
sales_current = add_delivery_speed(sales_current)
has_previous = not sales_previous.empty
if has_previous:
    sales_previous = add_delivery_speed(sales_previous)

if sales_current.empty:
    st.warning("No data for the selected period.")
    st.stop()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def fmt_currency(value):
    """Format a dollar value as $300K or $2.1M."""
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


def fmt_delta(value):
    """Format a percentage delta with sign and two decimals, or None."""
    if value is None:
        return None
    return f"{value:+.2f}%"


# ---------------------------------------------------------------------------
# Compute KPI metrics
# ---------------------------------------------------------------------------
revenue_val = bm.total_revenue(sales_current)
rev_growth_val = (
    bm.revenue_growth(sales_current, sales_previous)
    if has_previous
    else None
)
avg_mom_val = bm.average_monthly_growth(sales_current)
aov_val = bm.average_order_value(sales_current)
aov_growth_val = (
    bm.aov_growth(sales_current, sales_previous)
    if has_previous
    else None
)
orders_val = bm.total_orders(sales_current)
orders_growth_val = (
    bm.order_count_growth(sales_current, sales_previous)
    if has_previous
    else None
)


# ---------------------------------------------------------------------------
# KPI Row: 4 cards
# ---------------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(
        "Total Revenue",
        fmt_currency(revenue_val),
        delta=fmt_delta(rev_growth_val),
    )
with k2:
    st.metric("Avg Monthly Growth", f"{avg_mom_val:.2f}%")
with k3:
    st.metric(
        "Average Order Value",
        f"${aov_val:,.2f}",
        delta=fmt_delta(aov_growth_val),
    )
with k4:
    st.metric(
        "Total Orders",
        f"{orders_val:,}",
        delta=fmt_delta(orders_growth_val),
    )


# ---------------------------------------------------------------------------
# Chart constants
# ---------------------------------------------------------------------------
CHART_HEIGHT = 420
BLUE_DARK = "#2C5F8A"
BLUE_LIGHT = "#A8D5F2"
MONTH_LABELS = [month_abbr[m] for m in range(1, 13)]
PLOTLY_BG = "rgba(0,0,0,0)"
PLOTLY_PAPER_BG = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(128,128,128,0.2)"


# ---------------------------------------------------------------------------
# Charts Grid - Row 1
# ---------------------------------------------------------------------------
st.markdown("---")
chart_l, chart_r = st.columns(2)

# -- Revenue Trend (line chart) --
with chart_l:
    monthly_curr = bm.monthly_revenue(sales_current)
    monthly_prev = (
        bm.monthly_revenue(sales_previous)
        if has_previous
        else pd.DataFrame()
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly_curr["month"],
            y=monthly_curr["revenue"],
            mode="lines+markers",
            name=str(analysis_year),
            line=dict(color=BLUE_DARK, width=3),
            marker=dict(size=7),
            hovertemplate="Month %{x}: %{y:$,.0f}<extra></extra>",
        )
    )
    if not monthly_prev.empty:
        fig.add_trace(
            go.Scatter(
                x=monthly_prev["month"],
                y=monthly_prev["revenue"],
                mode="lines+markers",
                name=str(comparison_year),
                line=dict(color=BLUE_LIGHT, width=2, dash="dash"),
                marker=dict(size=5),
                hovertemplate="Month %{x}: %{y:$,.0f}<extra></extra>",
            )
        )
    fig.update_layout(
        title="Revenue Trend",
        xaxis=dict(
            title="Month",
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=MONTH_LABELS,
            gridcolor=GRID_COLOR,
        ),
        yaxis=dict(
            title="Revenue",
            tickprefix="$",
            tickformat="~s",
            gridcolor=GRID_COLOR,
            gridwidth=1,
        ),
        plot_bgcolor=PLOTLY_BG,
        paper_bgcolor=PLOTLY_PAPER_BG,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        height=CHART_HEIGHT,
        margin=dict(l=60, r=20, t=50, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

# -- Top 10 Categories (horizontal bar chart) --
with chart_r:
    cat_df = bm.revenue_by_category(sales_current, products).head(10)
    # Sort ascending so the highest-revenue category appears at the top
    cat_df = cat_df.sort_values("revenue", ascending=True)
    n = len(cat_df)
    # Blue gradient: lighter for lower values, darker for higher
    cat_colors = [
        f"rgba(44, 95, 138, {0.3 + 0.7 * i / max(n - 1, 1)})"
        for i in range(n)
    ]

    fig = go.Figure(
        go.Bar(
            x=cat_df["revenue"],
            y=cat_df["product_category_name"],
            orientation="h",
            marker_color=cat_colors,
            text=[fmt_currency(v) for v in cat_df["revenue"]],
            textposition="outside",
            hovertemplate="%{y}: %{x:$,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Top 10 Product Categories",
        xaxis=dict(title="Revenue", tickprefix="$", tickformat="~s"),
        yaxis=dict(title=""),
        plot_bgcolor=PLOTLY_BG,
        paper_bgcolor=PLOTLY_PAPER_BG,
        height=CHART_HEIGHT,
        margin=dict(l=170, r=70, t=50, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Charts Grid - Row 2
# ---------------------------------------------------------------------------
chart_l2, chart_r2 = st.columns(2)

# -- Revenue by State (choropleth) --
with chart_l2:
    state_df = bm.revenue_by_state(sales_current, orders, customers)
    fig = px.choropleth(
        state_df,
        locations="customer_state",
        color="revenue",
        locationmode="USA-states",
        scope="usa",
        color_continuous_scale="Blues",
        labels={"revenue": "Revenue (USD)", "customer_state": "State"},
    )
    fig.update_layout(
        title="Revenue by State",
        height=CHART_HEIGHT,
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor=PLOTLY_PAPER_BG,
        geo=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)

# -- Satisfaction vs Delivery Time (bar chart) --
with chart_r2:
    review_cat = bm.review_score_by_delivery_category(
        sales_current, reviews
    )
    bucket_order = ["1-3 days", "4-7 days", "8+ days"]
    review_cat["delivery_category"] = pd.Categorical(
        review_cat["delivery_category"],
        categories=bucket_order,
        ordered=True,
    )
    review_cat = review_cat.sort_values("delivery_category")

    fig = go.Figure(
        go.Bar(
            x=review_cat["delivery_category"],
            y=review_cat["review_score"],
            marker_color=["#7AB8E0", "#4A90D9", "#2C5F8A"],
            text=[f"{s:.2f}" for s in review_cat["review_score"]],
            textposition="outside",
            textfont=dict(size=13),
            hovertemplate="%{x}: %{y:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Satisfaction vs Delivery Time",
        xaxis_title="Delivery Time",
        yaxis=dict(title="Avg Review Score", range=[0, 5.5]),
        plot_bgcolor=PLOTLY_BG,
        paper_bgcolor=PLOTLY_PAPER_BG,
        height=CHART_HEIGHT,
        margin=dict(l=60, r=20, t=50, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Bottom Row: Delivery Time + Review Score
# ---------------------------------------------------------------------------
st.markdown("---")
b1, b2 = st.columns(2)

# -- Average Delivery Time with trend --
with b1:
    curr_speed = bm.delivery_speed_stats(sales_current)["mean"]
    speed_trend_html = ""

    if has_previous:
        prev_speed = bm.delivery_speed_stats(sales_previous)["mean"]
        if prev_speed and prev_speed > 0:
            speed_delta = (
                (curr_speed - prev_speed) / prev_speed
            ) * 100
            # For delivery time, lower is better:
            # negative delta = faster = good (green arrow down)
            # positive delta = slower = bad (red arrow up)
            if speed_delta <= 0:
                css_cls = "trend-positive"
                arrow = "↓"
            else:
                css_cls = "trend-negative"
                arrow = "↑"
            speed_trend_html = (
                f'<div class="card-trend {css_cls}">'
                f"{arrow} {speed_delta:+.2f}% vs {previous_label}"
                f"</div>"
            )

    st.markdown(
        f"""
        <div class="bottom-card">
            <div class="card-value">{curr_speed:.1f} days</div>
            <div class="card-label">Average Delivery Time</div>
            {speed_trend_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

# -- Review Score with stars --
with b2:
    avg_score = bm.average_review_score(sales_current, reviews)
    filled_stars = int(round(avg_score))
    stars_html = (
        "&#9733;" * filled_stars + "&#9734;" * (5 - filled_stars)
    )

    st.markdown(
        f"""
        <div class="bottom-card">
            <div class="card-value">{avg_score:.2f}</div>
            <div class="card-stars">{stars_html}</div>
            <div class="card-label">Average Review Score</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
