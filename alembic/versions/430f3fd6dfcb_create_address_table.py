"""Create address table

Revision ID: 430f3fd6dfcb
Revises: 9a4d2b5d8a86
Create Date: 2024-02-20 23:06:25.902251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '430f3fd6dfcb'
down_revision: Union[str, None] = '9a4d2b5d8a86'
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
