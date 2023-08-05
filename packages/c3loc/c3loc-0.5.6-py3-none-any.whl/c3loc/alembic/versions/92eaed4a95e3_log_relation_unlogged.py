"""log_relation_unlogged

Revision ID: 92eaed4a95e3
Revises: 720d3e9a9af0
Create Date: 2021-03-18 09:41:27.914377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92eaed4a95e3'
down_revision = '720d3e9a9af0'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE log SET UNLOGGED;")


def downgrade():
    op.execute("ALTER TABLE log SET LOGGED;")
