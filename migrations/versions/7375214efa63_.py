"""empty message

Revision ID: 7375214efa63
Revises: b85b792c3e03
Create Date: 2019-02-22 23:07:23.049967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7375214efa63'
down_revision = 'b85b792c3e03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('lexeme', sa.String(length=144), nullable=False))
    op.drop_column('item', 'name')
    op.add_column('user_item', sa.Column('name', sa.String(length=144), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_item', 'name')
    op.add_column('item', sa.Column('name', sa.VARCHAR(length=144), autoincrement=False, nullable=False))
    op.drop_column('item', 'lexeme')
    # ### end Alembic commands ###
