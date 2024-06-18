import sys

from PyQt6.QtWidgets import QApplication

from database.GoogleDriveManager import GoogleDriveManager
from database.MockUI import MockUI


def main():
    app = QApplication(sys.argv)
    window = MockUI()

    drive_manager = GoogleDriveManager()
    drive_manager.upload_file('local_file_example.txt', 'remote_file.txt', drive_manager.folder_id)
    drive_manager.download_file(drive_manager.folder_id, 'remote_file.txt', 'downloaded_file.txt')

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
