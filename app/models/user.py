from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, String, Text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampUpdatedMixin

if TYPE_CHECKING:
    from app.models.preference import Notification, UserPreference
    from app.models.route import LikedRoute
    from app.models.social import ChatParticipant, Friend, Match, Message
    from app.models.walk import Walk, WalkApplication


class User(Base, TimestampUpdatedMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    vk_id: Mapped[int | None] = mapped_column(BIGINT(unsigned=True), unique=True, nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    age_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)

    walks_as_first: Mapped[list["Walk"]] = relationship(
        back_populates="first_user",
        foreign_keys="Walk.first_user_id",
    )
    walks_as_second: Mapped[list["Walk"]] = relationship(
        back_populates="second_user",
        foreign_keys="Walk.second_user_id",
    )
    walk_applications: Mapped[list["WalkApplication"]] = relationship(back_populates="applicant")
    matches_as_first: Mapped[list["Match"]] = relationship(
        back_populates="first_user",
        foreign_keys="Match.first_user_id",
    )
    matches_as_second: Mapped[list["Match"]] = relationship(
        back_populates="second_user",
        foreign_keys="Match.second_user_id",
    )
    chat_participations: Mapped[list["ChatParticipant"]] = relationship(back_populates="user")
    messages_sent: Mapped[list["Message"]] = relationship(back_populates="sender")
    friends_initiated: Mapped[list["Friend"]] = relationship(
        back_populates="user",
        foreign_keys="Friend.user_id",
    )
    friends_received: Mapped[list["Friend"]] = relationship(
        back_populates="friend",
        foreign_keys="Friend.friend_id",
    )
    liked_routes: Mapped[list["LikedRoute"]] = relationship(back_populates="user")
    preferences: Mapped["UserPreference | None"] = relationship(
        back_populates="user",
        uselist=False,
    )
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user")
