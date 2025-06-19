"""Change product_id to String in OrderItem

Revision ID: 1f9cbb95d7d9
Revises: 16e204b35b52
Create Date: 2025-06-18 12:42:57.496001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1f9cbb95d7d9'
down_revision: Union[str, None] = '16e204b35b52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'order_items',
        'product_id',
        existing_type=sa.Integer(),
        type_=sa.String(),
        existing_nullable=False
    )

def downgrade() -> None:
    op.alter_column(
        'order_items',
        'product_id',
        existing_type=sa.String(),
        type_=sa.Integer(),
        existing_nullable=False
    )
