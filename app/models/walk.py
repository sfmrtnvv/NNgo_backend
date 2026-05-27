from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampUpdatedMixin

if TYPE_CHECKING:
    from app.models.lookup import ApplicationStatus, CompanyType, WalkStatus
    from app.models.route import Route
    from app.models.user import User


class Walk(Base, TimestampUpdatedMixin):
    __tablename__ = "walks"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    route_id: Mapped[int | None] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("routes.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    first_user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    second_user_id: Mapped[int | None] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    company_type_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("company_types.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    status_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("walk_statuses.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    route: Mapped["Route | None"] = relationship(back_populates="walks")
    first_user: Mapped["User"] = relationship(
        back_populates="walks_as_first",
        foreign_keys=[first_user_id],
    )
    second_user: Mapped["User | None"] = relationship(
        back_populates="walks_as_second",
        foreign_keys=[second_user_id],
    )
    company_type: Mapped["CompanyType"] = relationship(back_populates="walks")
    status: Mapped["WalkStatus"] = relationship(back_populates="walks")
    applications: Mapped[list["WalkApplication"]] = relationship(
        back_populates="walk",
        cascade="all, delete-orphan",
    )


class WalkApplication(Base, TimestampUpdatedMixin):
    __tablename__ = "walk_applications"
    __table_args__ = (
        UniqueConstraint("walk_id", "applicant_user_id", name="uq_walk_applications_walk_user"),
    )

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    walk_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("walks.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    applicant_user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    application_status_id: Mapped[int] = mapped_column(
        TINYINT(unsigned=True),
        ForeignKey("application_statuses.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )

    walk: Mapped["Walk"] = relationship(back_populates="applications")
    applicant: Mapped["User"] = relationship(back_populates="walk_applications")
    application_status: Mapped["ApplicationStatus"] = relationship(back_populates="walk_applications")
