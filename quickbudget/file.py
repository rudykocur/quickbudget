__author__ = 'ivan'

import os
import zlib
import hashlib
import shutil

BANK_IMPORT_FOLDER = os.path.join('quickbudget', 'data', 'import')

def crcContent(data):
    prev = 0
    prev = zlib.crc32(data, prev)
    return u"%X" % (prev & 0xFFFFFFFF)


def identifyFile(fullPath):
    with open(fullPath, 'r') as f:
        content = f.read()
        md5 = unicode(hashlib.md5(content).hexdigest())
        crc = crcContent(content)

    return (md5, crc)


def archiveBankImport(fullPath, bankImportObj):
    if not os.path.exists(BANK_IMPORT_FOLDER):
        os.makedirs(BANK_IMPORT_FOLDER)

    filename = os.path.basename(fullPath)
    targetImportFile = 'data-%s-%s' % (bankImportObj.id, filename)

    destPath = os.path.join(BANK_IMPORT_FOLDER, targetImportFile)

    shutil.copy(fullPath, destPath)

    return destPath
