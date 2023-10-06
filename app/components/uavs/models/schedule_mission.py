import datetime
from typing import Optional
from pydantic import BaseModel

from droner_server.app.components.uavs.models.point import Point


class ScheduleMissionRequest(BaseModel):
    uav: str
    name: str
    desc: str
    start_date: datetime
    start_point: Point
    destination_point: Point
    record_video: bool
    should_return: bool
