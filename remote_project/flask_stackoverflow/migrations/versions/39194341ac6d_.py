"""empty message

Revision ID: 39194341ac6d
Revises: 
Create Date: 2018-08-03 17:37:22.759088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39194341ac6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###