from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from droner_server.app.components.uavs.models.point import Point


class Mission(BaseModel):
    uav: str
    name: str
    desc: str
    starting_point: Point
    destination_point: Point
    start_date: datetime
    record_video: bool
    started: bool
    avg_speed: float
    status: str  #  "started" | "completed" | "postponed" | "failed" | "reached_destination" | "returning_to_starting"
    status_reason: str
    estimated_duration_in_hours: float
