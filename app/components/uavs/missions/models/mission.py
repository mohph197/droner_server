from datetime import datetime
from typing import Union
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
    status: str  #  "pending" | "going to starting" | "going to destination" | "completed" | "reached destination" | "returning to starting"
    success: bool
    distance: float
    real_starting_date: Union[datetime, None]
    reaching_destination_date: Union[datetime, None]
    completion_date: Union[datetime, None]
    estimated_duration_in_hours: float
    actual_duration_in_hours: Union[float, None]
    created_at: datetime
    updated_at: datetime
