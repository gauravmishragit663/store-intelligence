import pandas as pd
from fastapi import APIRouter

router = APIRouter()

CSV_FILE = "data/pos_transactions.csv"


@router.get("/sales-summary")
def sales_summary():

    df = pd.read_csv(CSV_FILE)

    total_orders = df["order_id"].nunique()

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

    sales_by_brand = (
        df.groupby("brand_name")["total_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .to_dict()
    )

    return {
        "total_orders": int(total_orders),
        "total_sales": float(total_sales),
        "average_order_value": float(average_order_value),
        "top_brand": top_brand,
        "top_5_brands_by_sales": sales_by_brand
    }