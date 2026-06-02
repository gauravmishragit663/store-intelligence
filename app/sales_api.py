import pandas as pd
from fastapi import APIRouter

router = APIRouter()

CSV_FILE = r"C:\Users\Admin\Downloads\Brigade_Bangalore_10_April_26 (1)bc6219c (1).csv"


@router.get("/sales-summary")
def sales_summary():

    df = pd.read_csv(CSV_FILE)

    total_orders = len(
        df["order_id"].unique()
    )

    total_sales = round(
        df["total_amount"].sum(),
        2
    )

    average_order_value = round(
        total_sales / total_orders,
        2
    )

    top_brand = (
        df["brand_name"]
        .value_counts()
        .idxmax()
    )

    top_department = (
        df["dep_name"]
        .value_counts()
        .idxmax()
    )

    top_category = (
        df["sub_category"]
        .value_counts()
        .idxmax()
    )

    return {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "average_order_value": average_order_value,
        "top_brand": top_brand,
        "top_department": top_department,
        "top_category": top_category
    }