import sqlite3

DB_NAME = "store_intelligence.db"


def save_visitor_analytics(
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


def save_sample_data():

    visitors = [

        (1, "SKINCARE", 45.6, "CAM1"),
        (2, "SKINCARE", 32.1, "CAM1"),
        (3, "SKINCARE", 18.4, "CAM1"),
        (4, "SKINCARE", 27.8, "CAM1"),
        (5, "SKINCARE", 15.2, "CAM1")

    ]

    for visitor in visitors:

        save_visitor_analytics(
            visitor[0],
            visitor[1],
            visitor[2],
            visitor[3]
        )

    print(
        "Analytics saved successfully."
    )


if __name__ == "__main__":

    save_sample_data()