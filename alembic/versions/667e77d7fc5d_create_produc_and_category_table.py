"""create produc and category table

Revision ID: 667e77d7fc5d
Revises: 6d6f4607cb47
Create Date: 2023-10-26 17:43:34.307288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "667e77d7fc5d"
down_revision: Union[str, None] = "6d6f4607cb47"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "category",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_category_id"), "category", ["id"], unique=False)
    op.create_table(
        "product",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("category_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("brand", sa.String(), nullable=True),
        sa.Column("stockquantity", sa.Integer(), nullable=True),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_id"), "product", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_product_id"), table_name="product")
    op.drop_table("product")
    op.drop_index(op.f("ix_category_id"), table_name="category")
    op.drop_table("category")
    # ### end Alembic commands ###
