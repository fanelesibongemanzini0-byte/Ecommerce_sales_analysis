# E-commerce Sales Analysis | Power BI
![pexels-biravencrow-33357508.jpg](screenshots/pexels-biravencrow-33357508.jpg)
## Project Overview

This project focuses on analysing e-commerce sales data using Power BI to uncover insights into sales performance, customer behaviour and business trends.

The project involves building an interactive dashboard that allows users to explore key performance indicators and monitor performance over time.

## Objectives

- Analyse overall sales performance.
- Monitor key business performance indicators (KPIs).
- Compare performance across different periods using Year-over-Year (YoY) analysis.
- Explore customer-related metrics.
- Build an interactive dashboard to support data-driven decision-making.

## Key Performance Indicators (KPIs)

- Total Revenue
- Total Orders
- Unique Customers
- Average Order Value (AOV)
- Average Customer Rating

## Tools & Technologies

- Power BI
- DAX
- Data Modelling
- Data Visualisation
- Time Intelligence

## Analysis & Features

- KPI cards for high-level performance monitoring.
- Year-based filtering.
- Interactive dashboard slicers.
- Year-over-Year performance comparisons.
- Dynamic KPI indicators.
- Calendar table for time intelligence calculations.

## Data Cleaning and Validation

The raw e-commerce dataset (`ecommerce_sales_analytics_5000.csv`) was prepared and validated using Python before being loaded into the MySQL database.

### 1. Data Inspection
- Inspected the dataset structure, column names and data types.
- Confirmed that the dataset contained 5,000 records and 12 columns.
- Checked for missing values and duplicate records.
- Verified that `order_id` values were unique.

### 2. Data Type Validation
- Converted the `order_date` column from text into a proper date format using Pandas.
- Ensured that date values could be parsed correctly.
- Checked that the dataset columns matched the expected structure.

### 3. Data Quality Checks
The following business rules were checked:

- `quantity` and `unit_price` must be positive.
- `discount` must fall between 0% and 35%.
- `customer_rating` must be between 1 and 5.
- `order_id` must be unique.
- `revenue` must correspond to the expected calculation:

  `Revenue = Quantity × Unit Price × (1 - Discount)`

### 4. Missing Values and Duplicates
- Confirmed that the original dataset contained no missing values.
- Confirmed that there were no duplicate records.
- The loading process rejects datasets containing null values or duplicate order IDs.

### 5. Data Export and Storage
- Preserved the original raw dataset.
- Stored the prepared dataset in `data/processed/ecommerce_sales_cleaned.csv`.
- Used the validated dataset as the source for the MySQL database loading process.

### 6. Database Loading Validation
Before loading data into MySQL:
- Checked that the dataset was not empty.
- Validated the expected column names and order.
- Parsed the order dates.
- Verified the number of records loaded against the input dataset.

**Tools used:** Python, Pandas, MySQL.

## What I Learned

Through this project, I have been developing practical skills in:

- Writing DAX measures.
- Creating a Calendar table.
- Establishing relationships within a data model.
- Applying time intelligence calculations.
- Creating dynamic KPI indicators.
- Designing interactive dashboards.
- Communicating data insights through visualisation.

## Dashboard Preview

![Screenshot 2026-11-21 164747.png](screenshots/Screenshot%202026-11-21%20164747.png)
![Screenshot 2026-11-21 164807.png](screenshots/Screenshot%202026-11-21%20164807.png)
## Project Status

This project is currently under development as I continue improving the dashboard, analysis and visual design.

## Author

Computer Science graduate-in-progress / aspiring Data Analyst & Data Engineer.
