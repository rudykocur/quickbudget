"""added import history data

Revision ID: 308b015a0cc9
Revises: 4221da5e07a0
Create Date: 2013-03-12 19:50:20.315532

"""

# revision identifiers, used by Alembic.
revision = '308b015a0cc9'
down_revision = '4221da5e07a0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'bank_import_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('contentPath', sa.Unicode(255)),
        sa.Column('type', sa.Unicode(30)),
        sa.Column('date', sa.DateTime)
    )

    op.create_table(
        'recipe_import_data',
        sa.Column('recipeId', sa.Integer, sa.ForeignKey('recipe.id'), primary_key=True),
        sa.Column('bankImportId', sa.Integer, sa.ForeignKey('bank_import_history.id'), primary_key=True),
        sa.Column('uid', sa.Unicode(255), unique=True),
        sa.Column('importLine', sa.Integer, nullable=False)
    )


def downgrade():
    op.drop_table('recipe_import_data')
    op.drop_table('bank_import_history')
