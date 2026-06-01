import sqlite3

DB_NAME = "store_intelligence.db"


def create_tables():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitor_analytics (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        visitor_id INTEGER,

        zone_name TEXT,

        dwell_time REAL,

        camera_id TEXT,

        visit_date DATETIME DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


def insert_visitor(
    visitor_id,
    zone_name,
    dwell_time,
    camera_id
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO visitor_analytics
        (
            visitor_id,
            zone_name,
            dwell_time,
            camera_id
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            visitor_id,
            zone_name,
            dwell_time,
            camera_id
        )
    )

    conn.commit()
    conn.close()


def fetch_all_visitors():

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

    return rows


if __name__ == "__main__":

    create_tables()

    print(
        "Database and table created successfully."
    )