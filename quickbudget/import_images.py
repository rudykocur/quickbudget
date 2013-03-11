
import os
import zlib
import hashlib
import pprint

from sqlalchemy.orm.exc import NoResultFound

from quickbudget import db
from quickbudget import gdrive
from quickbudget.db import db_session
from quickbudget.schema import RecipeImage


def crcContent(data):
    prev = 0
    prev = zlib.crc32(data, prev)
    return u"%X" % (prev & 0xFFFFFFFF)

def importAll(srv, folderId):
    storagePath = os.path.join('quickbudget', 'data', 'receipt')
    if not os.path.exists(storagePath):
        os.makedirs(storagePath)

    q = "'%s' in parents" % (folderId,)

    allRecipeImages = gdrive.retrieve_all_files(srv, q)

    for img in allRecipeImages:
        print 'OMG', img['title'], '::', img['id']  # , '::', img['embedLink']


        try:
            savedImage = RecipeImage.query.filter(RecipeImage.uid == img['id']).one()
            print 'FILE ID', img['id'], 'already known', savedImage.crc, '::', savedImage.md5
        except NoResultFound:
            content = gdrive.download_file(srv, img['downloadUrl'])
            md5 = unicode(hashlib.md5(content).hexdigest())
            crc = crcContent(content)

            try:
                savedDuplicate = RecipeImage.query.filter(RecipeImage.crc == crc and RecipeImage.md5 == md5).one()
                print 'PROPABLY A DUPLICATE', img['id'], ':: Other one:', savedDuplicate.uid
            except NoResultFound:

                filename = '%s-%s' % (img['id'], img['title'])
                fullPath = os.path.join(storagePath, filename)

                with open(fullPath, 'w') as f:
                    f.write(content)

                print 'NEW FILE', img['id'], 'at', fullPath
                image = RecipeImage(img['id'], filename)
                image.crc = crc
                image.md5 = md5

                db_session.add(image)
                db_session.commit()

        print
        print



if __name__ == '__main__':
    db.init_db()

    importAll(gdrive.drive_service, '0B_V-GNTsCHGERm9VNzc4YmRyQTA')

    db_session.commit()

