"""add categories and products

Revision ID: 3b98bcbde23c
Revises: 6f3c1b557da0
Create Date: 2026-10-01 11:04:01.180138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b98bcbde23c'
down_revision: Union[str, Sequence[str], None] = '6f3c1b557da0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
