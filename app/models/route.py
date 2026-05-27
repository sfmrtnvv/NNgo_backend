from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, TimestampUpdatedMixin

if TYPE_CHECKING:
    from app.models.lookup import BudgetType, Category, RestType
    from app.models.user import User
    from app.models.walk import Walk


class Spot(Base, TimestampMixin):
    __tablename__ = "spots"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    external_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    route_spots: Mapped[list["RouteSpot"]] = relationship(back_populates="spot")


class Route(Base, TimestampUpdatedMixin):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    estimated_time_minutes: Mapped[int | None] = mapped_column(INTEGER(unsigned=True), nullable=True)
    category_id: Mapped[int | None] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("categories.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    budget_type_id: Mapped[int | None] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("budget_types.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    rest_type_id: Mapped[int | None] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("rest_types.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    category: Mapped["Category | None"] = relationship(back_populates="routes")
    budget_type: Mapped["BudgetType | None"] = relationship(back_populates="routes")
    rest_type: Mapped["RestType | None"] = relationship(back_populates="routes")
    route_spots: Mapped[list["RouteSpot"]] = relationship(
        back_populates="route",
        cascade="all, delete-orphan",
        order_by="RouteSpot.spot_order",
    )
    walks: Mapped[list["Walk"]] = relationship(back_populates="route")
    liked_by: Mapped[list["LikedRoute"]] = relationship(back_populates="route")


class RouteSpot(Base):
    __tablename__ = "route_spots"
    __table_args__ = (
        UniqueConstraint("route_id", "spot_id", name="uq_route_spots_route_spot"),
        UniqueConstraint("route_id", "spot_order", name="uq_route_spots_route_order"),
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    route_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("routes.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    spot_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("spots.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    spot_order: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)

    route: Mapped["Route"] = relationship(back_populates="route_spots")
    spot: Mapped["Spot"] = relationship(back_populates="route_spots")


class LikedRoute(Base, TimestampMixin):
    __tablename__ = "liked_routes"
    __table_args__ = (UniqueConstraint("user_id", "route_id", name="uq_liked_routes_user_route"),)

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    route_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("routes.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="liked_routes")
    route: Mapped["Route"] = relationship(back_populates="liked_by")
