import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriveManager:
    def __init__(self, settings_file='drive_settings.yaml', app_folder_name='EMG Analysis Data'):
        self.settings_file = settings_file
        self.app_folder_name = app_folder_name

        self.gauth = GoogleAuth(settings_file=self.settings_file)
        self.authenticate_persistently()
        self.drive = GoogleDrive(self.gauth)

        self.app_folder_id = self.ensure_app_folder()

    def authenticate_persistently(self):
        credentials_file = self.gauth.settings.get('save_credentials_file')
        assert credentials_file, 'Credentials file path not set in the settings file'

        if os.path.exists(credentials_file):
            self.gauth.LoadCredentialsFile(credentials_file)

        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()

        self.gauth.SaveCredentialsFile(credentials_file)

    def ensure_app_folder(self):
        folder_id = self.get_folder_id()

        if folder_id is None:
            folder_id = self.create_folder()

        return folder_id

    def get_folder_id(self, folder_path=None, parent_folder_id='root'):  # TODO nested folders
        if not folder_path:
            folder_path = self.app_folder_name

        query = f"title='{self.app_folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        file_list = self.drive.ListFile({'q': query}).GetList()
        assert not len(file_list) > 1, 'Multiple folders with the same name found'

        if file_list:
            folder_id = file_list[0]['id']
            return folder_id
        return None

    def create_folder(self, parents_folder_id='root'):
        folder_metadata = {
            'title': self.app_folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [{'id': parents_folder_id}]
        }
        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder['id']

    def upload_file(self, local_path, remote_filename, remote_folder_id):
        file = self._get_file(remote_filename, remote_folder_id)
        if file:
            file.Delete()

        file = self.drive.CreateFile({
            'title': remote_filename,
            'parents': [{'id': remote_folder_id}]
        })
        file.SetContentFile(local_path)
        file.Upload()

    def _get_file(self, remote_filename, remote_folder_id):
        query = f"'{remote_folder_id}' in parents and title='{remote_filename}' and trashed=false"
        file_list = self.drive.ListFile({'q': query}).GetList()
        assert not len(file_list) > 1, 'Multiple files with the same name found'

        if file_list:
            file = file_list[0]
            return file
        return None

    def download_file(self, folder_id, drive_filename, local_path):
        file = self._get_file(drive_filename, folder_id)
        assert file, f'File {drive_filename} not found in folder'

        file.GetContentFile(local_path)
