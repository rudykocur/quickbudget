"""Dropped Recipe.uid

Revision ID: 484453eb0694
Revises: 1d1a6d42ab5c
Create Date: 2013-03-16 12:42:14.549106

"""

# revision identifiers, used by Alembic.
revision = '484453eb0694'
down_revision = '1d1a6d42ab5c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('recipe', 'uid')


#def downgrade():
#    pass
