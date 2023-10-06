from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.lib.broadcaster import send_notification
from app.web.fastapi.utils.exception_handler_middleware import (
    ExceptionHandlerMiddleware,
)

from .controllers.main_router import router as main_rounter


def start_fastapi_webserver() -> FastAPI:
    app = FastAPI(
        title="Fleet Management System API",
        docs_url="/api/docs/swagger",
        redoc_url="/api/docs/redoc",
        openapi_url="/api/docs/openapi.json",
        version="0.1.0",
    )

    app.add_middleware(ExceptionHandlerMiddleware)

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(main_rounter)

    @app.get("/", summary="Api Summary", tags=["api"])
    async def summary():
        return {
            "message": "Hello From Fleet Management API",
            "swagger": "/api/docs/swagger",
            "redoc": "/api/docs/redoc",
            "openapi": "/api/docs/openapi.json",
        }

    return app
