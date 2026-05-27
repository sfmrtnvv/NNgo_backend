from __future__ import annotations

import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.mixins import TimestampMixin, TimestampUpdatedMixin

if TYPE_CHECKING:
    from app.models.user import User


class FriendStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    blocked = "blocked"


class Match(Base, TimestampMixin):
    __tablename__ = "matches"
    __table_args__ = (UniqueConstraint("first_user_id", "second_user_id", name="uq_matches_users"),)

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    first_user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    second_user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    is_mutual: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    first_user: Mapped["User"] = relationship(
        back_populates="matches_as_first",
        foreign_keys=[first_user_id],
    )
    second_user: Mapped["User"] = relationship(
        back_populates="matches_as_second",
        foreign_keys=[second_user_id],
    )
    chat: Mapped["Chat | None"] = relationship(
        back_populates="match",
        uselist=False,
    )


class Chat(Base, TimestampUpdatedMixin):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    match_id: Mapped[int | None] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("matches.id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=True,
        nullable=True,
    )

    match: Mapped["Match | None"] = relationship(back_populates="chat")
    participants: Mapped[list["ChatParticipant"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )


class ChatParticipant(Base):
    __tablename__ = "chat_participants"

    chat_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("chats.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
    )

    chat: Mapped["Chat"] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship(back_populates="chat_participations")


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("chats.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    sender_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)

    chat: Mapped["Chat"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship(back_populates="messages_sent")


class Friend(Base, TimestampUpdatedMixin):
    __tablename__ = "friends"
    __table_args__ = (UniqueConstraint("user_id", "friend_id", name="uq_friends_pair"),)

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    friend_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    status: Mapped[FriendStatus] = mapped_column(
        Enum(FriendStatus, values_callable=lambda obj: [item.value for item in obj]),
        nullable=False,
        default=FriendStatus.pending,
    )

    user: Mapped["User"] = relationship(
        back_populates="friends_initiated",
        foreign_keys=[user_id],
    )
    friend: Mapped["User"] = relationship(
        back_populates="friends_received",
        foreign_keys=[friend_id],
    )
