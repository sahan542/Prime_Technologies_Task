"""Add address fields to Order model

Revision ID: 16e204b35b52
Revises: c3ca5cce82e8
Create Date: 2025-06-18 12:05:15.640923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '16e204b35b52'
down_revision: Union[str, None] = 'c3ca5cce82e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('orders', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('street_address', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('apartment', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('city', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('phone', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('email', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('create_account', sa.Boolean(), nullable=True))
    op.add_column('orders', sa.Column('ship_different', sa.Boolean(), nullable=True))
    op.add_column('orders', sa.Column('order_notes', sa.Text(), nullable=True))
    op.add_column('orders', sa.Column('shipping_method', sa.String(), nullable=True))
    op.add_column('orders', sa.Column('shipping_cost', sa.Float(), nullable=True))
    op.add_column('orders', sa.Column('service_fee', sa.Float(), nullable=True))
    op.add_column('orders', sa.Column('payment_method', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('slug', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('img', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('price', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False),
    sa.Column('original_price', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('sold_recently', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('brand', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('benefits', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('visible', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('products_pkey')),
    sa.UniqueConstraint('slug', name=op.f('products_slug_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_table('cart_item',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('cart_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('price', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('img', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('slug', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.user_id'], name=op.f('cart_item_cart_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('cart_item_pkey'))
    )
    op.create_table('cart',
    sa.Column('user_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('user_id', name=op.f('cart_pkey'))
    )
    op.create_table('wishlist',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('wishlist_pkey')),
    sa.UniqueConstraint('user_id', 'product_id', name=op.f('unique_user_product_wishlist'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    op.create_index(op.f('ix_wishlist_id'), 'wishlist', ['id'], unique=False)
    op.create_table('orders',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('orders_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_amount', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('payment_status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='orders_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='orders_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    op.create_table('order_items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name=op.f('order_items_order_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('order_items_pkey'))
    )
    op.create_index(op.f('ix_order_items_id'), 'order_items', ['id'], unique=False)
    # ### end Alembic commands ###
