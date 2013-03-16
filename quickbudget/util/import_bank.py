__author__ = 'ivan'

import sys
import re
import os
import datetime
import decimal
import shutil
import hashlib

from sqlalchemy.orm.exc import NoResultFound

from quickbudget import db
from quickbudget import csv_util
from quickbudget.enums import IMPORTTYPE, IMPORTSTATUS
from quickbudget.file import identifyFile, archiveBankImport, BANK_IMPORT_FOLDER

from quickbudget.schema import BankImportHistory, Recipe, RecipeImportData


def importPekaoCreditCard(filepath, session):

    md5, crc = identifyFile(filepath)

    try:
        bankImport = BankImportHistory.findByHash(md5, crc)
        print 'FOUND EXISTING IMPORT', bankImport.id
    except NoResultFound:
        print 'CREATING NEW BANK IMPORT'
        bankImport = BankImportHistory(IMPORTTYPE.pekao_cc)
        bankImport.md5 = md5
        bankImport.crc = crc
        session.add(bankImport)
        session.commit()

        storedPath = archiveBankImport(filepath, bankImport)
        bankImport.contentPath = os.path.basename(storedPath)
        session.commit()

    importLocation = os.path.join(BANK_IMPORT_FOLDER, bankImport.contentPath)
    print 'IMPORTING FROM', importLocation

    with open(importLocation, 'r') as f:
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

            print '%s) trans=%r, type=%s, amount=%s, descr=%r, ref=%s, card=%s' % (rowNum, transDate, operType,
                amount, description, refNum, cardNumber)

            if refNum == '':
                print 'SKIPPED ROW', rowNum, '- unknown refNum'
                print
                continue

            try:
                RecipeImportData.get(refNum)
                print 'SKIPPED ROW', rowNum, '- imported already'
            except NoResultFound:
                recipe = Recipe()
                recipe.total = amount
                recipe.date = transDate
                recipe.note = description

                recipeImport = RecipeImportData(recipe, bankImport, refNum, rowNum)

                session.add(recipe)
                session.add(recipeImport)
                session.commit()

            print

    bankImport.status = IMPORTSTATUS.completed
    session.commit()
    print 'Import of file', importLocation, 'done'


if __name__ == '__main__':
    db.init_db()
    importPekaoCreditCard(sys.argv[1], db.db_session)
