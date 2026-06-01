import sqlite3

DB_NAME = "store_intelligence.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def fetch_camera_analytics():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            camera_id,
            COUNT(*) AS visitors,
            ROUND(AVG(dwell_time), 2) AS avg_dwell
        FROM visitor_analytics
        GROUP BY camera_id
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


if __name__ == "__main__":

    data = fetch_camera_analytics()

    print("\n===== MULTI CAMERA ANALYTICS =====\n")

    if len(data) == 0:
        print("No analytics data found.")
        exit()

    max_visitors = 0
    best_camera = None

    max_dwell = 0
    highest_dwell_camera = None

    for row in data:

        camera_id = row[0]
        visitors = row[1]
        avg_dwell = row[2]

        print(f"{camera_id}")
        print(f"Visitors: {visitors}")
        print(f"Average Dwell: {avg_dwell} sec")
        print()

        if visitors > max_visitors:
            max_visitors = visitors
            best_camera = camera_id

        if avg_dwell > max_dwell:
            max_dwell = avg_dwell
            highest_dwell_camera = camera_id

    print(f"Most Visited Camera: {best_camera}")
    print(f"Highest Dwell Camera: {highest_dwell_camera}")