"""modify campo create at

Revision ID: 4b3699660e1a
Revises: 83f3eb0e0ec3
Create Date: 2025-06-28 00:36:10.958352
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b3699660e1a'
down_revision: Union[str, Sequence[str], None] = '83f3eb0e0ec3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: modificar campo create_at si existe."""
    conn = op.get_bind()

    result = conn.execute(
        sa.text("""
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'arbitration_ustd'
              AND column_name = 'create_at'
        """)
    ).fetchone()

    if result:
        op.alter_column(
            'arbitration_ustd',
            'create_at',
            existing_type=sa.DateTime(),
            server_default=sa.text('now()'),
            existing_nullable=True
        )
    else:
        print("❗La columna 'create_at' no existe en 'arbitration_ustd'. No se puede alterar.")


def downgrade() -> None:
    """Downgrade schema: quitar default de create_at si existe."""
    conn = op.get_bind()

    result = conn.execute(
        sa.text("""
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'arbitration_ustd'
              AND column_name = 'create_at'
        """)
    ).fetchone()

    if result:
        op.alter_column(
            'arbitration_ustd',
            'create_at',
            server_default=None,
            existing_type=sa.DateTime(),
            existing_nullable=True
        )
    else:
        print("❗La columna 'create_at' no existe. No se puede revertir el default.")
