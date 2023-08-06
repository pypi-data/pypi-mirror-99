import pandas as pd
from datetime import datetime, timedelta, date
import time
import random
import copy
import numpy as np
import string

print("Input Discipline Required")
discipline = str(input())
discipline = discipline.upper()

print("Input Number of Surgeries to Generate")
n = int(input()) # Number of surgeries to list

duration_min = 1  # hour
duration_max = 5  # hour

list_of_possible_durations = list(np.arange(start=duration_min, stop=duration_max+0.25, step=0.25))
procedure_codes = ['S' + random.choice(string.ascii_uppercase) + str(random.randint(100, 999)) for _ in range(100)] # just a random set of procedure codes
actual_predicted = [1, 0]  # will just randomly pick from here

final_df = np.array(['0', '0', '0', '0'])

for _ in range(n):
	picked_duration = random.choice(list_of_possible_durations)
	picked_procedure = random.choice(procedure_codes)
	request = random.choice(actual_predicted)
	row_ = np.array([discipline, picked_duration, picked_procedure, request])
	final_df = np.vstack((final_df, row_))

final_df = np.delete(final_df, 0, axis=0)
df_pandas = pd.DataFrame(final_df, columns=['Discipline', 'Duration', 'Procedure', 'Actual Request'])
df_pandas.to_csv('ToSchedule_' + str(discipline) + '_' + str(n) + '.csv', index=False)
