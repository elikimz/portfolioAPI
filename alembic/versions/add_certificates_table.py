"""Add certificates table

Revision ID: add_certificates_table
Revises: 458121a0cfe2
Create Date: 2025-03-25 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_certificates_table'
down_revision: Union[str, None] = '458121a0cfe2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('certificates',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('issuer', sa.String(), nullable=False),
    sa.Column('issue_date', sa.DateTime(), nullable=True),
    sa.Column('expiry_date', sa.DateTime(), nullable=True),
    sa.Column('credential_id', sa.String(), nullable=True),
    sa.Column('credential_url', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('certificates')
