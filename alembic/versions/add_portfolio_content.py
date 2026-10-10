"""Add profile CV and portfolio content resources."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = 'add_portfolio_content'
down_revision = ('add_packages', 'c4a53769ce4f')
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('cv_url', sa.String(), nullable=True))
    op.add_column('users', sa.Column('cv_filename', sa.String(), nullable=True))
    op.add_column('users', sa.Column('cv_updated_at', sa.DateTime(), nullable=True))
    for table, columns in {
        'experiences': [('title', sa.String(), False), ('organization', sa.String(), False), ('description', sa.Text(), True), ('start_date', sa.DateTime(), True), ('end_date', sa.DateTime(), True), ('is_current', sa.Boolean(), True)],
        'achievements': [('title', sa.String(), False), ('organization', sa.String(), True), ('description', sa.Text(), True), ('achieved_at', sa.DateTime(), True)],
        'event_photos': [('title', sa.String(), False), ('description', sa.Text(), True), ('image_url', sa.String(), False), ('event_date', sa.DateTime(), True)],
    }.items():
        op.create_table(table, sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True), *[sa.Column(n, t, nullable=nullable) for n, t, nullable in columns], sa.Column('created_at', sa.DateTime(), nullable=True), sa.Column('updated_at', sa.DateTime(), nullable=True), sa.Column('is_deleted', sa.Boolean(), nullable=True), sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False))

def downgrade():
    for table in ('event_photos', 'achievements', 'experiences'): op.drop_table(table)
    op.drop_column('users', 'cv_updated_at'); op.drop_column('users', 'cv_filename'); op.drop_column('users', 'cv_url')
