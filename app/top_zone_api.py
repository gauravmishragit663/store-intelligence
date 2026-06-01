from pipeline.database_storage import fetch_all_visitors


def get_top_zone():

    rows = fetch_all_visitors()

    if len(rows) == 0:

        return {
            "zone": None,
            "visitors": 0,
            "average_dwell_time": 0
        }

    zone_stats = {}

    for row in rows:

        zone_name = row[2]
        dwell_time = row[3]

        if zone_name not in zone_stats:

            zone_stats[zone_name] = {
                "visitors": 0,
                "dwell_times": []
            }

        zone_stats[zone_name]["visitors"] += 1

        zone_stats[zone_name]["dwell_times"].append(
            dwell_time
        )

    best_zone = max(
        zone_stats,
        key=lambda z:
        zone_stats[z]["visitors"]
    )

    visitors = zone_stats[best_zone]["visitors"]

    avg_dwell = round(
        sum(
            zone_stats[best_zone]["dwell_times"]
        )
        /
        len(
            zone_stats[best_zone]["dwell_times"]
        ),
        2
    )

    return {
        "zone": best_zone,
        "visitors": visitors,
        "average_dwell_time": avg_dwell
    }