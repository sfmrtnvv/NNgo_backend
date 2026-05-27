from __future__ import annotations

from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import AuthRepository
from app.auth.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.core.config import get_settings
from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.redis import get_redis, refresh_key
from app.core.security import (
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User


class AuthService:
    def __init__(self, repository: AuthRepository | None = None) -> None:
        self._repo = repository or AuthRepository()

    async def register(self, session: AsyncSession, data: RegisterRequest) -> TokenResponse:
        existing = await self._repo.get_by_email(session, data.email)
        if existing is not None:
            raise ConflictError("Email already registered")

        user = await self._repo.create_user(
            session,
            email=data.email,
            password_hash=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            birth_date=data.birth_date,
            city=data.city,
        )
        await session.commit()
        return await self._issue_tokens(user)

    async def login(self, session: AsyncSession, data: LoginRequest) -> TokenResponse:
        user = await self._repo.get_by_email(session, data.email)
        if user is None or not user.password_hash:
            raise UnauthorizedError("Invalid email or password")
        if not verify_password(data.password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        return await self._issue_tokens(user)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except JWTError as exc:
            raise UnauthorizedError("Invalid refresh token") from exc

        if payload.get("type") != TOKEN_TYPE_REFRESH:
            raise UnauthorizedError("Invalid refresh token")

        sub = payload.get("sub")
        jti = payload.get("jti")
        if not sub or not jti:
            raise UnauthorizedError("Invalid refresh token")

        redis = get_redis()
        stored_user_id = await redis.get(refresh_key(jti))
        if stored_user_id is None or stored_user_id != str(sub):
            raise UnauthorizedError("Refresh token revoked or expired")

        await redis.delete(refresh_key(jti))
        return await self._issue_tokens_for_user_id(int(sub))

    async def get_user_profile(self, session: AsyncSession, user_id: int) -> UserResponse:
        user = await self._repo.get_by_id(session, user_id)
        if user is None:
            raise UnauthorizedError("User not found")
        return UserResponse.model_validate(user)

    async def _issue_tokens_for_user_id(self, user_id: int) -> TokenResponse:
        access = create_access_token(user_id)
        refresh, jti = create_refresh_token(user_id)
        settings = get_settings()
        ttl_seconds = settings.refresh_token_expire_days * 24 * 60 * 60
        redis = get_redis()
        await redis.set(refresh_key(jti), str(user_id), ex=ttl_seconds)
        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
            expires_in=settings.access_token_expire_minutes * 60,
        )

    async def _issue_tokens(self, user: User) -> TokenResponse:
        return await self._issue_tokens_for_user_id(user.id)
