"""Added Recipe.note

Revision ID: 9cffcf88f2e
Revises: 308b015a0cc9
Create Date: 2013-03-12 20:56:13.712564

"""

# revision identifiers, used by Alembic.
revision = '9cffcf88f2e'
down_revision = '308b015a0cc9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('recipe', sa.Column('note', sa.Unicode(255)))


def downgrade():
    op.drop_column('recipe', 'note')
