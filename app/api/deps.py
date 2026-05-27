from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import AuthRepository
from app.core.auth_scheme import bearer_scheme
from app.core.exceptions import UnauthorizedError
from app.core.security import TOKEN_TYPE_ACCESS, safe_decode_token
from app.database.session import get_db
from app.models.user import User


async def get_current_user_id(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> int:
    if getattr(request.state, "authenticated", False) and request.state.user_id:
        return int(request.state.user_id)

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedError("Missing or invalid authorization header")

    payload = safe_decode_token(credentials.credentials)
    if payload is None or payload.get("type") != TOKEN_TYPE_ACCESS:
        raise UnauthorizedError("Invalid or expired access token")

    sub = payload.get("sub")
    if not sub:
        raise UnauthorizedError("Invalid access token")

    return int(sub)


async def get_current_user(
    user_id: Annotated[int, Depends(get_current_user_id)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    user = await AuthRepository().get_by_id(session, user_id)
    if user is None:
        raise UnauthorizedError("User not found")
    return user


__all__ = ["get_db", "get_current_user", "get_current_user_id", "bearer_scheme"]
