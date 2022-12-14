"""Add Admins table

Revision ID: a086201e6650
Revises: 36a96f29e834
Create Date: 2022-12-12 18:37:23.602686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a086201e6650'
down_revision = '36a96f29e834'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Admins',
    sa.Column('netid', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('netid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Admins')
    # ### end Alembic commands ###