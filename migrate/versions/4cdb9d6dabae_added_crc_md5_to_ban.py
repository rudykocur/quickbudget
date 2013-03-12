"""Added crc, md5 to BankImportHistory

Revision ID: 4cdb9d6dabae
Revises: 9cffcf88f2e
Create Date: 2013-03-12 21:08:45.629232

"""

# revision identifiers, used by Alembic.
revision = '4cdb9d6dabae'
down_revision = '9cffcf88f2e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bank_import_history', sa.Column('crc', sa.Unicode(20)))
    op.add_column('bank_import_history', sa.Column('md5', sa.Unicode(32)))


def downgrade():
    op.drop_column('bank_import_history', 'crc')
    op.drop_column('bank_import_history', 'md5')
