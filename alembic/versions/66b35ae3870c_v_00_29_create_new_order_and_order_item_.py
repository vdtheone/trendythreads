"""v_00_29_create new order and order_item table

Revision ID: 66b35ae3870c
Revises: 99a14ef20c53
Create Date: 2023-12-13 13:00:04.144010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66b35ae3870c'
down_revision: Union[str, None] = '99a14ef20c53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orderitem',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('order_id', sa.String(), nullable=True),
    sa.Column('product_id', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('total_amount', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orderitem_id'), 'orderitem', ['id'], unique=False)
    op.drop_constraint('order_product_id_fkey', 'order', type_='foreignkey')
    op.drop_column('order', 'quantity')
    op.drop_column('order', 'total_amount')
    op.drop_column('order', 'product_id')
    op.drop_column('order', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('order', sa.Column('product_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('order', sa.Column('total_amount', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('order', sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('order_product_id_fkey', 'order', 'product', ['product_id'], ['id'])
    op.drop_index(op.f('ix_orderitem_id'), table_name='orderitem')
    op.drop_table('orderitem')
    # ### end Alembic commands ###