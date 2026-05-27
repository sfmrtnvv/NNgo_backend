from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.route import Route
    from app.models.user import UserPreference
    from app.models.walk import Walk, WalkApplication


class CompanyType(Base, TimestampMixin):
    __tablename__ = "company_types"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    walks: Mapped[list["Walk"]] = relationship(back_populates="company_type")


class BudgetType(Base, TimestampMixin):
    __tablename__ = "budget_types"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    min_price: Mapped[int | None] = mapped_column(INTEGER(unsigned=True), nullable=True)
    max_price: Mapped[int | None] = mapped_column(INTEGER(unsigned=True), nullable=True)

    routes: Mapped[list["Route"]] = relationship(back_populates="budget_type")
    user_preferences: Mapped[list["UserPreference"]] = relationship(back_populates="preferred_budget")


class RestType(Base, TimestampMixin):
    __tablename__ = "rest_types"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    routes: Mapped[list["Route"]] = relationship(back_populates="rest_type")
    user_preferences: Mapped[list["UserPreference"]] = relationship(back_populates="preferred_rest_type")


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    routes: Mapped[list["Route"]] = relationship(back_populates="category")


class WalkStatus(Base, TimestampMixin):
    __tablename__ = "walk_statuses"

    id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    walks: Mapped[list["Walk"]] = relationship(back_populates="status")


class ApplicationStatus(Base, TimestampMixin):
    __tablename__ = "application_statuses"

    id: Mapped[int] = mapped_column(TINYINT(unsigned=True), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    walk_applications: Mapped[list["WalkApplication"]] = relationship(
        back_populates="application_status"
    )
