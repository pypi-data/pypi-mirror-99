import pandas as pd
from datetime import datetime, timedelta, date
import time
import random
import copy
import numpy as np

list_of_disc = ['BREAST','OTO', 'NES', 'CLR', 'HPB', 'PLS','ENT','SUR-ONCO','UGI','H&N','O&G','HND','VAS','CTS','URO']
ot_list = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'M1', 'M2', 'M3', 'M4', 'M5', 'OT 24','OT 25', 'OT 22', 'R1', 'R4', 'R5', 'R6', 'R7', 'R8', 'MRI']
template1 = [["1", '08:00', '12:00', "DR12345",'disc', 'ot',"Elective"],
             ["1", '12:15', '17:00', "DR14242",'disc', 'ot',"Semi-Elective"]]
template2 = [["1", '08:15', '13:15', "DR12345",'disc', 'ot',"Semi-Elective"],
             ["1", '15:45', '18:00', "DR33434",'disc', 'ot',"Semi-Elective"]]
template3 = [["1", '08:00', '11:45', "DR12345",'disc', 'ot',"Semi-Elective"],
             ["1", '12:00', '14:30', "DR31412",'disc', 'ot',"Semi-Elective"]]
template4 = [["1", '09:00', '12:00', "DR12412",'disc', 'ot',"Semi-Elective"],
             ["1", '12:15', '13:45', "DR14242",'disc', 'ot',"Elective"],
             ["1", '14:00', '17:45', "DR12351",'disc', 'ot',"Elective"]]
template5 = [["1", '08:00', '13:15', "DR12412",'disc', 'ot',"Semi-Elective"],
             ["1", '15:15', '17:30', "DR12351",'disc', 'ot',"Elective"]]
template6 = [["1", '10:15', '17:30', "DR12324",'disc', 'ot',"Semi-Elective"]]
template7 = [["1", '08:00', '12:15', "DR11242",'disc', 'ot',"Semi-Elective"],
             ["1", '13:00', '17:30', "DR12512",'disc', 'ot',"Elective"]]
template8 = [["1", '08:30', '11:00', "DR12414",'disc', 'ot',"Semi-Elective"],
             ["1", '11:00', '14:30', "DR21412",'disc', 'ot',"Elective"],
             ["1", '14:45', '17:00', "DR11242",'disc', 'ot',"Elective"]]
template9 = [["1", '08:00', '13:45', "DR12412",'disc', 'ot',"Semi-Elective"],
             ["1", '14:15', '17:00', "DR13532",'disc', 'ot',"Semi-Elective"]]
template10 = [["1", '08:45', '11:15', "DR12412",'disc', 'ot',"Semi-Elective"],
             ["1", '11:30', '14:45', "DR12351",'disc', 'ot',"Elective"],
             ["1", '14:45', '16:45', "DR13532",'disc', 'ot',"Semi-Elective"]]
template11 = [["1", '08:00', '10:00', "DR14224",'disc', 'ot',"Semi-Elective"],
             ["1", '10:00', '12:00', "DR11242",'disc', 'ot',"Elective"],
             ["1", '12:15', '15:00', "DR12442",'disc', 'ot',"Elective"]]
template12 = [["1", '08:15', '14:30', "DR14221",'disc', 'ot',"Semi-Elective"],
             ["1", '15:00', '17:15', "DR12424",'disc', 'ot',"Elective"]]
template13 = [["1", '08:30', '17:00', "DR24242",'disc', 'ot',"Semi-Elective"]]
template14 = [["1", '08:00', '12:30', "DR12252",'disc', 'ot',"Semi-Elective"],
             ["1", '12:45', '15:00', "DR12124",'disc', 'ot',"Elective"],
             ["1", '15:15', '17:15', "DR13524",'disc', 'ot',"Semi-Elective"]]
template15 = [["1", '08:00', '10:00', "DR12252",'disc', 'ot',"Semi-Elective"],
             ["1", '10:30', '12:15', "DR142124",'disc', 'ot',"Elective"],
             ["1", '12:30', '16:45', "DR12124",'disc', 'ot',"Elective"]]

templates = [template1, template2, template3, template4, template5, template6, template7, template8, template9, template10, template11, template12, template13, template14, template15]

print("Input number of weeks for planning horizon")
ph = int(input())

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

df = []
day = 1
for date_ in list_of_days:
    for ot_ in ot_list:
        template_random = random.choice(templates)
        temp = copy.deepcopy(template_random)
        disc_random = random.choice(list_of_disc)
        for slot in temp:
            start_time = slot[1]
            end_time = slot[2]
            slot[0] = day
            slot[1] = str(date_) + ' ' + str(start_time)
            slot[2] = str(date_) + ' ' + str(end_time)
            slot[4] = disc_random
            slot[5] = ot_

            df.append(slot)

    day += 1
print("Input percentage full in which current schedule are (0-100)")
perc_filled_ = int(input())
perc_filled = perc_filled_/100

number_rows = len(df)
number_to_delete = round((1-perc_filled) * number_rows) # i just used the number of surgeries, by right should consider duration
no_days = np.arange(day)
perc_per_day = no_days/np.sum(no_days)
number_to_delete_per_day = np.round(perc_per_day * number_to_delete)
final_df = np.array(['0','0','0','0', '0', '0','0'])

for index, day_ in enumerate(range(1, day)):
    temp_list = [row for row in df if row[0] == day_]
    len_list = len(temp_list)
    del_list = []
    for _ in range(int(number_to_delete_per_day[index])):
        del_list.append(random.randint(0,len_list))
    temp_list_np = np.array(temp_list)
    temp = np.delete(temp_list_np, del_list, axis=0)
    final_df = np.vstack((final_df, temp))

final_df = np.delete(final_df, 0, axis=0)
df_pandas = pd.DataFrame(final_df, columns=['Sessioart Date/Time', 'Session End Date Time', 'Surgeon ID', 'Department,OT', 'Code', 'Priority of Operation'])
df_pandas.to_csv('generated_schedule_' + str(ph) +'weeks_' + str(perc_filled_) + '%.csv', index=False)





