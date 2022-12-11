"""Make address non nullable

Revision ID: db54ffa7fbbb
Revises: a0b6a87db8eb
Create Date: 2022-12-11 17:48:40.982942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db54ffa7fbbb'
down_revision = 'a0b6a87db8eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('UserProfiles', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('UserProfiles', schema=None) as batch_op:
        batch_op.alter_column('address',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###
