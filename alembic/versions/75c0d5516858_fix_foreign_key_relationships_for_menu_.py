"""Fix foreign key relationships for menu and menu_item

Revision ID: 75c0d5516858
Revises: 9de869433902
Create Date: 2025-01-30 03:16:19.830091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75c0d5516858'
down_revision: Union[str, None] = '9de869433902'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
