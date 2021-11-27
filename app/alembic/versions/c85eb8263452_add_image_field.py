"""Add image field

Revision ID: c85eb8263452
Revises: 2f493c065c75
Create Date: 2021-11-27 21:38:10.977411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c85eb8263452'
down_revision = '2f493c065c75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('image', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'image')
    # ### end Alembic commands ###
