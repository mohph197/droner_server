from fastapi import APIRouter, Depends

from .uavs_router import router as uavs_router


router = APIRouter(prefix="/api")


router.include_router(uavs_router)
