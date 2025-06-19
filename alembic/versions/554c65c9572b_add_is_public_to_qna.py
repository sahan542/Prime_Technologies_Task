from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '554c65c9572b'
down_revision = 'a8177bf26113'  # your previous revision ID
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Add column with a default value (only for existing rows)
    op.add_column('qna', sa.Column('is_public', sa.Boolean(), nullable=False, server_default=sa.text('false')))

    # Step 2: Remove default if not desired permanently
    op.alter_column('qna', 'is_public', server_default=None)

def downgrade():
    op.drop_column('qna', 'is_public')
