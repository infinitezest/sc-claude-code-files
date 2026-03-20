# E-Commerce Exploratory Data Analysis

Refactored EDA notebook for analyzing e-commerce sales data with configurable date ranges and reusable metric calculations.

## Project Structure

```
lesson7_files/
  EDA_Refactored.ipynb   # Main analysis notebook
  dashboard.py            # Streamlit interactive dashboard
  data_loader.py          # Data loading, cleaning, and filtering functions
  business_metrics.py     # Business metric calculation functions
  requirements.txt        # Python dependencies
  ecommerce_data/         # Source CSV data files
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

1. Open `EDA_Refactored.ipynb` in Jupyter Notebook or JupyterLab.

2. Modify the configuration variables in the first code cell to analyze different periods:
   ```python
   ANALYSIS_YEAR = 2023
   COMPARISON_YEAR = 2022
   START_MONTH = 1    # January
   END_MONTH = 12     # December
   ```

3. Run all cells. The notebook will:
   - Load and prepare all datasets
   - Filter to the configured date range
   - Calculate and display all business metrics
   - Generate visualizations with the configured period labels

## Modules

### data_loader.py

Functions for loading and preparing e-commerce data:

| Function | Description |
|----------|-------------|
| `load_raw_datasets(data_dir)` | Load all CSV files into DataFrames |
| `parse_datetime_columns(orders)` | Convert timestamp strings to datetime |
| `build_sales_data(orders, order_items)` | Merge orders and items with month/year columns |
| `filter_delivered(sales)` | Keep only delivered orders |
| `filter_by_date_range(df, start_year, start_month, end_year, end_month)` | Filter by year/month range |
| `add_delivery_speed(df)` | Calculate days from purchase to delivery |
| `load_and_prepare(data_dir)` | Convenience function: load, parse, and merge |

### business_metrics.py

Functions for computing business metrics:

| Function | Description |
|----------|-------------|
| `total_revenue(sales)` | Sum of prices |
| `revenue_growth(current, previous)` | YoY revenue percentage change |
| `monthly_revenue(sales)` | Revenue grouped by year and month |
| `monthly_revenue_growth(sales)` | MoM percentage change |
| `average_order_value(sales)` | Mean total price per order |
| `total_orders(sales)` | Count of unique orders |
| `revenue_by_category(sales, products)` | Revenue per product category |
| `revenue_by_state(sales, orders, customers)` | Revenue per state |
| `delivery_speed_stats(sales)` | Mean, median, min, max delivery days |
| `review_score_by_delivery_speed(sales, reviews)` | Avg review per delivery day |
| `review_score_by_delivery_category(sales, reviews)` | Avg review per speed bucket |
| `average_review_score(sales, reviews)` | Overall mean review score |
| `review_score_distribution(sales, reviews)` | Normalized review score counts |
| `order_status_distribution(orders, year)` | Order status proportions |

## Dashboard

An interactive Streamlit dashboard that visualizes all metrics from the notebook.

### Running the Dashboard

```bash
cd lesson7_files
streamlit run dashboard.py
```

### Dashboard Layout

- **Header**: Title and date range filter (Year, From month, To month) that applies globally
- **KPI Row**: Total Revenue, Avg Monthly Growth, Average Order Value, Total Orders -- with YoY trend indicators (green for positive, red for negative)
- **Charts Grid** (2x2):
  - Revenue trend line chart (solid for current year, dashed for comparison year)
  - Top 10 product categories by revenue (horizontal bar, blue gradient)
  - Revenue by state (US choropleth, blue scale)
  - Customer satisfaction vs delivery time (bar chart by delivery speed bucket)
- **Bottom Row**: Average Delivery Time (with trend) and Average Review Score (with star rating)

All charts use Plotly and update dynamically when the date range filter changes.

## Data Files

The `ecommerce_data/` directory contains:

- `orders_dataset.csv` -- Order-level data with timestamps and status
- `order_items_dataset.csv` -- Line items with pricing
- `products_dataset.csv` -- Product catalog with categories
- `customers_dataset.csv` -- Customer locations
- `order_reviews_dataset.csv` -- Customer reviews
- `order_payments_dataset.csv` -- Payment records
