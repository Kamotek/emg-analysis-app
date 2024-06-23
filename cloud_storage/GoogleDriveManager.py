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
        """ Login to Google Drive and save the credentials securely to a file."""
        credentials_path = self.gauth.settings.get('save_credentials_file')

        if os.path.exists(credentials_path):
            self.gauth.LoadCredentialsFile(credentials_path)

        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()

        self.gauth.SaveCredentialsFile(credentials_path)

    def ensure_app_folder(self):
        folder_id = self.get_folder_IDs(self.app_folder_name, 'root')

        if folder_id is None:
            folder_id = self.create_folder(self.app_folder_name, 'root')

        return folder_id

    def get_folder_IDs(self, folder_name, parent_folder_id=None, is_recursive=False):
        """
        Get the folder ID of the folder with the given name.
        :param folder_name:
        :param parent_folder_id: Folder ID being the search starting point. The default is the app folder.
        :param is_recursive: If True, search for the folder in all subfolders.
        :return: Folder ID if found, None otherwise. List of IDs if is_recursive is True.
        :raises: AssertionError if multiple folders with the same name in a single folder are found.
        """
        folder_name = folder_name or self.app_folder_name
        parent_folder_id = parent_folder_id or self.app_folder_id

        query = f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if not is_recursive:
            query += f" and '{parent_folder_id}' in parents"

        file_list = self.drive.ListFile({'q': query}).GetList()

        assert not len(file_list) > 1 and not is_recursive, 'Multiple folders with the same name found'

        if file_list:
            if not is_recursive:
                return file_list[0]['id']

            folder_ids = [file['id'] for file in file_list]
            return folder_ids
        return None

    def create_folder(self, folder_name, parents_folder_id=None):
        """
        Create a folder with the given name.
        :param folder_name:
        :param parents_folder_id: By default, the app folder is the parent.
        :return: New folder's ID.
        """
        parents_folder_id = parents_folder_id or self.app_folder_id

        folder_metadata = {
            'title': folder_name,
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
