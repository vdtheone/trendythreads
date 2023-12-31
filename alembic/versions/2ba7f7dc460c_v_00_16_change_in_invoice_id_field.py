"""V_00_16_change in invoice_id field

Revision ID: 2ba7f7dc460c
Revises: 3cd3f58fd078
Create Date: 2023-11-07 11:31:50.882517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2ba7f7dc460c"
down_revision: Union[str, None] = "3cd3f58fd078"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "invoice",
        "invoice_id",
        existing_type=sa.INTEGER(),
        nullable=True,
        autoincrement=True,
    )
    op.create_index(
        op.f("ix_invoice_invoice_id"), "invoice", ["invoice_id"], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_invoice_invoice_id"), table_name="invoice")
    op.alter_column(
        "invoice",
        "invoice_id",
        existing_type=sa.INTEGER(),
        nullable=False,
        autoincrement=True,
    )
    # ### end Alembic commands ###
