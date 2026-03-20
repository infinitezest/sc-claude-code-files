"""
Business Metrics Module for E-Commerce Analysis

Contains reusable functions for computing business metrics:
revenue analysis, product performance, geographic distribution,
and customer experience indicators.
"""

import pandas as pd


# ---------------------------------------------------------------------------
# Revenue Metrics
# ---------------------------------------------------------------------------

def total_revenue(sales):
    """
    Calculate total revenue from a sales DataFrame.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with a 'price' column.

    Returns
    -------
    float
        Sum of the 'price' column.
    """
    return sales["price"].sum()


def revenue_growth(current_sales, previous_sales):
    """
    Calculate the percentage revenue growth between two periods.

    Parameters
    ----------
    current_sales : pd.DataFrame
        Sales DataFrame for the current period.
    previous_sales : pd.DataFrame
        Sales DataFrame for the previous/comparison period.

    Returns
    -------
    float
        Percentage growth (e.g., 5.2 means +5.2%).
        Returns None if previous period revenue is zero.
    """
    current_rev = total_revenue(current_sales)
    previous_rev = total_revenue(previous_sales)
    if previous_rev == 0:
        return None
    return ((current_rev - previous_rev) / previous_rev) * 100


def monthly_revenue(sales):
    """
    Calculate total revenue grouped by year and month.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'year', 'month', and 'price' columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['year', 'month', 'revenue'].
    """
    result = (
        sales.groupby(["year", "month"])["price"]
        .sum()
        .reset_index()
        .rename(columns={"price": "revenue"})
    )
    return result


def monthly_revenue_growth(sales):
    """
    Calculate month-over-month revenue growth percentages.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'month' and 'price' columns.

    Returns
    -------
    pd.Series
        Series indexed by month with percentage change values.
    """
    return sales.groupby("month")["price"].sum().pct_change() * 100


def average_monthly_growth(sales):
    """
    Calculate the average month-over-month growth rate.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'month' and 'price' columns.

    Returns
    -------
    float
        Mean of the month-over-month growth percentages.
    """
    return monthly_revenue_growth(sales).mean()


# ---------------------------------------------------------------------------
# Order Metrics
# ---------------------------------------------------------------------------

def total_orders(sales):
    """
    Count the number of unique orders.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with an 'order_id' column.

    Returns
    -------
    int
        Number of unique order IDs.
    """
    return sales["order_id"].nunique()


def order_count_growth(current_sales, previous_sales):
    """
    Calculate the percentage growth in order count between two periods.

    Parameters
    ----------
    current_sales : pd.DataFrame
        Sales DataFrame for the current period.
    previous_sales : pd.DataFrame
        Sales DataFrame for the previous/comparison period.

    Returns
    -------
    float
        Percentage growth in order count.
        Returns None if previous period has zero orders.
    """
    current_count = total_orders(current_sales)
    previous_count = total_orders(previous_sales)
    if previous_count == 0:
        return None
    return ((current_count - previous_count) / previous_count) * 100


def average_order_value(sales):
    """
    Calculate the average order value (total price per order).

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'order_id' and 'price' columns.

    Returns
    -------
    float
        Mean of per-order total prices.
    """
    return sales.groupby("order_id")["price"].sum().mean()


def aov_growth(current_sales, previous_sales):
    """
    Calculate percentage growth in average order value between two periods.

    Parameters
    ----------
    current_sales : pd.DataFrame
        Sales DataFrame for the current period.
    previous_sales : pd.DataFrame
        Sales DataFrame for the previous/comparison period.

    Returns
    -------
    float
        Percentage growth in AOV.
        Returns None if previous AOV is zero.
    """
    current_aov = average_order_value(current_sales)
    previous_aov = average_order_value(previous_sales)
    if previous_aov == 0:
        return None
    return ((current_aov - previous_aov) / previous_aov) * 100


def order_status_distribution(orders, year):
    """
    Calculate the proportional distribution of order statuses for a given year.

    Parameters
    ----------
    orders : pd.DataFrame
        Orders DataFrame with 'order_purchase_timestamp' and 'order_status'.
    year : int
        The year to filter on.

    Returns
    -------
    pd.Series
        Normalized value counts of order_status for the specified year.
    """
    orders_year = orders[
        orders["order_purchase_timestamp"].dt.year == year
    ]
    return orders_year["order_status"].value_counts(normalize=True)


# ---------------------------------------------------------------------------
# Product Metrics
# ---------------------------------------------------------------------------

