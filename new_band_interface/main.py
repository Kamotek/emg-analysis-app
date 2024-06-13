# main.py
# !/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QListWidget, QLabel, QLineEdit, QInputDialog, QMessageBox)
from PyQt5.QtCore import Qt
from gforce_interface import GForceHandler

class GForceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.handler = GForceHandler()

    def initUI(self):
        self.setGeometry(100, 100, 400, 600)
        self.setWindowTitle('GForce Controller')

        self.layout = QVBoxLayout()

        self.scan_btn = QPushButton('Scan Devices', self)
        self.scan_btn.clicked.connect(self.scan_devices)
        self.layout.addWidget(self.scan_btn)

        self.device_list = QListWidget(self)
        self.layout.addWidget(self.device_list)

        self.connect_btn = QPushButton('Connect to Device', self)
        self.connect_btn.clicked.connect(self.connect_device)
        self.layout.addWidget(self.connect_btn)

        self.firmware_btn = QPushButton('Get Firmware Version', self)
        self.firmware_btn.clicked.connect(self.get_firmware_version)
        self.layout.addWidget(self.firmware_btn)

        self.led_btn = QPushButton('Toggle LED', self)
        self.led_btn.clicked.connect(self.toggle_led)
        self.layout.addWidget(self.led_btn)

        self.motor_btn = QPushButton('Toggle Motor', self)
        self.motor_btn.clicked.connect(self.toggle_motor)
        self.layout.addWidget(self.motor_btn)

        self.quaternion_btn = QPushButton('Get Quaternion', self)
        self.quaternion_btn.clicked.connect(self.get_quaternion)
        self.layout.addWidget(self.quaternion_btn)

        self.stop_quat_btn = QPushButton('Stop Quaternion', self)
        self.stop_quat_btn.clicked.connect(self.stop_quaternion)
        self.layout.addWidget(self.stop_quat_btn)

        self.emg_btn = QPushButton('Set EMG Config', self)
        self.emg_btn.clicked.connect(self.set_emg_config)
        self.layout.addWidget(self.emg_btn)

        self.raw_emg_btn = QPushButton('Get Raw EMG Data', self)
        self.raw_emg_btn.clicked.connect(self.get_emg_data)
        self.layout.addWidget(self.raw_emg_btn)

        self.stop_emg_btn = QPushButton('Stop EMG Data', self)
        self.stop_emg_btn.clicked.connect(self.stop_emg_data)
        self.layout.addWidget(self.stop_emg_btn)

        self.gesture_btn = QPushButton('Get Gesture ID', self)
        self.gesture_btn.clicked.connect(self.get_gesture_id)
        self.layout.addWidget(self.gesture_btn)

        self.stop_gesture_btn = QPushButton('Stop Gesture ID', self)
        self.stop_gesture_btn.clicked.connect(self.stop_gesture_id)
        self.layout.addWidget(self.stop_gesture_btn)

        self.setLayout(self.layout)

    def scan_devices(self):
        self.device_list.clear()
        devices = self.handler.scan_devices()
        if not devices:
            QMessageBox.information(self, "Info", "No devices found.")
        for idx, device in enumerate(devices):
            device_info = f"{idx}: {device[1]} {device[2]} Rssi={device[3]} Connectable={device[4]}"
            self.device_list.addItem(device_info)

    def connect_device(self):
        selected_device = self.device_list.currentRow()
        if selected_device == -1:
            QMessageBox.warning(self, "Warning", "No device selected.")
            return
        addr = self.device_list.item(selected_device).text().split()[2]
        self.handler.connect(addr)

    def get_firmware_version(self):
        self.handler.get_firmware_version()

    def toggle_led(self):
        self.handler.toggle_led()

    def toggle_motor(self):
        self.handler.toggle_motor()

    def get_quaternion(self):
        self.handler.get_quaternion()

    def stop_quaternion(self):
        self.handler.stop_quaternion()

    def set_emg_config(self):
        sampRate, ok1 = QInputDialog.getInt(self, "EMG Config", "Sample Rate (max 500):", 500, 1, 500, 1)
        if not ok1:
            return
        channelMask, ok2 = QInputDialog.getInt(self, "EMG Config", "Channel Mask (e.g., 0xFF):", 0xFF, 0, 255, 1)
        if not ok2:
            return
        dataLen, ok3 = QInputDialog.getInt(self, "EMG Config", "Data Length (e.g., 128):", 128, 1, 1024, 1)
        if not ok3:
            return
        resolution, ok4 = QInputDialog.getInt(self, "EMG Config", "Resolution (8 or 12):", 8, 8, 12, 4)
        if not ok4:
            return
        self.handler.set_emg_config(sampRate, channelMask, dataLen, resolution)

    def get_emg_data(self):
        self.handler.get_emg_data()

    def stop_emg_data(self):
        self.handler.stop_emg_data()

    def get_gesture_id(self):
        flag, ok = QInputDialog.getInt(self, "Gesture ID", "0: ID only, 1: ID and strength:", 0, 0, 1, 1)
        if ok:
            self.handler.get_gesture_id(flag)

    def stop_gesture_id(self):
        self.handler.stop_gesture_id()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = GForceApp()
    mainWin.show()
    sys.exit(app.exec_())
