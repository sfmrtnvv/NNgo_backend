"""
ORM models for MySQL 8 schema (NNgo_bd_mysql8.sql).

Import this package before Alembic autogenerate so all tables are registered on Base.metadata.
"""

from app.database.base import Base
from app.models.lookup import (
    ApplicationStatus,
    BudgetType,
    Category,
    CompanyType,
    RestType,
    WalkStatus,
)
from app.models.preference import Notification, UserPreference
from app.models.route import LikedRoute, Route, RouteSpot, Spot
from app.models.social import Chat, ChatParticipant, Friend, FriendStatus, Match, Message
from app.models.user import User
from app.models.walk import Walk, WalkApplication

__all__ = [
    "Base",
    "User",
    "CompanyType",
    "BudgetType",
    "RestType",
    "Category",
    "WalkStatus",
    "ApplicationStatus",
    "Spot",
    "Route",
    "RouteSpot",
    "LikedRoute",
    "Walk",
    "WalkApplication",
    "Match",
    "Chat",
    "ChatParticipant",
    "Message",
    "Friend",
    "FriendStatus",
    "UserPreference",
    "Notification",
]
