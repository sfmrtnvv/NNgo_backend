"""initial schema (all tables from ORM metadata)

Revision ID: 20260525_0001
Revises:
Create Date: 2026-05-25

"""

from typing import Sequence, Union

from alembic import op

revision: str = "20260525_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from app.database.base import Base

    import app.models  # noqa: F401

    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    from app.database.base import Base

    import app.models  # noqa: F401

    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
