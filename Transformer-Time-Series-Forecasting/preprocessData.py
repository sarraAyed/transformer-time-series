import csv
from typing import Dict, List
from datetime import datetime, timezone
import math


def fill_csv_file(signal_number, file_to_write: str, files_raw: List[Dict]):
    header = ['sensor_id','timestamp','humidity','reindexed_id','sin_hour','cos_hour','sin_day','cos_day','sin_month','cos_month']
    # header = ["patient_number", "timestamp", "signal_value", "reindexed_id",
    #           "sin_microsecond", "cos_microsecond", "sin_second", "cos_second", "sin_minute", "cos_minute"]
    with open(file_to_write, "w+", newline="") as txt:
        writer = csv.writer(txt)
        writer.writerow(header)

        for index, file in enumerate(files_raw):
            signals = extract_signals_info(signal_number, file["file_path"])
            for signal_value in signals:

                # print("signal_value: ", signal_value, type(signal_value[0]))

                # date_time = datetime.strptime(signal_value[0], '%Y-%m-%d %H:%M:%S.%f+00:00')
                #
                # micro_second = date_time.microsecond
                # seconds = date_time.second
                # minutes = date_time.minute

                # print("date_time: ", date_time)
                #
                # print(type(date_time.microsecond))
                # hours = "{}".format(date_time.hour)
                # minutes = "{}".format(date_time.minute)
                #
                # micro_second = date_time.microsecond
                micro_second = signal_value[0] * pow(10,3)
                seconds = signal_value[0]
                minutes = signal_value[0] / 60
                row = [file["id_patient"], signal_value[0], signal_value[1], index+1,
                       math.sin(micro_second), math.cos(micro_second), math.sin(seconds),
                       math.cos(seconds), math.sin(minutes), math.cos(minutes)]
                writer.writerow(row)

def get_validate_csv(signal_number):
    sick_patient_file = {
        "file_to_write": "Data/validate_dataset.csv",
        "files_raw": [{
            "id_patient": "4",
            "file_path": "Data/original-data/GaPt03_01.txt"
        }]
    }
    fill_csv_file(signal_number, sick_patient_file["file_to_write"], sick_patient_file["files_raw"])


def get_train_csv_file(signal_number):
    train_data = {
        "file_to_write" : "Data/train_dataset.csv",
        "files_raw": [{
            "id_patient": "1",
            "file_path": "Data/original-data/GaCo01_01.txt"
        }, {
            "id_patient": "2",
            "file_path": "Data/original-data/GaCo02_01.txt"
        }]
    }

    test_data = {
        "file_to_write": "Data/test_dataset.csv",
        "files_raw": [{
            "id_patient": "3",
            "file_path": "Data/original-data/GaCo02_02.txt"
        }]
    }

    fill_csv_file(signal_number, train_data["file_to_write"], train_data["files_raw"])
    fill_csv_file(signal_number, test_data["file_to_write"], test_data["files_raw"])


def convert_from_s(seconds: int):
    result = datetime.fromtimestamp(seconds, timezone.utc).isoformat(' ', 'microseconds')
    return result



def extract_signals_info(signal_number: int, file_to_read: str):
    # filesHealthyPatients = ["Data/original-data/GaCo01_01.txt"]
    # train_data = ("Data/train_dataset.csv",  ["Data/original-data/GaCo01_01.txt", "Data/original-data/GaCo02_01.txt"])
    # test_data = ("Data/test_dataset.csv", ["Data/original-data/GaCo02_02.txt"])

    all_signal: list() = []
    with open(file_to_read, "r") as txt:
        lines = txt.readlines()

    for line in lines:
        signal_t = line.rstrip().split('\t')
        for index, signal_i in enumerate(signal_t):
            if index == signal_number:
                # time = convert_from_s(float(signal_t[0]))
                # time = strftime("%H:%M:%S", gmtime(float(signal_t[0])))
                time = float(signal_t[0])
                value = float(signal_i)
                all_signal.append((time, value))
    return all_signal


def main(signal_number: int):
    get_train_csv_file(signal_number)
    get_validate_csv(signal_number)


if __name__ == "__main__":
    main(signal_number=1)