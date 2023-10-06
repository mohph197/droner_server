from datetime import datetime
from pydantic import BaseModel

from app.components.uavs.missions.models.point import Point


class Mission(BaseModel):
    id: str
    uav: str
    name: str
    desc: str
    starting_point: Point
    destination_point: Point
    start_date: datetime
    record_video: bool
    started: bool
    avg_speed: float
    status: str  #  "pending" | "started" | "completed" | "postponed" | "failed" | "reached_destination" | "returning_to_starting"
    status_reason: str
    distance: float
    estimated_duration_in_hours: float
    created_at: datetime
    updated_at: datetime
