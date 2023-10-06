from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

from app.components.uavs.list_uavs import list_uavs
from app.components.uavs.get_uav_data import get_uav_data
from app.components.uavs.control_data_streaming import (
    start_data_streaming,
    stop_data_streaming,
)
from app.components.uavs.missions.get_missions import get_missions
from app.components.uavs.missions.schedule_mission import schedule_mission
from app.components.uavs.missions.models.schedule_mission import (
    ScheduleMissionRequest,
)
from app.components.uavs.missions.models.mission import Mission


router = APIRouter(prefix="/uavs", tags=["uavs"])


@router.get("/", summary="Get List of uavs Available")
async def get_uavs():
    return list_uavs()


@router.get("/:uav", summary="Get Latest UAV Data")
async def get_uavs(uav: str):
    return get_uav_data(uav)


class StartStreamingRequest(BaseModel):
    uavs: List[str]


@router.post(
    "/data_streaming/start", summary="Start Streaming the Latest UAV Data in Real Time"
)
async def start_data_streaming_end_point(body: StartStreamingRequest):
    return start_data_streaming(body.uavs)


class StopStreamingRequest(BaseModel):
    uavs: List[str]


@router.post(
    "/data_streaming/stop", summary="Stop Streaming the Latest UAV Data in Real Time"
)
async def stop_data_streaming_end_point(body: StopStreamingRequest):
    return stop_data_streaming(body.uavs)


@router.post("/missions", summary="Create mission")
async def create_mission(body: ScheduleMissionRequest):
    return schedule_mission(body)


@router.get("/missions", summary="Get missions")
async def list_missions() -> List[Mission]:
    return get_missions()
