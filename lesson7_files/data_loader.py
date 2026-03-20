"""
Data Loader Module for E-Commerce Analysis

Handles loading, processing, and cleaning of e-commerce datasets.
Provides functions to load raw CSV files, merge them into analysis-ready
DataFrames, and filter by configurable date ranges.
"""

import pandas as pd
from pathlib import Path


# Default path to the data directory
DEFAULT_DATA_DIR = "ecommerce_data"


def load_raw_datasets(data_dir=DEFAULT_DATA_DIR):
    """
    Load all raw CSV datasets from the specified directory.

    Parameters
    ----------
    data_dir : str
        Path to the directory containing the CSV files.

    Returns
    -------
    dict
        Dictionary with keys: 'orders', 'order_items', 'products',
        'customers', 'reviews', 'payments'. Each value is a DataFrame.
    """
    data_path = Path(data_dir)

    datasets = {
        "orders": pd.read_csv(data_path / "orders_dataset.csv"),
        "order_items": pd.read_csv(data_path / "order_items_dataset.csv"),
        "products": pd.read_csv(data_path / "products_dataset.csv"),
        "customers": pd.read_csv(data_path / "customers_dataset.csv"),
        "reviews": pd.read_csv(data_path / "order_reviews_dataset.csv"),
        "payments": pd.read_csv(data_path / "order_payments_dataset.csv"),
    }

    return datasets


def parse_datetime_columns(orders):
    """
    Convert date/time string columns in the orders DataFrame to datetime.

    Parameters
    ----------
    orders : pd.DataFrame
        Orders DataFrame with timestamp string columns.

    Returns
    -------
    pd.DataFrame
        Orders DataFrame with parsed datetime columns.
    """
    datetime_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    orders = orders.copy()
    for col in datetime_cols:
        if col in orders.columns:
            orders[col] = pd.to_datetime(orders[col], errors="coerce")
    return orders


def build_sales_data(orders, order_items):
    """
    Merge orders and order_items into a combined sales DataFrame.

    Adds 'month' and 'year' columns extracted from the purchase timestamp.

    Parameters
    ----------
    orders : pd.DataFrame
        Orders DataFrame (datetime columns should already be parsed).
    order_items : pd.DataFrame
        Order items DataFrame.

    Returns
    -------
    pd.DataFrame
        Merged sales DataFrame with columns from both tables plus
        'month' and 'year'.
    """
    sales = pd.merge(
        left=order_items[["order_id", "order_item_id", "product_id", "price"]],
        right=orders[
            [
                "order_id",
                "order_status",
                "order_purchase_timestamp",
                "order_delivered_customer_date",
            ]
        ],
        on="order_id",
    )

    sales["month"] = sales["order_purchase_timestamp"].dt.month
    sales["year"] = sales["order_purchase_timestamp"].dt.year

    return sales


def filter_delivered(sales):
    """
    Filter the sales DataFrame to include only delivered orders.

    Parameters
    ----------
    sales : pd.DataFrame
        Sales DataFrame with an 'order_status' column.

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame containing only rows where order_status == 'delivered'.
    """
    return sales[sales["order_status"] == "delivered"].copy()


def filter_by_date_range(df, start_year, start_month, end_year, end_month):
    """
    Filter a DataFrame by a year/month range using the 'year' and 'month' columns.

    Both start and end boundaries are inclusive.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'year' and 'month' integer columns.
    start_year : int
        Start year (inclusive).
    start_month : int
        Start month (inclusive, 1-12).
    end_year : int
        End year (inclusive).
    end_month : int
        End month (inclusive, 1-12).

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame.
    """
    start_val = start_year * 100 + start_month
    end_val = end_year * 100 + end_month
    period = df["year"] * 100 + df["month"]
    return df[(period >= start_val) & (period <= end_val)].copy()


def add_delivery_speed(df):
    """
    Add a 'delivery_speed' column representing the number of days
    between purchase and delivery.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'order_delivered_customer_date' and
        'order_purchase_timestamp' columns (both datetime).

    Returns
    -------
    pd.DataFrame
        DataFrame with the added 'delivery_speed' column (integer days).
    """
    df = df.copy()
    df["delivery_speed"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days
    return df


def load_and_prepare(data_dir=DEFAULT_DATA_DIR):
    """
    Convenience function: load all datasets, parse datetimes, and build
    the full sales DataFrame.

    Parameters
    ----------
    data_dir : str
        Path to the directory containing the CSV files.

    Returns
    -------
    tuple
        (datasets, sales_all) where datasets is the raw dict of DataFrames
        and sales_all is the merged sales DataFrame (all statuses).
    """
    datasets = load_raw_datasets(data_dir)
    datasets["orders"] = parse_datetime_columns(datasets["orders"])
    sales_all = build_sales_data(datasets["orders"], datasets["order_items"])
    return datasets, sales_all
