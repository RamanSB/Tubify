"""URL & Length added to song table

Revision ID: 55804e844338
Revises: e9f22a0fa710
Create Date: 2019-04-27 22:11:56.098573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55804e844338'
down_revision = 'e9f22a0fa710'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song', sa.Column('length', sa.String(length=5), nullable=True))
    op.add_column('song', sa.Column('url', sa.LargeBinary(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('song', 'url')
    op.drop_column('song', 'length')
    # ### end Alembic commands ###
