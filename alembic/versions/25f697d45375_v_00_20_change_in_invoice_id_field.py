"""V_00_20_change in invoice_id field

Revision ID: 25f697d45375
Revises: d52b2e7db9fd
Create Date: 2023-11-07 12:26:34.781396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "25f697d45375"
down_revision: Union[str, None] = "d52b2e7db9fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_invoice_invoice_id", table_name="invoice")
    op.create_unique_constraint(None, "invoice", ["invoice_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "invoice", type_="unique")
    op.create_index("ix_invoice_invoice_id", "invoice", ["invoice_id"], unique=False)
    # ### end Alembic commands ###
