"""Add field for users who can deliver

Revision ID: dbbdeae4c65d
Revises: f2b8b767218a
Create Date: 2022-12-12 13:17:15.243047

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'dbbdeae4c65d'
down_revision = 'f2b8b767218a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('UserProfiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('does_delivery', sa.Boolean(), nullable=True))

    # make a local Table object
    table = sa.Table(
        'UserProfiles',
        sa.MetaData(),
        sa.Column('netid', sa.Integer, primary_key=True),
        sa.Column('does_delivery', sa.Boolean()))
    # update all rows to have a non-null value
    connection = op.get_bind()
    connection.execute(table.update().values(does_delivery=False))

    with op.batch_alter_table('UserProfiles', schema=None) as batch_op:
        batch_op.alter_column('does_delivery', existing_type=sa.Boolean(),
        nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('UserProfiles', schema=None) as batch_op:
        batch_op.drop_column('does_delivery')

    # ### end Alembic commands ###
