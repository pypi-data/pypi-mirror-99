import os
import csv
from tkinter import *
from tkinter import filedialog
from datetime import *

def read_toschedule():

    # this is a window prompt for selecting csv file to be read
    dialog_root = Tk()
    dialog_root.geometry("1200x700+350+150")
    dialog_root.withdraw()

    # this will obtain file path of the selected csv file
    file_path = filedialog.askopenfilename(title='Please select the to be scheduled .csv file')
    file_path = os.path.normpath(file_path)

    # discipline dictionary to identify code
    discipline_codes = {10: 'BREAST',
                        11: 'OTO',
                        12: 'NES',
                        13: 'CLR',
                        14: 'HPB',
                        15: 'PLS',
                        16: 'ENT',
                        17: 'SUR-ONCO',
                        18: 'UGI',
                        19: 'H&N',
                        20: 'O&G',
                        21: 'HND',
                        22: 'OMS',
                        23: 'VAS',
                        24: 'CTS',
                        25: 'URO'
                        }

    # create empty initial procedures list
    procedure_code_list = []
    # create empty initial procedures dictionary
    new_proc_codes = {}

    # initial loop through csv to find unique procedure codes/names
    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv:  # add each array
            if row[2] not in procedure_code_list:
                procedure_code_list.append(row[2])

    # create a dictionary with the unique procedure code list
    for i in range(len(procedure_code_list)):
        new_proc_codes[int(10+i)] = procedure_code_list[i]

    key_list = list(discipline_codes.keys())
    value_list = list(discipline_codes.values())
    proc_key_list = list(new_proc_codes.keys())
    proc_value_list = list(new_proc_codes.values())

    procedure_list = []
    to_schedule = []

    # final output list
    output_list = []

    # find number of surgeries in the to_schedule csv file
    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv: # add each array
            duration = int(float(row[1]) / 0.25)
            duplicate_count = procedure_list.count(row[2])
            procedure_list.append(row[2])
            position = value_list.index(row[0])
            proc_position = proc_value_list.index(row[2])
            if int(row[3]) == 1:
                temp_list = [1100000 + (key_list[position])*1000 + (proc_key_list[proc_position])*10 + duplicate_count] * duration
                to_schedule.append(temp_list)
            elif int(row[3]) == 0:
                temp_list = [1200000 + (key_list[position])*1000 + (proc_key_list[proc_position])*10 + duplicate_count] * duration
                to_schedule.append(temp_list)

    # append to_schedule and new_proc_codes to final output list
    output_list.append(to_schedule)
    output_list.append(new_proc_codes)

    # return to_schedule
    return output_list


def read_toschedule1(file_path):

    # this is a window prompt for selecting csv file to be read
    dialog_root = Tk()
    dialog_root.geometry("1200x700+350+150")
    dialog_root.withdraw()

    # discipline dictionary to identify code
    discipline_codes = {10: 'BREAST',
                        11: 'OTO',
                        12: 'NES',
                        13: 'CLR',
                        14: 'HPB',
                        15: 'PLS',
                        16: 'ENT',
                        17: 'SUR-ONCO',
                        18: 'UGI',
                        19: 'H&N',
                        20: 'O&G',
                        21: 'HND',
                        22: 'OMS',
                        23: 'VAS',
                        24: 'CTS',
                        25: 'URO'
                        }

    # create empty initial procedures list
    procedure_code_list = []
    # create empty initial procedures dictionary
    new_proc_codes = {}

    # initial loop through csv to find unique procedure codes/names
    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv:  # add each array
            if row[2] not in procedure_code_list:
                procedure_code_list.append(row[2])

    # create a dictionary with the unique procedure code list
    for i in range(len(procedure_code_list)):
        new_proc_codes[int(10 + i)] = procedure_code_list[i]

    key_list = list(discipline_codes.keys())
    value_list = list(discipline_codes.values())
    proc_key_list = list(new_proc_codes.keys())
    proc_value_list = list(new_proc_codes.values())

    procedure_list = []
    to_schedule = []

    # final output list
    output_list = []

    # find number of surgeries in the to_schedule csv file
    with open(file_path, 'r', newline='') as csv_file:
        mock_csv = csv.reader(csv_file, delimiter=',')
        next(mock_csv, None)  # skip header
        for row in mock_csv:  # add each array
            duration = int(float(row[1]) / 0.25)
            duplicate_count = procedure_list.count(row[2])
            procedure_list.append(row[2])
            position = value_list.index(row[0])
            proc_position = proc_value_list.index(row[2])
            if int(row[3]) == 1:
                temp_list = [1100000 + (key_list[position]) * 1000 + (
                proc_key_list[proc_position]) * 10 + duplicate_count] * duration
                to_schedule.append(temp_list)
            elif int(row[3]) == 0:
                temp_list = [1200000 + (key_list[position]) * 1000 + (
                proc_key_list[proc_position]) * 10 + duplicate_count] * duration
                to_schedule.append(temp_list)

    # append to_schedule and new_proc_codes to final output list
    output_list.append(to_schedule)
    output_list.append(new_proc_codes)

    return output_list