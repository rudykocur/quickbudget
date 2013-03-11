#!/usr/bin/python

#import httplib2
#import pprint
#
#from apiclient.discovery import build
#from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

CLIENT_ID = raw_input('Enter CLIENT ID: ').strip()
CLIENT_SECRET = raw_input('Enter CLIENT SECRET: ').strip()

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print 'Go to the following link in your browser: \n' + authorize_url
code = raw_input('Enter verification code: ').strip()
credentials = flow.step2_exchange(code)

print 'TOKEN', credentials.access_token


s = Storage('google_api.credentials')
s.put(credentials)