def revenue_by_category(sales, products):
    """
    Calculate total revenue per product category, sorted descending.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'product_id' and 'price' columns.
    products : pd.DataFrame
        Products DataFrame with 'product_id' and 'product_category_name'.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['product_category_name', 'revenue'],
        sorted by revenue descending.
    """
    merged = pd.merge(
        left=products[["product_id", "product_category_name"]],
        right=sales[["product_id", "price"]],
        on="product_id",
    )
    result = (
        merged.groupby("product_category_name")["price"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"price": "revenue"})
    )
    return result


# ---------------------------------------------------------------------------
# Geographic Metrics
# ---------------------------------------------------------------------------

def revenue_by_state(sales, orders, customers):
    """
    Calculate total revenue per customer state, sorted descending.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'order_id' and 'price' columns.
    orders : pd.DataFrame
        Orders DataFrame with 'order_id' and 'customer_id'.
    customers : pd.DataFrame
        Customers DataFrame with 'customer_id' and 'customer_state'.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['customer_state', 'revenue'],
        sorted by revenue descending.
    """
    sales_customers = pd.merge(
        left=sales[["order_id", "price"]],
        right=orders[["order_id", "customer_id"]],
        on="order_id",
    )
    sales_states = pd.merge(
        left=sales_customers,
        right=customers[["customer_id", "customer_state"]],
        on="customer_id",
    )
    result = (
        sales_states.groupby("customer_state")["price"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"price": "revenue"})
    )
    return result


# ---------------------------------------------------------------------------
# Customer Experience Metrics
# ---------------------------------------------------------------------------

def delivery_speed_stats(sales):
    """
    Calculate delivery speed statistics from a sales DataFrame
    that has a 'delivery_speed' column (integer days).

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'delivery_speed' column.

    Returns
    -------
    dict
        Dictionary with 'mean', 'median', 'min', 'max' delivery days.
    """
    speed = sales["delivery_speed"].dropna()
    return {
        "mean": speed.mean(),
        "median": speed.median(),
        "min": speed.min(),
        "max": speed.max(),
    }


def review_score_by_delivery_speed(sales, reviews):
    """
    Calculate average review score grouped by delivery speed (days).

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'order_id' and 'delivery_speed' columns.
    reviews : pd.DataFrame
        Reviews DataFrame with 'order_id' and 'review_score'.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['delivery_speed', 'review_score'].
    """
    merged = sales[["order_id", "delivery_speed"]].drop_duplicates().merge(
        reviews[["order_id", "review_score"]],
        on="order_id",
    )
    result = (
        merged.groupby("delivery_speed")["review_score"]
        .mean()
        .reset_index()
    )
    return result


def categorize_delivery_speed(days):
    """
    Categorize delivery speed into bins.

    Parameters
    ----------
    days : int
        Number of days from purchase to delivery.

    Returns
    -------
    str
        One of '1-3 days', '4-7 days', or '8+ days'.
    """
    if days <= 3:
        return "1-3 days"
    if days <= 7:
        return "4-7 days"
    return "8+ days"


def review_score_by_delivery_category(sales, reviews):
    """
    Calculate average review score grouped by delivery speed category.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'order_id' and 'delivery_speed' columns.
    reviews : pd.DataFrame
        Reviews DataFrame with 'order_id' and 'review_score'.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['delivery_category', 'review_score'].
    """
    merged = sales[["order_id", "delivery_speed"]].drop_duplicates().merge(
        reviews[["order_id", "review_score"]],
        on="order_id",
    )
    merged["delivery_category"] = merged["delivery_speed"].apply(
        categorize_delivery_speed
    )
    result = (
        merged.groupby("delivery_category")["review_score"]
        .mean()
        .reset_index()
    )
    return result


def average_review_score(sales, reviews):
    """
    Calculate the overall average review score for orders in sales.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'order_id' column.
    reviews : pd.DataFrame
        Reviews DataFrame with 'order_id' and 'review_score'.

    Returns
    -------
    float
        Mean review score.
    """
    order_ids = sales["order_id"].unique()
    matched_reviews = reviews[reviews["order_id"].isin(order_ids)]
    return matched_reviews["review_score"].mean()


def review_score_distribution(sales, reviews):
    """
    Calculate the normalized distribution of review scores for orders
    in the sales DataFrame.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with 'order_id' column.
    reviews : pd.DataFrame
        Reviews DataFrame with 'order_id' and 'review_score'.

    Returns
    -------
    pd.Series
        Normalized value counts of review scores.
    """
    order_ids = sales["order_id"].unique()
    matched_reviews = reviews[reviews["order_id"].isin(order_ids)]
    scores = matched_reviews["review_score"]
    return scores.value_counts(normalize=True).sort_index()
