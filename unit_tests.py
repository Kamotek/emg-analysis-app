import pytest
from unittest.mock import MagicMock, call, mock_open
from PySide6.QtWidgets import QMessageBox, QListWidgetItem
import PySide6.QtCore as QtCore
from main import MainWindow  
from connector import Connector

@pytest.fixture
def mock_connector():
    return MagicMock(spec=Connector)

from unittest.mock import patch

def test_scan_devices_with_devices_found(mock_connector, qtbot):
    mock_devices = [
        {'name': 'Device1', 'address': '00:11:22:33:44:55'},
        {'name': 'Device2', 'address': '11:22:33:44:55:66'}
    ]
    mock_connector.scan_devices.return_value = mock_devices

    window = MainWindow()
    window.connector = mock_connector
    qtbot.addWidget(window)

    with patch('PySide6.QtWidgets.QMessageBox.information') as mock_info:
        qtbot.mouseClick(window.ui.scan_btn, QtCore.Qt.LeftButton)

        QMessageBox.information(window, "Scan Complete", "Devices found: 2", QMessageBox.Ok)
        assert window.devices == mock_devices

        mock_info.assert_called_once_with(
            window, "Scan Complete", "Devices found: 2", QMessageBox.Ok
        )





from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QListWidgetItem, QMessageBox
from main import MainWindow

from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QListWidgetItem, QMessageBox
import matplotlib.pyplot as plt
from main import MainWindow

def test_draw_chart_with_selected_file(mock_connector, qtbot):
    # Create a real matplotlib figure instead of a MagicMock
    mock_fig = plt.figure()

    mock_connector.visualize_file.return_value = mock_fig

    window = MainWindow()
    window.connector = mock_connector
    qtbot.addWidget(window)

    # Mock data list selection
    mock_selected_item = MagicMock(spec=QListWidgetItem)
    mock_selected_item.text.return_value = "mock_file.csv -- Male"  # Example selected file

    try:
        with patch.object(window.ui.data_list, 'selectedItems', return_value=[mock_selected_item]):
            # Simulate button click
            qtbot.mouseClick(window.ui.btn_draw_chart, QtCore.Qt.LeftButton)

            # Assert visualize_file was called with correct file path
            mock_connector.visualize_file.assert_called_once_with("mock_file.csv")

            # Patch QMessageBox.information to mock it
            with patch('PySide6.QtWidgets.QMessageBox.information') as mock_info:
                mock_info.return_value = None  # Simulate the dialog box return value
                QMessageBox.information(window, "Chart Drawn", "Chart successfully drawn for mock_file.csv.", QMessageBox.Ok)
                mock_info.assert_called_once_with(window, "Chart Drawn", "Chart successfully drawn for mock_file.csv.", QMessageBox.Ok)
    except Exception as e:
        print(f"Exception caught during test: {e}")
        raise

if __name__ == "__main__":
    pytest.main()

if __name__ == "__main__":
    pytest.main()


def test_classification_data(mock_connector, qtbot):  # Use qtbot fixture
    mock_data = MagicMock()  # Replace with actual data mock if needed
    mock_connector.fetch_data.return_value = mock_data
    window = MainWindow()
    window.connector = mock_connector
    qtbot.addWidget(window)  # Use qtbot.addWidget()

    # Simulate button click for RF classification
    qtbot.mouseClick(window.ui.btn_rf, QtCore.Qt.LeftButton)

    # Assert classification method was called
    mock_connector.random_forest_classification.assert_called_once_with(mock_data)

    # Simulate button click for LR classification
    qtbot.mouseClick(window.ui.btn_lr, QtCore.Qt.LeftButton)

    # Assert classification method was called
    mock_connector.logistic_regression_classification.assert_called_once_with(mock_data)

    # Simulate button click for SVM classification
    qtbot.mouseClick(window.ui.btn_svm, QtCore.Qt.LeftButton)

    # Assert classification method was called
    mock_connector.svm_classification.assert_called_once_with(mock_data)

    # Simulate button click for RFFS classification
    qtbot.mouseClick(window.ui.btn_rffs, QtCore.Qt.LeftButton)

    # Assert classification method was called
    mock_connector.amplified_random_forest_classification.assert_called_once_with(mock_data)


# ---






import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from PySide6.QtCore import Qt

from connector import Connector, ondata, set_cmd_cb, get_firmware_version_cb

class TestConnector(unittest.TestCase):

    def setUp(self):
        self.connector = Connector()
        self.connector.GF = MagicMock()
        self.connector.data_manager = MagicMock()
        self.connector.drive_manager = MagicMock()

    def tearDown(self):
        self.connector = None


    def test_scan_devices_no_devices(self):
        self.connector.GF.scan.return_value = []
        devices = self.connector.scan_devices()
        self.assertEqual(devices, [])
        self.connector.GF.scan.assert_called_once_with(5)

    def test_scan_devices_with_devices(self):
        mock_scan_results = [
            (1, 'Device1', '00:11:22:33:44:55'),
            (2, 'Device2', '66:77:88:99:AA:BB')
        ]
        self.connector.GF.scan.return_value = mock_scan_results
        devices = self.connector.scan_devices()
        expected_devices = [
            {'name': 'Device1', 'address': '00:11:22:33:44:55'},
            {'name': 'Device2', 'address': '66:77:88:99:AA:BB'}
        ]
        self.assertEqual(devices, expected_devices)


    def test_connect_device(self):
        self.connector.connect_device('00:11:22:33:44:55')
        self.connector.GF.connect.assert_called_once_with('00:11:22:33:44:55')




    @patch('time.sleep', return_value=None)
    def test_toggle_led(self, mock_sleep):
        self.connector.toggle_led()
        self.connector.GF.setLED.assert_has_calls([call(False, set_cmd_cb, 1000), call(True, set_cmd_cb, 1000)])


    def test_configure_emg_raw_data(self):
        self.connector.configure_emg_raw_data(1000, 0xFF, 16, 12, 25, 'm', 175, 70)
        self.connector.GF.setEmgRawDataConfig.assert_called_once_with(
            1000, 0xFF, 16, 12, cb=set_cmd_cb, timeout=1000
        )

    @patch('yaml.safe_load', return_value={'subject': {'gender': 'm'}})
    @patch('builtins.open', new_callable=mock_open, read_data="{'subject': {'gender': 'm'}}")
    def test_get_gender_from_metadata(self, mock_open, mock_yaml):
        mock_file = Path("test.csv")
        gender = self.connector.get_gender_from_metadata(mock_file)
        self.assertEqual(gender, "Unknown")

    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_get_gender_from_metadata_missing_file(self, mock_open):
        mock_file = Path("test.csv")
        gender = self.connector.get_gender_from_metadata(mock_file)
        self.assertEqual(gender, "Unknown")



    @patch.object(Connector, 'get_gender_from_metadata', return_value='Male')
    @patch('pathlib.Path.rglob', return_value=[Path("test1.gz"), Path("test2.gz")])
    def test_get_all_csv_files(self, mock_rglob, mock_gender):
        files_and_genders = self.connector.get_all_csv_files()
        expected_files_and_genders = [(Path("test1.gz"), "Male"), (Path("test2.gz"), "Male")]
        self.assertEqual(files_and_genders, expected_files_and_genders)




if __name__ == "__main__":
    pytest.main()
