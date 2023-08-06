import numpy as np
import pandas as pd
from SDP18py.Generate_initial_solution import initial_solution_random_fit
from SDP18py.MO_fitting_func_calc import MO_calculate
from SDP18py.MO_fitting_func_calc import calc_crowding_distance
from SDP18py import find_legal_neighbors as fd, swapper as sp
import pareto as pt
from SDP18py.plot_pareto_front import plot_front_only
import time
# from view_timetable1 import show_timetable
from SDP18py.view_timetable1 import show_timetable_1
from SDP18py.view_timetable1 import show_timetable
from threading import Thread
import random
import copy

def run_moshcr(current_schedule_list, to_schedule_read, mas_read, disc_select, tl):

    OT_indexes = {0: 'L1',
                  1: 'L2',
                  2: 'L3',
                  3: 'L4',
                  4: 'L5',
                  5: 'L6',
                  6: 'L7',
                  7: 'L8',
                  8: 'M1',
                  9: 'M2',
                  10: 'M3',
                  11: 'M4',
                  12: 'M5',
                  13: 'OT 24',
                  14: 'OT 25',
                  15: 'OT 22',
                  16: 'R1',
                  17: 'R4',
                  18: 'R5',
                  19: 'R6',
                  20: 'R7',
                  21: 'R8',
                  22: 'MRI',
                  }

    current_schedule = current_schedule_list
    # add one more schedule_date
    schedule_date = current_schedule[2]
    # code on top ^
    schedule_days = current_schedule[1]
    day_index = current_schedule[3]
    current_schedule = current_schedule[0]
    # to_schedule = to_schedule_read
    to_schedule = to_schedule_read[0]
    to_schedule_dict = to_schedule_read[1]

    MAS_full = mas_read
    MAS_allowed = MAS_full[disc_select]

    t0 = time.time()

    # first fit or random fit
    schedule_copy = copy.deepcopy(current_schedule)
    soln = initial_solution_random_fit(schedule_copy, to_schedule, MAS_allowed, day_index, OT_indexes)

    # HILL CLIMBING ALGORITHM
    print("Hill Climbing Algorithm")

    iter_per_restart = 200  # will restart every max_iter of iterations
    pareto_efficient_set_scores_and_solution = [[9999, 9999, 9999, soln]]
    time_limit = tl  # seconds
    k = 1
    while time.time() - t0 < time_limit:
        print("Restart" + str(k))
        schedule_copy = copy.deepcopy(current_schedule)
        soln = initial_solution_random_fit(schedule_copy, to_schedule, MAS_allowed, day_index, OT_indexes)
        for _ in range(iter_per_restart):
            sp.pushback2(soln)
            past_pareto_scores_and_soln = copy.deepcopy(pareto_efficient_set_scores_and_solution)
            # print(past_pareto_scores)
            curr_score = MO_calculate(soln)
            legal_swaps = fd.all_legal_swaps(soln, to_schedule, MAS_allowed, day_index, OT_indexes)
            neighbour = random.choice(legal_swaps)  # stochastic hill climbing
            perturb_soln = sp.swapping(soln, neighbour)
            perturb_score = MO_calculate(perturb_soln)
            perturb_score_and_soln = perturb_score.tolist() + [perturb_soln]
            pareto_efficient_set_scores_and_solution.append(perturb_score_and_soln)
            pareto_efficient_set_scores_and_solution = pt.eps_sort(pareto_efficient_set_scores_and_solution, objectives=[0,1,2])
            if perturb_score_and_soln in pareto_efficient_set_scores_and_solution:
                curr_score = perturb_score # assign current soln to perturb soln
                soln = perturb_soln
            if (perturb_score <= curr_score).all:
                curr_score = perturb_score
                soln = perturb_soln
            print([[j[0], j[1], j[2]] for j in pareto_efficient_set_scores_and_solution])
            if time.time() - t0 > time_limit:
                break
    print("TIMEOUT: " + str(time_limit) + " seconds")
    pareto_efficient_set_scores_and_solution = pd.DataFrame(pareto_efficient_set_scores_and_solution)
    pareto_solns = pareto_efficient_set_scores_and_solution.iloc[:,3]
    pareto_solns = pareto_solns.tolist()
    pareto_scores = pareto_efficient_set_scores_and_solution.iloc[:, 0:3]
    print("Pareto Front Scores:")
    print(pareto_scores)
    t1 = time.time()
    print("Time Taken for MOSHCR: " + str(t1 - t0) + ' seconds')

    #plot_front_only(np.array(pareto_scores))

    return pareto_scores


