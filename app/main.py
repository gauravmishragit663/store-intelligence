from fastapi import FastAPI
import sqlite3

app = FastAPI(
    title="Store Intelligence API",
    description="Retail Analytics API",
    version="1.0"
)

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


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }