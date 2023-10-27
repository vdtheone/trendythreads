"""V_00_6_remove otp column form user table

Revision ID: 6d6f4607cb47
Revises: ad76846bd194
Create Date: 2023-10-26 11:36:34.429413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6d6f4607cb47"
down_revision: Union[str, None] = "ad76846bd194"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "otp")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("otp", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###