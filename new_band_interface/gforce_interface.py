# gforce_interface.py
# !/usr/bin/python
# -*- coding:utf-8 -*-

import struct
import time
import csv
from gforce import DataNotifFlags, GForceProfile, NotifDataType

# Open CSV files for logging data
quat_file = open("quaternion_data.csv", "w", newline='')
quat_writer = csv.writer(quat_file)
emg_file = open("emg_raw_data.csv", "w", newline='')
emg_writer = csv.writer(emg_file)
gest_file = open("gesture_data.csv", "w", newline='')
gest_writer = csv.writer(gest_file)

packet_cnt = 0
start_time = 0

def set_cmd_cb(resp):
    print("Command result: {}".format(resp))

def get_firmware_version_cb(resp, firmware_version):
    print("Command result: {}".format(resp))
    print("Firmware version: {}".format(firmware_version))

def ondata(data):
    global packet_cnt, start_time

    if len(data) > 0:
        if data[0] == NotifDataType["NTF_QUAT_FLOAT_DATA"] and len(data) == 17:
            quat_iter = struct.iter_unpack("f", data[1:])
            quaternion = [i[0] for i in quat_iter]
            print("quaternion:", quaternion)
            quat_writer.writerow(quaternion)

        elif data[0] == NotifDataType["NTF_EMG_ADC_DATA"] and len(data) == 129:
            if start_time == 0:
                start_time = time.time()

            packet_cnt += 1

            if packet_cnt % 100 == 0:
                period = time.time() - start_time
                sample_rate = 100 * 16 / period  # 16 means repeat times in one packet
                byte_rate = 100 * len(data) / period
                print("----- sample_rate:{0}, byte_rate:{1}".format(sample_rate, byte_rate))
                start_time = time.time()

            emg_data = list(data[1:129])
            emg_writer.writerow(emg_data)

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

class GForceHandler:
    def __init__(self):
        self.GF = GForceProfile()

    def scan_devices(self):
        print("Scanning devices...")
        scan_results = self.GF.scan(5)
        return scan_results

    def connect(self, addr):
        self.GF.connect(addr)
        print(f"Connected to {addr}")

    def get_firmware_version(self):
        self.GF.getControllerFirmwareVersion(get_firmware_version_cb, 1000)

    def toggle_led(self):
        self.GF.setLED(False, set_cmd_cb, 1000)
        time.sleep(1)
        self.GF.setLED(True, set_cmd_cb, 1000)

    def toggle_motor(self):
        self.GF.setMotor(True, set_cmd_cb, 1000)
        time.sleep(1)
        self.GF.setMotor(False, set_cmd_cb, 1000)

    def get_quaternion(self):
        self.GF.setDataNotifSwitch(DataNotifFlags["DNF_QUATERNION"], set_cmd_cb, 1000)
        time.sleep(1)
        self.GF.startDataNotification(ondata)

    def stop_quaternion(self):
        self.GF.stopDataNotification()
        time.sleep(1)
        self.GF.setDataNotifSwitch(DataNotifFlags["DNF_OFF"], set_cmd_cb, 1000)

    def set_emg_config(self, sampRate, channelMask, dataLen, resolution):
        self.GF.setEmgRawDataConfig(
            sampRate, channelMask, dataLen, resolution, cb=set_cmd_cb, timeout=1000
        )

    def get_emg_data(self):
        self.GF.setDataNotifSwitch(DataNotifFlags["DNF_EMG_RAW"], set_cmd_cb, 1000)
        time.sleep(1)
        self.GF.startDataNotification(ondata)

    def stop_emg_data(self):
        self.GF.stopDataNotification()
        time.sleep(1)
        self.GF.setDataNotifSwitch(DataNotifFlags["DNF_OFF"], set_cmd_cb, 1000)

    def get_gesture_id(self, flag):
        if flag == 0:
            self.GF.setDataNotifSwitch(DataNotifFlags["DNF_EMG_GESTURE"], set_cmd_cb, 1000)
        else:
            self.GF.setDataNotifSwitch(DataNotifFlags["DNF_EMG_GESTURE_STRENGTH"], set_cmd_cb, 1000)
        time.sleep(1)
        self.GF.startDataNotification(ondata)

    def stop_gesture_id(self):
        self.GF.stopDataNotification()
        time.sleep(1)
        self.GF.setDataNotifSwitch(DataNotifFlags["DNF_OFF"], set_cmd_cb, 1000)
