from datetime import datetime

datetime_str = "2025-05-20T00:00:00+02:00"
trip_1 = {
    "id": "1",
    "start_time": datetime.fromisoformat(datetime_str),
    "x_start": 1,
    "y_start": 2,
    "x_stop": 3,
    "y_stop": 4,
}
