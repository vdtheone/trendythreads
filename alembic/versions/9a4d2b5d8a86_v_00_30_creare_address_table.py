"""v_00_30_creare address table

Revision ID: 9a4d2b5d8a86
Revises: 66b35ae3870c
Create Date: 2024-02-20 00:00:11.202804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a4d2b5d8a86'
down_revision: Union[str, None] = '66b35ae3870c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
