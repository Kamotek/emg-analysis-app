import sys
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QListWidgetItem, QDialog
from band_interface.ui_main import Ui_MainWindow  # Make sure the path to the Ui_MainWindow is correct
from connector import Connector
from band_interface.emg_config_dialog import EMGConfigDialog
from band_interface.ui_functions import UIFunctions

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connector = Connector()

        # Connect UI buttons to methods (unchanged from your original code)
        self.ui.Btn_Toggle.clicked.connect(lambda: self.toggle_menu())
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
        self.ui.btn_page_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))

        self.ui.scan_btn.clicked.connect(self.scan_devices)
        self.ui.emg_btn.clicked.connect(self.configure_emg)
        self.ui.connect_btn.clicked.connect(self.connect_device)
        self.ui.firmware_btn.clicked.connect(self.get_firmware_version)
        self.ui.led_btn.clicked.connect(self.toggle_led)
        self.ui.motor_btn.clicked.connect(self.toggle_motor)
        self.ui.quaternion_btn.clicked.connect(self.start_quaternion_notifications)
        self.ui.stop_quat_btn.clicked.connect(self.stop_notifications)
        self.ui.raw_emg_button.clicked.connect(self.start_emg_notifications)
        self.ui.stop_emg_button.clicked.connect(self.stop_notifications)
        self.ui.gesture_btn.clicked.connect(lambda: self.start_gesture_notifications(0))
        self.ui.stop_gesture_btn.clicked.connect(self.stop_notifications)

        self.ui.btn_rf.clicked.connect(lambda: self.classify_data('rf'))
        self.ui.btn_lr.clicked.connect(lambda: self.classify_data('lr'))
        self.ui.btn_svm.clicked.connect(lambda: self.classify_data('svm'))
        self.ui.btn_rffs.clicked.connect(lambda: self.classify_data('rffs'))

        self.connector.firmwareVersionReceived.connect(self.on_firmware_version_received)
        self.connector.emgDataReceived.connect(self.on_emg_data_received)
        self.connector.quaternionDataReceived.connect(self.on_quaternion_data_received)

        self.ui.btn_refresh.clicked.connect(self.load_files)
        self.ui.btn_draw_chart.clicked.connect(self.draw_chart)

        self.devices = []  # List to store scanned devices
        self.show()

    def toggle_menu(self):
        UIFunctions.toggle_menu(self, 220, True)  # 220 is the maximum width of the menu

    def scan_devices(self):
        self.devices = self.connector.scan_devices()
        if not self.devices:
            QMessageBox.information(self, "Scan Devices", "No devices found.")
            return

        self.ui.config_list.clear()  # Clear the list before adding new items
        for device in self.devices:
            item = QListWidgetItem(f"{device['name']} ({device['address']})")
            item.setData(1, device['address'])  # Store the address in the item for later use
            self.ui.config_list.addItem(item)

    def connect_device(self):
        selected_items = self.ui.config_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Connect Device", "No device selected.")
            return

        selected_item = selected_items[0]  # Get the first selected item
        device_address = selected_item.data(1)  # Get the stored address
        self.connector.connect_device(device_address)
        QMessageBox.information(self, "Connect Device", f"Connected to {device_address}")

    def get_firmware_version(self):
        self.connector.get_firmware_version()

    def toggle_led(self):
        self.connector.toggle_led()

    def toggle_motor(self):
        self.connector.toggle_motor()

    def start_quaternion_notifications(self):
        self.connector.start_quaternion_notifications()

    def configure_emg(self):
        dialog = EMGConfigDialog(self)
        if dialog.exec() == QDialog.Accepted:
            config = dialog.get_values()
            print("EMG Configuration:", config)
            self.connector.configure_emg_raw_data(
                sampRate=config['sample_rate'],
                channelMask=config['channel_mask'],
                dataLen=config['data_length'],
                resolution=config['resolution']
            )

    def start_gesture_notifications(self, gesture_type):
        self.connector.start_gesture_notifications(gesture_type)

    def stop_notifications(self):
        self.connector.stop_notifications()

    def start_emg_notifications(self):
        self.connector.start_emg_notifications()

    def on_firmware_version_received(self, firmware_version):
        item = QListWidgetItem(f"Firmware Version: {firmware_version}")
        self.ui.data_read.addItem(item)

    def on_quaternion_data_received(self, quaternion_data):
        item = QListWidgetItem(f"Quaternion Data: {quaternion_data}")
        self.ui.data_read.addItem(item)

    def on_emg_data_received(self, emg_data):
        item = QListWidgetItem(f"EMG Data: {emg_data}")
        self.ui.data_read.addItem(item)

    def load_files(self):
        csv_files = self.connector.get_all_csv_files()
        self.ui.data_list.clear()  # Clear the list before adding new items
        for file_path in csv_files:
            item = QListWidgetItem(str(file_path))
            self.ui.data_list.addItem(item)

    def draw_chart(self):
        selected_items = self.ui.data_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Draw Chart", "No file selected.")
            return

        selected_file = selected_items[0].text()
        self.connector.visualize_file(selected_file)

    def classify_data(self, method):
        data = self.connector.fetch_data()
        result = None

        if method == 'rf':
            result = self.connector.random_forest_classification(data)
        elif method == 'lr':
            result = self.connector.logistic_regression_classification(data)
        elif method == 'svm':
            result = self.connector.svm_classification(data)
        elif method == 'rffs':
            result = self.connector.amplified_random_forest_classification(data)

        self.ui.classification_results.clear()

        # Split the result string by lines and add each line separately
        for line in result.split('\n'):
            list_item = QListWidgetItem(line)
            self.ui.classification_results.addItem(list_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
