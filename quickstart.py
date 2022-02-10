from __future__ import print_function
import os
import httplib2
from googleapiclient.http import MediaFileUpload
from oauth2client.file import Storage
from oauth2client import tools, client
from apiclient import discovery
from googleapiclient.errors import HttpError
import argparse


def save_files(service, file_metadata, file_name):
    media = MediaFileUpload(
        file_name,
        mimetype='text/csv'
    )
    try:
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
    except HttpError:
        print('Arquivo Corrompido')
        pass


def get_credentials():
    credential_path = os.path.join('my_secrets/drive.json')
    print(credential_path)
    store = Storage(credential_path)
    credentials = store.get()
    try:

        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    # Se modificar esses escopos, exclua suas credenciais salvas anteriormente
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = 'my_secrets/client.json'
    APPLICATION_NAME = 'Drive API Python Quickstart'

    if not credentials or credentials.invalid:

        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)

        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        # Necessário apenas para compatibilidade com Python 2.6
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    print("Credentials Successfully")
    return credentials


def upload(file_name, dir_name="", folder_id=""):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    if dir_name != "":
        folder_metadata = {
            'name': dir_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': ['1pJsqI16zD3HF6Ja1x20QUcgut4bDPU0I']
        }
        folder_id = service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()
        file_metadata = {
            'name': file_name,
            'parents': [folder_id['id']]
        }
    else:
        file_metadata = {
            'name': file_name,
            'parents': folder_id
        }
    save_files(service, file_metadata, file_name)
