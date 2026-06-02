import pandas as pd

# ==========================
# POS DATASET PATH
# ==========================

csv_file = r"C:\Users\Admin\Downloads\Brigade_Bangalore_10_April_26 (1)bc6219c (1).csv"
# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv(csv_file)

print("\n===== POS ANALYTICS =====\n")

# ==========================
# TOTAL ORDERS
# ==========================

total_orders = len(
    df["order_id"].unique()
)

# ==========================
# TOTAL SALES
# ==========================

total_sales = round(
    df["total_amount"].sum(),
    2
)

# ==========================
# AVERAGE ORDER VALUE
# ==========================

average_order_value = round(
    total_sales / total_orders,
    2
)

# ==========================
# TOP BRAND
# ==========================

top_brand = (
    df["brand_name"]
    .value_counts()
    .idxmax()
)

top_brand_sales = (
    df[df["brand_name"] == top_brand]
    ["total_amount"]
    .sum()
)

# ==========================
# TOP DEPARTMENT
# ==========================

top_department = (
    df["dep_name"]
    .value_counts()
    .idxmax()
)

top_department_sales = (
    df[df["dep_name"] == top_department]
    ["total_amount"]
    .sum()
)

# ==========================
# TOP CATEGORY
# ==========================

top_category = (
    df["sub_category"]
    .value_counts()
    .idxmax()
)

# ==========================
# PRINT REPORT
# ==========================

print(
    f"Total Orders: {total_orders}"
)

print(
    f"Total Sales: ₹{total_sales}"
)

print(
    f"Average Order Value: ₹{average_order_value}"
)

print()

print(
    f"Top Brand: {top_brand}"
)

print(
    f"Top Brand Sales: ₹{round(top_brand_sales, 2)}"
)

print()

print(
    f"Top Department: {top_department}"
)

print(
    f"Department Sales: ₹{round(top_department_sales, 2)}"
)

print()

print(
    f"Top Category: {top_category}"
)