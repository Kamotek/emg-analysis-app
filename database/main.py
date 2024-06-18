from database.GoogleDriveManager import GoogleDriveManager


def main():
    drive_manager = GoogleDriveManager()
    drive_manager.upload_file('local_file_example.txt', 'remote_file.txt', drive_manager.app_folder_id)
    drive_manager.download_file(drive_manager.app_folder_id, 'remote_file.txt', 'downloaded_file.txt')


if __name__ == '__main__':
    main()
