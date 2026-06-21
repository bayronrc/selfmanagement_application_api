"""fix fk orders batch_id

Revision ID: fef61af9fb4e
Revises: 62bdbcc9e75d
Create Date: 2026-06-18 08:53:57.047222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'fef61af9fb4e'
down_revision: Union[str, Sequence[str], None] = '62bdbcc9e75d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('order_batches',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('file_name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('uploaded_by', sa.INTEGER(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], name=op.f('order_batches_uploaded_by_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('order_batches_pkey'))
    )
    op.create_table('orders',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('batch_id', sa.INTEGER(), nullable=False),
    sa.Column('fecha', sa.VARCHAR(length=20), nullable=False),
    sa.Column('id_profesional', sa.VARCHAR(length=100), nullable=True),
    sa.Column('profesional', sa.VARCHAR(length=255), nullable=True),
    sa.Column('no_orden', sa.VARCHAR(length=100), nullable=True),
    sa.Column('codigo', sa.VARCHAR(length=100), nullable=True),
    sa.Column('procedimiento', sa.VARCHAR(length=500), nullable=True),
    sa.Column('cantidad', sa.INTEGER(), nullable=True),
    sa.Column('dosis', sa.VARCHAR(length=100), nullable=True),
    sa.Column('dias_tto', sa.INTEGER(), nullable=True),
    sa.Column('status', sa.VARCHAR(length=20), nullable=False),
    sa.Column('error_message', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], ['order_batches.id'], name=op.f('orders_batch_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('orders_pkey'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('orders')
    op.drop_table('order_batches')
