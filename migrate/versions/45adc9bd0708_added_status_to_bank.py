"""Added status to BankImportHistory

Revision ID: 45adc9bd0708
Revises: 4cdb9d6dabae
Create Date: 2013-03-16 11:01:39.457998

"""

# revision identifiers, used by Alembic.
revision = '45adc9bd0708'
down_revision = '4cdb9d6dabae'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bank_import_history', sa.Column('status', sa.Unicode(50)))


def downgrade():
    op.drop_column('bank_import_history', 'status')
