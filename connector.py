import os
from PySide6.QtCore import QObject, Signal
import classifiers_and_tests.classifier_svm
import classifiers_and_tests.classifier_logistic_regression
import classifiers_and_tests.classifier_tree_with_feature_selection
import classifiers_and_tests.classifier_tree
import visualizers.draw
from visualizers import draw
from test.gforce import DataNotifFlags, GForceProfile, NotifDataType
import struct
import csv
import time
from pathlib import Path

# Global file handlers and CSV writers for data logging
quat_file = open("quaternion_data.csv", "w", newline='')
quat_writer = csv.writer(quat_file)

emg_file = open("emg_raw_data.csv", "w", newline='')
emg_writer = csv.writer(emg_file)

gest_file = open("gesture_data.csv", "w", newline='')
gest_writer = csv.writer(gest_file)

# Callback functions
def set_cmd_cb(resp):
    print(f"Command result: {resp}")

def get_firmware_version_cb(resp, firmware_version):
    print(f"Command result: {resp}")
    print(f"Firmware version: {firmware_version}")

# Packet counter and start time for EMG data
packet_cnt = 0
start_time = 0

# Data handling function
def ondata(data, connector):
    global packet_cnt, start_time

    if len(data) > 0:
        if data[0] == NotifDataType["NTF_QUAT_FLOAT_DATA"] and len(data) == 17:
            quat_iter = struct.iter_unpack("f", data[1:])
            quaternion = [i[0] for i in quat_iter]
            print("quaternion:", quaternion)
            quat_writer.writerow(quaternion)
            connector.quaternionDataReceived.emit(quaternion)  # Emitting signal for quaternion data

        elif data[0] == NotifDataType["NTF_EMG_ADC_DATA"] and len(data) == 129:
            if start_time == 0:
                start_time = time.time()

            packet_cnt += 1

            if packet_cnt % 100 == 0:
                period = time.time() - start_time
                sample_rate = 100 * 16 / period  # 16 means repeat times in one packet
                byte_rate = 100 * len(data) / period
                print(f"----- sample_rate:{sample_rate}, byte_rate:{byte_rate}")
                start_time = time.time()

            emg_data = list(data[1:129])
            emg_writer.writerow(emg_data)
            connector.emgDataReceived.emit(emg_data)  # Emitting signal for EMG data

        elif data[0] == NotifDataType["NTF_EMG_GEST_DATA"]:
            if len(data) == 2:
                ges = struct.unpack("<B", data[1:])
                print(f"ges_id:{ges[0]}")
                gest_writer.writerow([ges[0]])
            else:
                ges = struct.unpack("<B", data[1:2])[0]
                s = struct.unpack("<H", data[2:4])[0]
                print(f"ges_id:{ges}  strength:{s}")
                gest_writer.writerow([ges, s])