def run_moshcr_1(current_schedule_list, to_schedule_read, mas_read, disc_select):

    OT_indexes = {0: 'L1',
                  1: 'L2',
                  2: 'L3',
                  3: 'L4',
                  4: 'L5',
                  5: 'L6',
                  6: 'L7',
                  7: 'L8',
                  8: 'M1',
                  9: 'M2',
                  10: 'M3',
                  11: 'M4',
                  12: 'M5',
                  13: 'OT 24',
                  14: 'OT 25',
                  15: 'OT 22',
                  16: 'R1',
                  17: 'R4',
                  18: 'R5',
                  19: 'R6',
                  20: 'R7',
                  21: 'R8',
                  22: 'MRI',
                  }

    current_schedule = current_schedule_list
    # add one more schedule_date
    schedule_date = current_schedule[2]
    # code on top ^
    schedule_days = current_schedule[1]
    day_index = current_schedule[3]
    current_schedule = current_schedule[0]
    # to_schedule = to_schedule_read
    to_schedule = to_schedule_read[0]
    to_schedule_dict = to_schedule_read[1]

    MAS_full = mas_read
    MAS_allowed = MAS_full[disc_select]

    t0 = time.time()

    # first fit or random fit
    schedule_copy = copy.deepcopy(current_schedule)
    soln = initial_solution_random_fit(schedule_copy, to_schedule, MAS_allowed, day_index, OT_indexes)

    # HILL CLIMBING ALGORITHM
    print("Hill Climbing Algorithm")

    R = 10 # number of restart runs
    max_iter = 100
    pareto_efficient_set_scores_and_solution = [[9999,9999,9999, soln]]
    time_limit = 180 # seconds
    for k in range(R):
        print("Restart" + str(k))
        schedule_copy = copy.deepcopy(current_schedule)
        soln = initial_solution_random_fit(schedule_copy, to_schedule, MAS_allowed, day_index, OT_indexes)
        for _ in range(max_iter):
            sp.pushback2(soln)
            past_pareto_scores_and_soln = copy.deepcopy(pareto_efficient_set_scores_and_solution)
            # print(past_pareto_scores)
            curr_score = MO_calculate(soln)
            legal_swaps = fd.all_legal_swaps(soln, to_schedule, MAS_allowed, day_index, OT_indexes)
            neighbour = random.choice(legal_swaps)  # stochastic hill climbing
            perturb_soln = sp.swapping(soln, neighbour)
            perturb_score = MO_calculate(perturb_soln)
            perturb_score_and_soln = perturb_score.tolist() + [perturb_soln]
            pareto_efficient_set_scores_and_solution.append(perturb_score_and_soln)
            pareto_efficient_set_scores_and_solution = pt.eps_sort(pareto_efficient_set_scores_and_solution, objectives=[0,1,2])
            if perturb_score_and_soln in pareto_efficient_set_scores_and_solution:
                curr_score = perturb_score # assign current soln to perturb soln
                soln = perturb_soln
            if (perturb_score <= curr_score).all:
                curr_score = perturb_score
                soln = perturb_soln
            print([[j[0], j[1], j[2]] for j in pareto_efficient_set_scores_and_solution])
            if time.time() - t0 > time_limit: break
        if time.time() - t0 > time_limit:
            print("TIMEOUT: " + str(time_limit) + " seconds")
            break
    pareto_efficient_set_scores_and_solution = pd.DataFrame(pareto_efficient_set_scores_and_solution)
    pareto_solns = pareto_efficient_set_scores_and_solution.iloc[:,3]
    pareto_solns = pareto_solns.tolist()
    pareto_scores = pareto_efficient_set_scores_and_solution.iloc[:, 0:3]
    print("Pareto Front Scores:")
    print(pareto_scores)
    t1 = time.time()
    print("Time Taken for MOSHCR: " + str(t1 - t0) + ' seconds')

    # sol_list = [pareto_solns[0], schedule_days, schedule_date, to_schedule_dict]
    # thread1 = Thread(target=show_timetable, args=[sol_list])
    # thread1.start()

    sol_list = [pareto_solns, schedule_days, schedule_date, to_schedule_dict]
    thread1 = Thread(target=show_timetable_1, args=[sol_list])
    thread1.start()

    plot_front_only(np.array(pareto_scores))

