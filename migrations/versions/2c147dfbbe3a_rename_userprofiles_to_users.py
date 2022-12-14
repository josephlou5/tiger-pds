"""Rename 'UserProfiles' table to 'Users'

Revision ID: 2c147dfbbe3a
Revises: a086201e6650
Create Date: 2022-12-14 00:36:39.276302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c147dfbbe3a'
down_revision = 'a086201e6650'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('UserProfiles', 'Users')


def downgrade():
    op.rename_table('Users', 'UserProfiles')
