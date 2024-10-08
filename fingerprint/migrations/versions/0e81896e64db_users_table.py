"""users table

Revision ID: 0e81896e64db
Revises: 
Create Date: 2020-03-30 19:16:47.126568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e81896e64db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fingerprint', sa.String(length=32), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('second_name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_fingerprint'), 'user', ['fingerprint'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_fingerprint'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
