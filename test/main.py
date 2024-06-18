# main.py

import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication
from test.ui_main import Ui_MainWindow

# Import Connector class
from test.connector import Connector
from test.ui_functions import UIFunctions

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize Connector
        self.connector = Connector()

        # Connect UI buttons to methods
        self.ui.Btn_Toggle.clicked.connect(lambda: self.toggle_menu())
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1))
        self.ui.btn_page_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.btn_page_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))

        # Add event handlers for page 1 buttons
        self.ui.scan_btn.clicked.connect(self.scan_devices)
        self.ui.connect_btn.clicked.connect(self.connect_device)
        self.ui.firmware_btn.clicked.connect(self.get_firmware_version)
        self.ui.led_btn.clicked.connect(self.toggle_led)
        self.ui.motor_btn.clicked.connect(self.toggle_motor)
        self.ui.quaternion_btn.clicked.connect(self.start_quaternion_notifications)
        self.ui.stop_quat_btn.clicked.connect(self.stop_notifications)
        self.ui.raw_emg_button.clicked.connect(self.configure_emg)
        self.ui.stop_emg_button.clicked.connect(self.stop_notifications)
        self.ui.gesture_btn.clicked.connect(lambda: self.start_gesture_notifications(0))
        self.ui.stop_gesture_btn.clicked.connect(self.stop_notifications)

        self.show()

    def toggle_menu(self):
        UIFunctions.toggle_menu(self, 220, True)  # 220 is the maximum width of the menu

        pass

    def scan_devices(self):
        devices = self.connector.scan_devices()
        for device in devices:
            print(device)

    def connect_device(self):
        # For simplicity, we take the first device found.
        devices = self.connector.scan_devices()
        if devices:
            self.connector.connect_device(devices[0][2])

    def get_firmware_version(self):
        self.connector.get_firmware_version()

    def toggle_led(self):
        self.connector.toggle_led()

    def toggle_motor(self):
        self.connector.toggle_motor()

    def start_quaternion_notifications(self):
        self.connector.start_quaternion_notifications()

    def configure_emg(self):
        # Example configuration, these can be taken from user input
        sampRate = 500
        channelMask = 0xFF
        dataLen = 128
        resolution = 8
        self.connector.configure_emg_raw_data(sampRate, channelMask, dataLen, resolution)

    def start_gesture_notifications(self, gesture_type):
        self.connector.start_gesture_notifications(gesture_type)

    def stop_notifications(self):
        self.connector.stop_notifications()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
