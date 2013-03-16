
import os
import json

import Image
import StringIO

from flask import render_template, jsonify, request, redirect, url_for, Response

from quickbudget.schema import Receipt, ReceiptImage
from quickbudget.file import RECEIPT_IMAGE_FOLDER


_routerList = []
def router(rule, **options):
    def decorator(f):
        endpoint = options.pop('endpoint', None)
        
        _routerList.append((rule, endpoint, f, options))
        return f
    
    return decorator


@router('/')
def main():
    receipts = Receipt.allWithoutImage()
    images = ReceiptImage.allWithoutReceipt()

    return render_template('index.html', receipts=receipts, images=images[:15])

@router('/import')
def importer():
    return render_template('importer.html')

@router('/receipt_thumb/<receipt_uid>')
def receipt_thumb(receipt_uid):
    print '!!!!!', receipt_uid

    img = ReceiptImage.get(receipt_uid)
    imgPath = os.path.join(RECEIPT_IMAGE_FOLDER, img.contentPath)

    thumbPath = '%s.thumb' % (imgPath, )

    if not os.path.exists(thumbPath):
        im = Image.open(imgPath)
        im.thumbnail((200, 200), Image.ANTIALIAS)
        im.save(thumbPath, "JPEG")

    return Response(file(thumbPath, 'r'), mimetype="image/jpeg", direct_passthrough=True)


def init_routing(app):
    for rule, endpoint, fun, options in _routerList:
        #print 'Registering', rule#, '::', endpoint, '::', fun, '::', options
        
        app.add_url_rule(rule, endpoint, fun, **options)
    



