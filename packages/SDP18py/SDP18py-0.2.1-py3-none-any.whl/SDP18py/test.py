

# python3 setup.py sdist bdist_wheel
# twine upload --repository-url http://upload.pypi.org/legacy/ dist/*

from SDP18py.view_timetable1 import show_timetable
from SDP18py.read_MAS import read_mas
from SDP18py.read_csv import read_csv
from SDP18py.read_toschedule import read_toschedule
from SDP18py.test_hco import run_hco
from SDP18py.test_ts import run_ts
from SDP18py.test_sa import run_sa
from SDP18py.test_ga import run_ga

# s = read_csv()
# current_schedule = s
#
# show_timetable(current_schedule)


# to_schedule = read_toschedule()
# MAS_full = read_mas()
import numpy as np
import numpy_indexed as npi
from operator import itemgetter
# c = np.array([np.nan]*3)
import pareto as pt
import pandas as pd
# p = [[1, 2, 3, np.array([1,2,4])], [1, 3, 3, np.array([1,2,3])]]
# x = np.array([1.13, 2.133 ,3.1313])
# p = pd.DataFrame([[1,2,3], [4,5,6]])
#
# print(np.power(0.9, x))
# print(q)
# max_overtime, max_idletime, max_waittime = q.max(axis = 0)
# print(max_overtime, max_idletime, max_waittime)
     #[('b','e'), 3, 4,4], [['c',23],2,1,4], [('d','s'),21,1,3], [[22132,'asd'],2,5,1]]
#df = pd.DataFrame(p)
#print(df.iloc[:, 0:3])

#print(df)
#p = [[(23, 21), 1, 3], [(15, 16), 2, 5], [(9, 2), 2, 1]]
#, ['f', 4, 5, 7]]
# c = pt.eps_sort(p, objectives=[0,1,2])
# print(c)
#
# #get = np.array([1, 2, 5], dtype=float)
# #print(itemgetter(*get)(p))
# #print(q.tolist())
# #ort itertools
# # a = np.array(list(itertools.permutations([1, 2, 3])))
# # b = np.array(list(itertools.permutations([2, 4, 6])))
# # print(np.concatenate((a,b), axis=0))
#
# # from SDP18py.MO_fitting_func_calc import calculate_delta_S
# #
# # t = 500
# #
# # z = calculate_delta_S(c, p, t)
# # print(z)
#
#
# p = np.arange(start=1, stop=5+1) # 20 days
# print(p)
# q = np.power(5,p)
# print(q)
# percentage = 0.25 * 20 # 25%
# qq = np.sum(q)
# r = percentage / qq
# print(r)
# z = r*q
# print(z)
# print(np.average(z))

# from sympy import Eq, Symbol, solve
#
# y = Symbol('y')
# eqn = Eq(y + y**2 + y**3, 8.0)
#
# print(solve(eqn))
# from pygmo import hypervolume
#
# max_overtime_hco, max_idletime_hco, max_waitingtime_hco = hco_front.max(axis=0)
# max_overtime_sa, max_idletime_sa, max_waitingtime_sa = sa_front.max(axis=0)
# max_overtime_ts, max_idletime_ts, max_waitingtime_ts = ts_front.max(axis=0)
# max_overtime_ga, max_idletime_ga, max_waitingtime_ga = ga_front.max(axis=0)
#
# arr_ = np.array([[max_overtime_hco, max_idletime_hco, max_waitingtime_hco],
#                 [max_overtime_sa, max_idletime_sa, max_waitingtime_sa],
#                 [max_overtime_ts, max_idletime_ts, max_waitingtime_ts],
#                 [max_overtime_ga, max_idletime_ga, max_waitingtime_ga]], dtype=float)
#
# max_overtime, max_idletime, max_waitingtime = arr_.max(axis=0)
#
# ref_point = [max_overtime,max_idletime,max_waitingtime]
#
# hv_hco = hypervolume(hco_front)
# print("Hill Climbing Hypervolume:")
# print(hv_hco.compute(ref_point))
#
# hv_sa = hypervolume(sa_front)
# print("Simulated Annealing Hypervolume:")
# print(hv_sa.compute(ref_point))
#
# hv_ts = hypervolume(ts_front)
# print("Tabu Search Hypervolume:")
# print(hv_ts.compute(ref_point))
#
# hv_ga = hypervolume(ga_front)
# print("Genetic Algorithm Hypervolume:")
# print(hv_ga.compute(ref_point))