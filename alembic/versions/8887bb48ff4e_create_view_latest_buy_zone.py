"""create view latest buy zone

Revision ID: 8887bb48ff4e
Revises: 71599ba466a3
Create Date: 2025-08-30 17:23:05.211615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8887bb48ff4e'
down_revision: Union[str, Sequence[str], None] = '71599ba466a3'
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
        ORDER BY bz.user, bz.create_at DESC
    """)


def downgrade() -> None:
    # Elimina la vista si existe
    op.execute("DROP VIEW IF EXISTS v_latest_buy_zone")