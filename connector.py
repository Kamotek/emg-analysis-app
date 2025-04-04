import csv
import struct
import time
from pathlib import Path
import yaml

import yaml
from PySide6.QtCore import QObject, Signal

import classifiers_and_tests.classifier_logistic_regression
import classifiers_and_tests.classifier_svm
import classifiers_and_tests.classifier_tree
import classifiers_and_tests.classifier_tree_with_feature_selection
from backend.data_manager import DataManager
from backend.emg_signal import EMGSignal, build_metadata
from band_interface.gforce import DataNotifFlags, GForceProfile, NotifDataType
from cloud_storage.drive_manager import GoogleDriveManager
from visualizers import draw


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

            connector.emg_signal.add_data_row(emg_data)

            connector.emgDataReceived.emit(emg_data)  # Emitting signal for EMG data

        elif data[0] == NotifDataType["NTF_EMG_GEST_DATA"]:
            if len(data) == 2:
                ges = struct.unpack("<B", data[1:])
                print(f"ges_id:{ges[0]}")
            else:
                ges = struct.unpack("<B", data[1:2])[0]
                s = struct.unpack("<H", data[2:4])[0]
                print(f"ges_id:{ges}  strength:{s}")


class Connector(QObject):
    firmwareVersionReceived = Signal(str)
    emgDataReceived = Signal(list)
    quaternionDataReceived = Signal(list)

    def __init__(self):
        super().__init__()
        self.GF = GForceProfile()

        self.experiment_metadata = None

        self.data_manager = DataManager()
        self.emg_signal = None

        self.drive_manager = None  # initialize on demand

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

        data = self.emg_signal.signal
        metadata = self.emg_signal.metadata
        self.data_manager.store_dataset(data, metadata)
        self.emg_signal = None  # Free the memory

    def configure_emg_raw_data(self, sampRate, channelMask, dataLen, resolution, age, gender, height, weight):
        self.experiment_metadata = build_metadata(sampling_rate=sampRate, channel_mask=channelMask, channels=dataLen,
                                                  resolution=resolution, age=age, gender=gender, height=height, weight=weight)

        self.GF.setEmgRawDataConfig(sampRate, channelMask, dataLen, resolution, cb=set_cmd_cb, timeout=1000)

    def start_gesture_notifications(self, gesture_type):
        if gesture_type == 0:
            self.GF.setDataNotifSwitch(DataNotifFlags["DNF_EMG_GESTURE"], set_cmd_cb, 1000)
        else:
            self.GF.setDataNotifSwitch(DataNotifFlags["DNF_EMG_GESTURE_STRENGTH"], set_cmd_cb, 1000)
        self.GF.startDataNotification(lambda data: ondata(data, self))

    def start_emg_notifications(self):
        if self.experiment_metadata is not None:
            # TODO please @Kamil examine if this line below is needed. Especially when executing EMG Start a few times in a row.
            self.GF.setEmgRawDataConfig(self.experiment_metadata['band']['sampling_rate'],
                                        self.experiment_metadata['band']['channel_mask'],
                                        self.experiment_metadata['band']['channels'],
                                        self.experiment_metadata['band']['resolution'],
            # TODO especially because it's already done in configure_emg_raw_data()
                                        cb=set_cmd_cb,
                                        timeout=1000)
            self.GF.setDataNotifSwitch(DataNotifFlags["DNF_EMG_RAW"], set_cmd_cb, 1000)

            self.emg_signal = EMGSignal(metadata=self.experiment_metadata)

            self.GF.startDataNotification(lambda data: ondata(data, self))
        else:
            print("EMG configuration is not set. Call configure_emg_raw_data first.")

    def fetch_data(self):
        # Placeholder for data fetching logic
        # Replace with actual data fetching logic
        return "Data fetched"

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

    def get_gender_from_metadata(self, file):
        """Retrieve the gender from the Metadata.yaml file located in the same directory as the file."""
        metadata_file = file.parent / "metadata.yaml"
        gender = "Unknown"  # Default if metadata or gender is missing
        
        if metadata_file.exists():
            with metadata_file.open() as f:
                metadata = yaml.safe_load(f)
                gender = metadata.get("subject", {}).get("gender", "Unknown").capitalize()

        return gender

    def get_all_csv_files(self):
        base_path = Path("assets/")

        files_and_genders = []
        for file in base_path.rglob("*.gz"):  # More efficient to filter directly in rglob
            gender = self.get_gender_from_metadata(file)
            files_and_genders.append((file, gender))
        return files_and_genders

    def get_local_datasets_IDs(self):
        return self.data_manager.list_datasets()

    def get_local_dataset_description(self, dataset_id):
        metadata = self.data_manager.load_metadata(dataset_id)
        description = f'[{dataset_id}] {metadata}'

        return description

    def ensure_drive_login(self):
        if self.drive_manager is None:
            self.drive_manager = GoogleDriveManager()

    def get_external_datasets_IDs(self):
        return self.drive_manager.list_datasets()

    def get_external_dataset_description(self, dataset_id):
        metadata = 'unknown'
        description = f'[{dataset_id}] {metadata}'

        return description

    def visualize_file(self, file_path):
        try:
            # Assuming draw_chart is defined in visualisations.draw module
            return draw.main(file_path)
        except Exception as e:
            print(f"Error visualizing file {file_path}: {e}")

    def create_next_folder(self, base_path='data'):
        base_path = Path(base_path)
        # Ensure the base path exists
        base_path.mkdir(parents=True, exist_ok=True)

        # Get all subdirectories in the base path
        subdirs = [d for d in base_path.iterdir() if d.is_dir() and d.name.startswith('d') and d.name[1:].isdigit()]

        if not subdirs:
            # If no subdirectories, create d1
            new_folder_name = 'd1'
        else:
            # Get the highest numbered folder
            last_folder = max(subdirs, key=lambda d: int(d.name[1:]))
            last_number = int(last_folder.name[1:])
            new_folder_name = f'd{last_number + 1}'

        new_folder_path = base_path / new_folder_name
        new_folder_path.mkdir()

        return new_folder_path
