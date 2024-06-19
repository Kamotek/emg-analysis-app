import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QListWidgetItem, QDialog
from PySide6.QtCore import QObject, Signal
from ui_main import Ui_MainWindow
from connector import Connector
from emg_config_dialog import EMGConfigDialog
from ui_functions import UIFunctions


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connector = Connector()

        # Connect UI buttons to methods
        self.ui.Btn_Toggle.clicked.connect(lambda: self.toggle_menu())
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))

        # Add event handlers for page 1 buttons
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

        # Connect signals from Connector class
        self.connector.firmwareVersionReceived.connect(self.on_firmware_version_received)
        self.connector.emgDataReceived.connect(self.on_emg_data_received)
        self.connector.quaternionDataReceived.connect(self.on_quaternion_data_received)


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
