import pandas as pd
from datetime import datetime, timedelta, date
import time
import random
import copy
import numpy as np


def get_slots_per_day(days, perc):
	slot_in_a_day = 23*44
	day_vec = np.arange(start=1, stop=days+1)
	goal = perc * days

	# binary search solver
	right = 999999
	left = -999999
	while True:
		mid = (right+left)/2
		c = np.power(mid, day_vec)
		c = np.sum(c)
		if abs(goal - c)<0.00001:
			break
		elif c > goal:
			right = mid
		elif c < goal:
			left = mid

	x = np.log(mid)
	day_vec = np.multiply(day_vec, x)
	day_vec = np.exp(day_vec)
	day_vec = np.multiply(day_vec, slot_in_a_day)

	return np.round(day_vec)


def random_sum_to(n):  # returns a tuple of 2 list
	sum_n = 0
	m = 44 * 23 - n
	random_list_n = []
	random_list_m = []
	while sum_n + 44 < n:
		a = round(random.uniform(4, 20))
		sum_n += a
		random_list_n.append(a)

	random_list_n.append(n - sum_n)

	sum_m = 0
	while sum_m + 8 < m:
		a = random.randint(4, 28)
		sum_m += a
		random_list_m.append(a)
	random_list_m.append(m - sum_m)
	return (random_list_n, random_list_m)


def fill_surg_or_breaks(lensurg, lenbreaks):
	# print(lensurg)
	# print(lenbreaks)
	prob_surg = lensurg/ (lensurg + lenbreaks)
	if random.uniform(0,1) < prob_surg:
		return 0
	else:
		return 1


list_of_disc = ['BREAST','OTO', 'NES', 'CLR', 'HPB', 'PLS','ENT','SUR-ONCO','UGI','H&N','O&G','HND','VAS','CTS','URO']
ot_list = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'M1', 'M2', 'M3', 'M4', 'M5', 'OT 24','OT 25', 'OT 22', 'R1', 'R4', 'R5', 'R6', 'R7', 'R8', 'MRI']
random_surgeon_id = ['DR' + str(random.randint(10000, 99999)) for _ in range(50)]
priority = ['Elective', 'Semi-Elective']
print("Input number of weeks for planning horizon")
ph = int(input())

print("Input percentage full in which current schedule are (0-100)")
perc_filled_ = int(input())

today_string = datetime.today().strftime("%d/%m/%Y")
list_of_days = []

for _ in range(ph*5):
	list_of_days.append(today_string)
	now = datetime.strptime(today_string, "%d/%m/%Y")
	today_string = now + timedelta(days=1)
	if today_string.weekday() == 5:
		today_string = today_string + timedelta(days=2)
	elif today_string.weekday() == 6:
		today_string = today_string + timedelta(days=1)
	today_string = datetime.strftime(today_string, "%d/%m/%Y")

print(list_of_days)
# how much to fill for each day?
to_fill = get_slots_per_day(ph*5, perc_filled_/100)
final_df = np.array(['0','0','0','0', '0', '0','0'])
print(list_of_days)
for index, date in enumerate(list_of_days):
	number_to_fill = to_fill[index]

	tup = list(random_sum_to(number_to_fill))
	mock_sche_dur, mock_sche_resttime = tup[0], tup[1]
	flag = 0
	for ot_room in ot_list:
		dur_for_ot = 0
		disc_random = random.choice(list_of_disc)
		date_time_variable_right = date + " 08:00"
		session_end = date_time_variable_right

		while True:
			if len(tup[0]) == 0 and len(tup[1]) == 0:
				flag = 1
				break
			choice_surg_ot = fill_surg_or_breaks(len(tup[0]), len(tup[1]))
			dur_ = tup[choice_surg_ot].pop(0)  # pop away the chosen one
			if dur_for_ot + dur_ > 36:
				break
			date_time_variable_left = datetime.strptime(session_end, "%d/%m/%Y %H:%M")
			date_time_variable_right = date_time_variable_left + timedelta(minutes=(dur_ * 15))
			session_start = datetime.strftime(date_time_variable_left, "%d/%m/%Y %H:%M")
			session_end = datetime.strftime(date_time_variable_right, "%d/%m/%Y %H:%M")
			if choice_surg_ot == 0:
				row_ = np.array(['1', session_start, session_end, random.choice(random_surgeon_id), disc_random, ot_room, random.choice(priority)])
				final_df = np.vstack((final_df, row_))
			dur_for_ot += dur_

		if flag == 1:
			print(str(date) + " completed")
			break

final_df = np.delete(final_df, 0, axis=0)
df_pandas = pd.DataFrame(final_df, columns=['Session No', 'Session Start Date/Time', 'Session End Date/Time', 'Surgeon ID', 'Department,OT', 'Code', 'Priority of Operation'])
df_pandas.to_csv('generated_schedule_' + str(ph) +'weeks_' + str(perc_filled_) + '%.csv', index=False)


