
import os
import json
import glob

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

@router('/receipt_thumb/<receipt_uid>/<size>')
def receipt_thumb(receipt_uid, size):
    img = ReceiptImage.get(receipt_uid)
    imgPath = os.path.join(RECEIPT_IMAGE_FOLDER, img.contentPath)

    if size != 'thumb':
        return Response(file(imgPath, 'r'), direct_passthrough=True)

    thumbSize = 100

    thumbPath = '%s.%s-thumb' % (imgPath, thumbSize)

    if not os.path.exists(thumbPath):
        im = Image.open(imgPath)
        im.thumbnail((thumbSize, thumbSize), Image.ANTIALIAS)
        im.save(thumbPath, "JPEG")

    r = Response(file(thumbPath, 'r'), mimetype="image/jpeg", direct_passthrough=True)
    #r.cache_control.max_age = 60*60*24
    #import datetime
    #r.expires = datetime.datetime(2014,1,1)
    return r

@router('/receipt_rotate/<receipt_uid>/<direction>')
def receipt_rotate(receipt_uid, direction):
    img = ReceiptImage.get(receipt_uid)
    imgPath = os.path.join(RECEIPT_IMAGE_FOLDER, img.contentPath)

    angle = -90 if direction == 'right' else 90

    #rotated = None
    with open(imgPath, 'r') as f:
        im = Image.open(f)
        rotated = im.rotate(angle)

    for x in glob.glob('%s.*' % (imgPath, )):
        os.unlink(x)

    rotated.save(imgPath)

    return ''



def init_routing(app):
    for rule, endpoint, fun, options in _routerList:
        #print 'Registering', rule#, '::', endpoint, '::', fun, '::', options
        
        app.add_url_rule(rule, endpoint, fun, **options)
    



