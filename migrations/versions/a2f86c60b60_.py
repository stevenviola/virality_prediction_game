"""empty message

Revision ID: a2f86c60b60
Revises: 2ae95cecc3a0
Create Date: 2015-10-07 11:08:48.345571

"""

# revision identifiers, used by Alembic.
revision = 'a2f86c60b60'
down_revision = '2ae95cecc3a0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deleted_post')
    op.add_column('post', sa.Column('show_to_users', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'show_to_users')
    op.create_table('deleted_post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('date_created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('date_modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('score', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('reddit_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('subreddit', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('month_posted', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('year_posted', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('hand_validatd', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'deleted_post_pkey')
    )
    ### end Alembic commands ###
