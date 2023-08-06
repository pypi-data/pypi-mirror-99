from SDP18py.UMOSA import run_umosa
from SDP18py.MOSHCR import run_moshcr
from SDP18py.TAMOCO import run_tamoco
from SDP18py.NSGAII import run_nsga2
from SDP18py.plot_pareto_front import plot_front_multiple
import csv
from pathlib import Path
import numpy as np
import os
import csv
from tkinter import *
from tkinter import filedialog
from datetime import *
from SDP18py.read_csv import read_csv1
from SDP18py.read_MAS import read_mas1
from SDP18py.read_toschedule import read_toschedule1
import copy

directory = Path(r"C:\Users\Jordon Leow\Desktop\Y4S1\SDP\NewProject\SDP18py")
# change these file names when running different % full and number to schedule
current_schedule_list = read_csv1(directory/"generated_schedule_4weeks_50%.csv")
mas_read = read_mas1(directory/"mock_MAS.csv")
to_schedule_read = read_toschedule1(directory/"ToSchedule_OTO_25.csv")
disc_select = 'OTO'

time_limit = 180  # seconds, change to whatever time required

current_schedule_list1 = copy.deepcopy(current_schedule_list)
current_schedule_list2 = copy.deepcopy(current_schedule_list)
current_schedule_list3 = copy.deepcopy(current_schedule_list)
current_schedule_list4 = copy.deepcopy(current_schedule_list)


#hco_front = np.array(run_moshcr(current_schedule_list1, to_schedule_read, mas_read, disc_select, time_limit))
#sa_front = np.array(run_umosa(current_schedule_list3, to_schedule_read, mas_read, disc_select, time_limit))
ts_front = np.array(run_tamoco(current_schedule_list2, to_schedule_read, mas_read, disc_select, time_limit))
#ga_front = np.array(run_nsga2(current_schedule_list4, to_schedule_read, mas_read, disc_select, time_limit))

# print("HCO")
# print(hco_front)
# print("SA")
# print(sa_front)
# print("TS")
# print(ts_front)
# print("GA")
# print(ga_front)

# plot_front_multiple(hco_front, sa_front, ts_front, ga_front)

