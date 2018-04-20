"""empty message

Revision ID: 8af81e499422
Revises: 1d3a41021173
Create Date: 2018-04-18 21:55:28.532637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8af81e499422'
down_revision = '1d3a41021173'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('businesses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('category', sa.String(length=60), nullable=False),
    sa.Column('location', sa.String(length=60), nullable=False),
    sa.Column('description', sa.String(length=60), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('businessId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['businessId'], ['businesses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('businesses')
    op.drop_table('users')
    # ### end Alembic commands ###