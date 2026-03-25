"""Add user_credits table

Revision ID: 0002
Revises: 0001
Create Date: 2025-01-01 00:00:01
"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user_credits',
        sa.Column('id',         sa.String(36),  primary_key=True),
        sa.Column('user_id',    sa.String(36),  sa.ForeignKey('users.id'), nullable=False, unique=True),
        sa.Column('credits',    sa.Integer(),   server_default='100'),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )


def downgrade() -> None:
    op.drop_table('user_credits')
