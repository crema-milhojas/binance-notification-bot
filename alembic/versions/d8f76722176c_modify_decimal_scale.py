"""modify decimal scale

Revision ID: d8f76722176c
Revises: 4b3699660e1a
Create Date: 2025-06-28 00:52:07.013220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8f76722176c'
down_revision: Union[str, Sequence[str], None] = '4b3699660e1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('arbitration_ustd', 'trans_amount',
               existing_type=sa.NUMERIC(precision=18, scale=2),
               type_=sa.Numeric(precision=18, scale=4),
               existing_nullable=True)
    op.alter_column('arbitration_ustd', 'buy_price',
               existing_type=sa.NUMERIC(precision=18, scale=2),
               type_=sa.Numeric(precision=18, scale=4),
               existing_nullable=True)
    op.alter_column('arbitration_ustd', 'sell_price',
               existing_type=sa.NUMERIC(precision=18, scale=2),
               type_=sa.Numeric(precision=18, scale=4),
               existing_nullable=True)
    op.alter_column('arbitration_ustd', 'spread',
               existing_type=sa.NUMERIC(precision=18, scale=2),
               type_=sa.Numeric(precision=18, scale=4),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('arbitration_ustd', 'spread',
               existing_type=sa.Numeric(precision=18, scale=4),
               type_=sa.NUMERIC(precision=18, scale=2),
               existing_nullable=True)
    op.alter_column('arbitration_ustd', 'sell_price',
               existing_type=sa.Numeric(precision=18, scale=4),
               type_=sa.NUMERIC(precision=18, scale=2),
               existing_nullable=True)
    op.alter_column('arbitration_ustd', 'buy_price',
               existing_type=sa.Numeric(precision=18, scale=4),
               type_=sa.NUMERIC(precision=18, scale=2),
               existing_nullable=True)
    op.alter_column('arbitration_ustd', 'trans_amount',
               existing_type=sa.Numeric(precision=18, scale=4),
               type_=sa.NUMERIC(precision=18, scale=2),
               existing_nullable=True)
    # ### end Alembic commands ###
