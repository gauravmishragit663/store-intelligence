from fastapi import FastAPI
import sqlite3
from app.dashboard_api import get_dashboard_summary
from app.top_zone_api import get_top_zone
from app.sales_api import router as sales_router
from fastapi.middleware.cors import CORSMiddleware
from app.ingestion import router as ingestion_router

app = FastAPI(
    title="Store Intelligence API",
    description="Retail Analytics API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales_router)
app.include_router(ingestion_router)

DB_NAME = "store_intelligence.db"


@app.get("/")
def home():

    return {
        "message": "Store Intelligence API Running"
    }


@app.get("/visitors")
def get_visitors():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM visitor_analytics
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return {
        "total_records": len(rows),
        "data": rows
    }


@app.get("/dashboard-summary")
def dashboard_summary():

    return get_dashboard_summary()


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }
@app.get("/top-zone")
def top_zone():

    return get_top_zone()