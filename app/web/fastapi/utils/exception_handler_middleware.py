from typing import Callable
from fastapi import Request, status
from fastapi.exceptions import (
    RequestValidationError,
    HTTPException,
    ResponseValidationError,
)
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

        self.app = app

    async def dispatch(self, request: Request, call_next: Callable):
        try:
            return await call_next(request)
        except Exception as exception:
            try:
                if isinstance(exception, ValueError):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "code": "INTERNAL_SERVER_ERROR",
                            "message": str(exception),
                        },
                    )

                if isinstance(exception, RequestValidationError):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=exception.errors(),
                    )

                if isinstance(exception, ResponseValidationError):
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail={
                            "code": "INTERNAL_SERVER_ERROR",
                            "message": exception.errors(),
                        },
                    )

                if isinstance(exception, HTTPException):
                    raise HTTPException(
                        status_code=exception.status_code,
                        detail={"code": "HTTP_EXCEPTION", "message": exception.detail},
                    )

                if isinstance(exception, Exception):
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail={
                            "code": "INTERNAL_SERVER_ERROR",
                            "message": str(exception),
                        },
                    )

                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={"code": "INTERNAL_SERVER_ERROR", "message": "unkown error"},
                )
            except HTTPException as exception:
                return JSONResponse(
                    status_code=exception.status_code,
                    content={
                        "method": request.method,
                        "path": request.url.path,
                        "status": exception.status_code,
                        "error": exception.detail,
                    },
                )
