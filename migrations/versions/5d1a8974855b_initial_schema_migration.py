"""Initial schema migration

Revision ID: 5d1a8974855b
Revises: n/a
Create Date: 2020-03-11 13:35:49.613211

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5d1a8974855b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('race', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_table(
        'weapons',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('owner', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['owner'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'offers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'offers_users_association_table',
        sa.Column('offers_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('users_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['offers_id'], ['offers.id'], ),
        sa.ForeignKeyConstraint(['users_id'], ['users.id'], )
    )

    op.create_table(
        'offers_weapons_association_table',
        sa.Column('offers_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('weapons_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['offers_id'], ['offers.id'], ),
        sa.ForeignKeyConstraint(['weapons_id'], ['weapons.id'], )
    )


def downgrade():
    op.drop_table('offers_weapons_association_table')
    op.drop_table('offers_users_association_table')
    op.drop_table('offers')
    op.drop_table('weapons')
    op.drop_table('users')
