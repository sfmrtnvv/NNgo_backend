from __future__ import annotations

from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.security import TOKEN_TYPE_ACCESS, safe_decode_token

PUBLIC_PATHS: frozenset[str] = frozenset(
    {
        "/health",
        "/auth/register",
        "/auth/login",
        "/auth/refresh",
        "/docs",
        "/redoc",
        "/openapi.json",
    }
)

PROTECTED_PATHS: frozenset[str] = frozenset(
    {
        "/auth/me",
        "/protected-ping",
    }
)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Validates JWT on protected paths and attaches user id to request.state.
    Public auth endpoints (register/login/refresh) stay open.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path
        request.state.user_id = None
        request.state.authenticated = False

        if request.method == "OPTIONS" or path in PUBLIC_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
            payload = safe_decode_token(token)
            if payload and payload.get("type") == TOKEN_TYPE_ACCESS and payload.get("sub"):
                request.state.user_id = int(payload["sub"])
                request.state.authenticated = True

        if path in PROTECTED_PATHS and not request.state.authenticated:
            return JSONResponse(
                status_code=401,
                content={"detail": "Not authenticated", "code": "unauthorized"},
            )

        return await call_next(request)
