
import os
import json


from flask import render_template, jsonify, request, redirect, url_for


_routerList = []
def router(rule, **options):
    def decorator(f):
        endpoint = options.pop('endpoint', None)
        
        _routerList.append((rule, endpoint, f, options))
        return f
    
    return decorator


@router('/')
def main():
    return render_template('index.html')

@router('/import')
def importer():

    return render_template('importer.html')



def init_routing(app):
    for rule, endpoint, fun, options in _routerList:
        #print 'Registering', rule#, '::', endpoint, '::', fun, '::', options
        
        app.add_url_rule(rule, endpoint, fun, **options)
    



