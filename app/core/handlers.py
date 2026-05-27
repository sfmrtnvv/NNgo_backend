from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
        body: dict = {"detail": exc.detail}
        if exc.code:
            body["code"] = exc.code
        return JSONResponse(status_code=exc.status_code, content=body)
