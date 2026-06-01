from pipeline.database_storage import fetch_all_visitors


def get_dashboard_summary():

    rows = fetch_all_visitors()

    if len(rows) == 0:

        return {
            "total_visitors": 0,
            "average_dwell_time": 0,
            "most_visited_zone": None,
            "highest_dwell_zone": None
        }

    total_visitors = len(rows)

    total_dwell = 0

    zone_counts = {}

    zone_dwell = {}

    for row in rows:

        zone_name = row[2]
        dwell_time = row[3]

        total_dwell += dwell_time

        zone_counts[zone_name] = (
            zone_counts.get(zone_name, 0) + 1
        )

        if zone_name not in zone_dwell:
            zone_dwell[zone_name] = []

        zone_dwell[zone_name].append(
            dwell_time
        )

    average_dwell_time = round(
        total_dwell / total_visitors,
        2
    )

    most_visited_zone = max(
        zone_counts,
        key=zone_counts.get
    )

    highest_dwell_zone = max(
        zone_dwell,
        key=lambda z:
        sum(zone_dwell[z]) /
        len(zone_dwell[z])
    )

    return {
        "total_visitors": total_visitors,
        "average_dwell_time": average_dwell_time,
        "most_visited_zone": most_visited_zone,
        "highest_dwell_zone": highest_dwell_zone
    }