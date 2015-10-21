"""empty message

Revision ID: 4a887b3789f3
Revises: 558ee0a8fe63
Create Date: 2015-10-20 14:35:00.559664

"""

# revision identifiers, used by Alembic.
revision = '4a887b3789f3'
down_revision = '558ee0a8fe63'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_score', sa.Column('num_questions', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_score', 'num_questions')
    ### end Alembic commands ###