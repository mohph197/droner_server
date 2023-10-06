from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

from app.components.uavs import list_uavs
from app.components.uavs import get_uav_data
from app.components.uavs.control_data_streaming import (
    start_data_streaming,
    stop_data_streaming,
)


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


@router.post(
    "/data_streaming/stop", summary="Stop Streaming the Latest UAV Data in Real Time"
)
async def stop_data_streaming_end_point(uavs: List[str]):
    return stop_data_streaming(uavs)
