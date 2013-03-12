"""initial table structure

Revision ID: 4221da5e07a0
Revises: None
Create Date: 2013-03-12 19:19:04.050975

"""

# revision identifiers, used by Alembic.
revision = '4221da5e07a0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('recipe',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('uid', sa.Unicode(255), primary_key=True),
        sa.Column('total', sa.Numeric(18,2), nullable=False),
        sa.Column('date', sa.Date, nullable=True)
    )

    op.create_table('recipe_image',
        sa.Column('uid', sa.Unicode(255), primary_key=True),
        sa.Column('recipeId', sa.Integer, sa.ForeignKey('recipe.id'), nullable=True),
        sa.Column('contentPath', sa.Unicode(255)),
        sa.Column('crc', sa.Unicode(20)),
        sa.Column('md5', sa.Unicode(32)))


def downgrade():
    op.drop_table('recipe_image')
    op.drop_table('recipe')
