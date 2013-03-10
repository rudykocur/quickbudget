
import zlib

from quickbudget import db
from quickbudget import gdrive


from quickbudget.db import db_session


from quickbudget.schema import RecipeImage


def crc(data):
    prev = 0
    prev = zlib.crc32(data, prev)
    return "%X"%(prev & 0xFFFFFFFF)

def importAll(srv, folderId):
    a = RecipeImage.query.all()
    print a

    q = "'%s' in parents" % (folderId,)

    allRecipeImages = gdrive.retrieve_all_files(srv, q)

    for img in allRecipeImages:
        print 'OMG', img['title'], '::', img['id']  # , '::', img['embedLink']

        #c = download_file(drive_service, f['downloadUrl'])

        #print 'CONTENT LENGTH', len(c), '::', crc(c)


if __name__ == '__main__':
    db.init_db()

    importAll(gdrive.drive_service, '0B_V-GNTsCHGERm9VNzc4YmRyQTA')

    db_session.commit()

