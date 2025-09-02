"""se cambiará vista

Revision ID: 49e37998e758
Revises: 050f8db5b3dd
Create Date: 2025-08-30 21:37:33.838423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49e37998e758'
down_revision: Union[str, Sequence[str], None] = '050f8db5b3dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crea la vista para obtener el último precio de compra por usuario
    op.execute("""
        CREATE OR REPLACE VIEW v_latest_buy_zone AS
        SELECT DISTINCT ON (bz.user)
            bz.id,
            bz.user,
            bz.buy_price,
            bz.create_at
        FROM buy_zone bz
        where bz.status = true
        ORDER BY bz.user, bz.create_at DESC
    """)


def downgrade() -> None:
    # Elimina la vista si existe
    op.execute("DROP VIEW IF EXISTS v_latest_buy_zone")
