from fastapi import FastAPI
import sqlite3
from app.dashboard_api import get_dashboard_summary
from app.top_zone_api import get_top_zone
from app.sales_api import router as sales_router
from fastapi.middleware.cors import CORSMiddleware
from app.ingestion import router as ingestion_router
from app.logger_config import logger
import time
import uuid
from fastapi import Request
from fastapi.responses import FileResponse

app = FastAPI(
    title="Store Intelligence API",
    description="Retail Analytics API",
    version="1.0"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):

    trace_id = str(uuid.uuid4())

    start_time = time.time()

    response = await call_next(request)

    latency = round(
        (time.time() - start_time) * 1000,
        2
    )

    logger.info(
        f"trace_id={trace_id} "
        f"endpoint={request.url.path} "
        f"status_code={response.status_code} "
        f"latency_ms={latency}"
    )

    return response

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
@app.get("/dashboard")
def dashboard():

    return FileResponse(
        "dashboard/index.html"
    )


    