class Connector(QObject):
    firmwareVersionReceived = Signal(str)
    emgDataReceived = Signal(list)
    quaternionDataReceived = Signal(list)

    def __init__(self):
        super().__init__()
        self.GF = GForceProfile()
        self.sampRate = None
        self.channelMask = None
        self.dataLen = None
        self.resolution = None

    def scan_devices(self):
        print("Scanning devices...")
        scan_results = self.GF.scan(5)
        if not scan_results:
            print("No devices found.")
            return []

        # Assuming scan_results is a list of tuples or lists with [idx, name, address]
        devices = []
        for device in scan_results:
            devices.append({
                'name': device[1],  # Assuming device[1] is the name
                'address': device[2]  # Assuming device[2] is the address
            })
        return devices

    def connect_device(self, addr):
        self.GF.connect(addr)
        print(f"Connected to {addr}")

    def get_firmware_version(self):
        def get_firmware_version_cb(resp, firmware_version):
            self.firmwareVersionReceived.emit(firmware_version)

        self.GF.getControllerFirmwareVersion(get_firmware_version_cb, 1000)

    def toggle_led(self):
        self.GF.setLED(False, set_cmd_cb, 1000)
        time.sleep(1)
        self.GF.setLED(True, set_cmd_cb, 1000)

    def toggle_motor(self):
        self.GF.setMotor(True, set_cmd_cb, 1000)
        time.sleep(3)
        self.GF.setMotor(False, set_cmd_cb, 1000)

    def start_quaternion_notifications(self):
        self.GF.setDataNotifSwitch(DataNotifFlags["DNF_QUATERNION"], set_cmd_cb, 1000)
        self.GF.startDataNotification(lambda data: ondata(data, self))

    def stop_notifications(self):
        self.GF.stopDataNotification()
        self.GF.setDataNotifSwitch(DataNotifFlags["DNF_OFF"], set_cmd_cb, 1000)

    def configure_emg_raw_data(self, sampRate, channelMask, dataLen, resolution):
        self.sampRate = sampRate
        self.channelMask = channelMask
        self.dataLen = dataLen
        self.resolution = resolution
        
        self.GF.setEmgRawDataConfig(sampRate, channelMask, dataLen, resolution, cb=set_cmd_cb, timeout=1000)


    def start_gesture_notifications(self, gesture_type):
        if gesture_type == 0:
            self.GF.setDataNotifSwitch(DataNotifFlags["DNF_EMG_GESTURE"], set_cmd_cb, 1000)
        else:
            self.GF.setDataNotifSwitch(DataNotifFlags["DNF_EMG_GESTURE_STRENGTH"], set_cmd_cb, 1000)
        self.GF.startDataNotification(lambda data: ondata(data, self))

    def start_emg_notifications(self):
        if self.sampRate is not None and self.channelMask is not None and self.dataLen is not None and self.resolution is not None:
            self.GF.setEmgRawDataConfig(self.sampRate, self.channelMask, self.dataLen, self.resolution, cb=set_cmd_cb, timeout=1000)
            self.GF.setDataNotifSwitch(DataNotifFlags["DNF_EMG_RAW"], set_cmd_cb, 1000)
            self.GF.startDataNotification(lambda data: ondata(data, self))
        else:
            print("EMG configuration is not set. Call configure_emg_raw_data first.")

    def get_raw_emg(self):
        if self.sampRate is not None and self.channelMask is not None and self.dataLen is not None and self.resolution is not None:
            self.GF.setEmgRawDataConfig(self.sampRate, self.channelMask, self.dataLen, self.resolution, cb=set_cmd_cb, timeout=1000)
            self.GF.setDataNotifSwitch(DataNotifFlags["DNF_EMG_RAW"], set_cmd_cb, 1000)
            self.GF.startDataNotification(lambda data: ondata(data, self))
        else:
            print("EMG configuration is not set. Call configure_emg_raw_data first.")


    def random_forest_classification(self, data):
        # Placeholder for classification logic
        # Replace with actual RandomForest classification logic
        return classifiers_and_tests.classifier_tree.main()
    def logistic_regression_classification(self, data):
        # Placeholder for classification logic
        # Replace with actual Logistic Regression classification logic
        return classifiers_and_tests.classifier_logistic_regression.main()

    def svm_classification(self, data):
        # Placeholder for classification logic
        # Replace with actual SVM classification logic
        return classifiers_and_tests.classifier_svm.main()

    def amplified_random_forest_classification(self, data):
        # Placeholder for classification logic
        # Replace with actual Amplified Random Forest classification logic
        return classifiers_and_tests.classifier_tree_with_feature_selection.main()
    
    base_path = Path("preprocessed_data/")
    def get_all_csv_files(self):
        csv_files = []
        for file in self.base_path.rglob("*"):
            if file.suffix == ".csv":
                csv_files.append(file)
        return csv_files
    
    def visualize_file(self, file_path):
        try:
            # Assuming draw_chart is defined in visualisations.draw module
            draw.main(file_path)
        except Exception as e:
            print(f"Error visualizing file {file_path}: {e}")

    # Other methods of the Connector cl