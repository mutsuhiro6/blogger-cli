import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import build_http
from oauth2client import client
from oauth2client import file
from oauth2client import tools


def blogger_service():
    CLIENT_SECRET_FILENAME = 'client_secret.json'
    CLIENT_SECRET_FILE = os.path.join(
        os.path.dirname(__file__), CLIENT_SECRET_FILENAME)
    SCOPE = 'https://www.googleapis.com/auth/blogger'  # Scope for Blogger R/W.
    flow = client.flow_from_clientsecrets(
        filename=CLIENT_SECRET_FILE,
        scope=SCOPE,
        message=tools.message_if_missing(CLIENT_SECRET_FILE)
    )
    credentials_data_path = os.path.join(
        os.path.dirname(__file__),
        'credentials',
        'blogger.dat')
    storage = file.Storage(credentials_data_path)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage)
    http = credentials.authorize(http=build_http())
    blogger = build('blogger', 'v3', http=http)
    return blogger
