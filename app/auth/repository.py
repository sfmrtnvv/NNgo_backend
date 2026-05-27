from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class AuthRepository:
    async def get_by_email(self, session: AsyncSession, email: str) -> User | None:
        result = await session.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, session: AsyncSession, user_id: int) -> User | None:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create_user(
        self,
        session: AsyncSession,
        *,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        birth_date=None,
        city: str | None = None,
    ) -> User:
        user = User(
            email=email.lower(),
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            city=city,
        )
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user
