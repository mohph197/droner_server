from datetime import datetime
import math

from uuid import uuid4


from app.components.uavs.missions.models.point import Point
from app.lib.mongodb import mongodb
from .models.schedule_mission import ScheduleMissionRequest


def schedule_mission(request: ScheduleMissionRequest):
    collection = mongodb["missions"]

    assigned_missions = list(
        collection.find(
            {
                "uav": request.uav,
                "start_date": {"$lte": request.start_date},
                "status": {"$ne": "completed"},
            }
        )
    )

    if len(assigned_missions) != 0:
        raise ValueError("UAV is already assigned to a mission at that time")

    distance = _calculate_distnace_in_km(request.start_point, request.destination_point)

    mission = {
        "id": str(uuid4()),
        "uav": request.uav,
        "name": request.name,
        "desc": request.desc,
        "starting_point": request.start_point.model_dump(),
        "destination_point": request.destination_point.model_dump(),
        "start_date": request.start_date,
        "record_video": request.record_video,
        "avg_speed": request.avg_speed,
        "status": "pending",
        "success": False,
        "distane": distance,
        "real_starting_date": None,
        "completion_date": None,
        "reaching_destination_date": None,
        "actual_duration_in_hours": None,
        "estimated_duration_in_hours": round(distance / request.avg_speed, 2),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

    collection.insert_one(mission)

    del mission["_id"]

    return mission


def _calculate_distnace_in_km(p1: Point, p2: Point):
    return (
        math.acos(
            math.sin(p1.lat) * math.sin(p2.lat)
            + math.cos(p1.lat) * math.cos(p2.lat) * math.cos(p2.lon - p1.lon)
        )
        * 6371
    )
