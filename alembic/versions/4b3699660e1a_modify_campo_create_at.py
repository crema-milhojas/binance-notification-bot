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
    """Upgrade schema."""
    # Ejemplo: renombrar columna createAt a create_at y cambiar tipo/default
    with op.batch_alter_table('arbitration_ustd') as batch_op:
        # Renombrar columna si es necesario
        batch_op.alter_column('createAt', new_column_name='create_at', existing_type=sa.DateTime(), existing_nullable=True)
        # Cambiar el default a now() si es necesario
        batch_op.alter_column('create_at', server_default=sa.text('now()'), existing_type=sa.DateTime(), existing_nullable=True)

def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('arbitration_ustd') as batch_op:
        # Revertir el default
        batch_op.alter_column('create_at', server_default=None, existing_type=sa.DateTime(), existing_nullable=True)
        # Renombrar de vuelta si es necesario
        batch_op.alter_column('create_at', new_column_name='createAt', existing_type=sa.DateTime(), existing_nullable=True)