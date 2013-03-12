__author__ = 'ivan'

import sys
import re
import os
import datetime
import decimal
import shutil

from quickbudget import db
from quickbudget import csv_util

from quickbudget.schema import BankImportHistory


def importPekaoCreditCard(filename, db):
    storagePath = os.path.join('quickbudget', 'data', 'import')
    if not os.path.exists(storagePath):
        os.makedirs(storagePath)

    #targetFile = BankImportHistory(targetPath, 'pekao_cc')

    with open(filename, 'r') as f:
        #reader = csv.reader(f, delimiter='\t')
        reader = csv_util.UnicodeReader(f, encoding='cp1250', delimiter='\t')

        for rowNum, row in enumerate(reader):
            if not row:
                continue

            transDate, _, operType, _, _, _, amount, _, description, refNum, _, cardNumber = row

            try:
                transDate = datetime.datetime.strptime(transDate, '%Y-%m-%d').date()
            except ValueError:
                # any row which does not contain parsable transaction date is invalid for us
                print 'SKIPPED ROW', rowNum, 'from import'
                continue

            amount = decimal.Decimal(amount.replace(',', '.'))
            description = re.sub(r'(\s+)', ' ', description).strip()

            print '%s) trans=%r, type=%s, amount=%s, descr=%r, ref=%s, card=%s' % (rowNum, transDate, operType, amount, description, refNum, cardNumber)
            print

    print 'Import of file', filename, 'done - moving to local files'


if __name__ == '__main__':
    db.init_db()
    importPekaoCreditCard(sys.argv[1], db.db_session)
