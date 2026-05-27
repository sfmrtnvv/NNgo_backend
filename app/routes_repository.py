from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.route import Route
from app.routes_schemas import RouteCreateSchema


class RoutesRepository:

    @staticmethod
    async def get_routes(session: AsyncSession):
        result = await session.execute(
            select(Route)
        )

        return result.scalars().all()