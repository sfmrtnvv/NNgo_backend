from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, TimestampUpdatedMixin

if TYPE_CHECKING:
    from app.models.lookup import BudgetType, RestType
    from app.models.user import User


class UserPreference(Base, TimestampUpdatedMixin):
    __tablename__ = "user_preferences"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
    preferred_budget_id: Mapped[int | None] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("budget_types.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    preferred_rest_type_id: Mapped[int | None] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("rest_types.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    user: Mapped["User"] = relationship(back_populates="preferences")
    preferred_budget: Mapped["BudgetType | None"] = relationship(back_populates="user_preferences")
    preferred_rest_type: Mapped["RestType | None"] = relationship(back_populates="user_preferences")


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user: Mapped["User"] = relationship(back_populates="notifications")
