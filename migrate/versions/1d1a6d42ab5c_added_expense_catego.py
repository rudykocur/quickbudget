"""Added expense category

Revision ID: 1d1a6d42ab5c
Revises: 45adc9bd0708
Create Date: 2013-03-16 12:03:30.783852

"""

# revision identifiers, used by Alembic.
revision = '1d1a6d42ab5c'
down_revision = '45adc9bd0708'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'expense_category',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.Unicode(255), nullable=False, unique=True),
    )

    fk = sa.ForeignKey('expense_category.id', name='expense_category')
    op.add_column('recipe', sa.Column('expenseCategoryId', sa.Integer, fk, nullable=True))


def downgrade():
    op.drop_constraint('expense_category', 'recipe', 'foreignkey')
    op.drop_column('recipe', 'expenseCategoryId')

    op.drop_table('expense_category')
