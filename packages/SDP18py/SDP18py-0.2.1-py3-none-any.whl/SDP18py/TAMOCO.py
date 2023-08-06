import numpy as np
import pandas as pd
from SDP18py.Generate_initial_solution import initial_solution_random_fit
from SDP18py.Generate_initial_solution import initial_solution_first_fit
from SDP18py.MO_fitting_func_calc import MO_calculate
import pareto as pt
from SDP18py import find_legal_neighbors as fd, swapper as sp
from SDP18py.plot_pareto_front import plot_front_only
import time
import random
from SDP18py.view_timetable1 import show_timetable
from SDP18py.view_timetable1 import show_timetable_1
from threading import Thread


def run_tamoco(current_schedule_list, to_schedule_read, mas_read, disc_select, tl):

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
    k = 10  # number of solutions in X
    drift_criterion_iter = 15
    tabu_tenure = 5
    time_limit = tl #seconds
    #iter_max = 200
    soln_list = []
    X = []
    pareto_efficient_set_scores_and_solution = [[9999, 9999, 9999, 'a']]
    pareto_efficient_set_solns = []
    for _ in range(k): # generate parallel initial solution list
        soln = initial_solution_random_fit(current_schedule, to_schedule, MAS_allowed, day_index, OT_indexes)
        score = MO_calculate(soln)
        score_and_soln = score.tolist() + [soln]
        X.append(score_and_soln)

    count = 1
    pi_k = np.array([1/3, 1/3, 1/3], dtype=float) # initalize pi_k as all 1/3, will change according to scale of solutions in pareto frontier later
    tabu_list = [[None] for i in range(k)]
    #for _ in range(iter_max):
    while time.time()-t0 <time_limit:
        for index, score_and_soln in enumerate(X): # a parallel tabu search
            flag = 0
            score_i = score_and_soln[:3]
            lambda_ = np.array([0, 0, 0])
            soln = score_and_soln[3]
            for score_and_soln2 in X: # gotta adjust the weights to spread the pareto solutions
                score_j = score_and_soln2[:3]
                if not score_i == score_j:  # it will be based on how far it is from other solutions
                    if (np.array(score_i) > np.array(score_j)).any():  # check if i dominates j
                        lambda_ = new_lambda(score_i, score_j, pi_k, lambda_)
            # generate all legal swaps
            legal_swaps = fd.all_legal_swaps_subset(soln, to_schedule, MAS_allowed, day_index, OT_indexes)
            fy = []

            for swaps in legal_swaps:  # calculate score vector for each swap
                vec_score = MO_calculate(sp.swapping(soln, swaps))
                scaler_score = np.sum(np.multiply(vec_score, lambda_))
                fy.append(scaler_score)
            min_index = fy.index(min(fy)) # chosen solution
            new_soln = sp.swapping(soln, legal_swaps[min_index])
            new_vec_score = MO_calculate(new_soln).tolist()
            new_score_and_soln = new_vec_score + [new_soln]
            while "".join([str(i) for i in new_vec_score]) in tabu_list[index]:
                print("tabu!")
                fy.pop(min_index)
                if len(fy) == 0:
                    flag == 1
                    print("All nieghboring solutions are tabooed, jumping to next search instead")
                    break
                min_index = fy.index(min(fy))
                new_soln = sp.swapping(soln, legal_swaps[min_index])
                new_vec_score = MO_calculate(new_soln).tolist()
                new_score_and_soln = new_vec_score + [new_soln]
            if flag == 1: continue
            X[index] = new_score_and_soln
            tabu_list[index] = pop_tabu_list(tabu_list[index])
            tabu_list[index] = tabu_list[index] + ["".join([str(i) for i in new_vec_score])] * tabu_tenure
            pareto_efficient_set_scores_and_solution.append(new_score_and_soln)
            pareto_efficient_set_scores_and_solution = pt.eps_sort(pareto_efficient_set_scores_and_solution, objectives=[0,1,2])
            pi_k = adjust_pi_k(pi_k, pareto_efficient_set_scores_and_solution)
            count += 1
            if count == drift_criterion_iter:
                print("drift criterion reached: randomly assigning X")
                r1 = random.randint(0, len(X)-1)
                r2 = random.randint(0, len(X) - 1)
                X[r1] = X[r2] # randomly change a solution to another
            print([[j[0], j[1], j[2]] for j in pareto_efficient_set_scores_and_solution])
            if time.time() - t0 > time_limit: break

    print("TIMEOUT: " + str(time_limit) + " seconds")
    pareto_efficient_set_scores_and_solution = pd.DataFrame(pareto_efficient_set_scores_and_solution)
    pareto_solns = pareto_efficient_set_scores_and_solution.iloc[:, 3]
    pareto_solns = pareto_solns.tolist()
    pareto_scores = pareto_efficient_set_scores_and_solution.iloc[:, 0:3]
    print("Pareto Front Scores:")
    print(pareto_scores)
    t1 = time.time()
    print("Time Taken for TAMOCO: " + str(t1 - t0) + ' seconds')
    #plot_front_only(np.array(pareto_scores))
    return pareto_scores

def new_lambda(score1, score2, pi_k, lambda_):
    score1 = np.array(score1)
    score2 = np.array(score2)
    d = abs(score1-score2)
    d = np.multiply(d, pi_k)
    w = 1/np.sum(d)
    t = score1 < score2 # update lambda_ for those with i > j
    lambda_ = lambda_ + w * pi_k * t # dont update lambda for those worse

    return lambda_/np.sum(lambda_)


def pop_tabu_list(tabu_list):
    uniq = list(set(tabu_list))
    for value in uniq:
        tabu_list.remove(value)
    return tabu_list


def adjust_pi_k(pi_k, pareto_scores):
    pareto_scores = np.array(pareto_scores)[:, :3]
    max_overtime, max_idletime, max_waittime = pareto_scores.max(axis=0)
    min_overtime, min_idletime, min_waittime = pareto_scores.min(axis=0)
    range_arr = np.array([max_overtime-min_overtime, max_idletime-min_idletime, max_waittime-min_waittime])
    if (range_arr == 0).any():
        return np.array([1 / 3, 1 / 3, 1 / 3], dtype=float)

    return range_arr/np.sum(range_arr)


def run_tamoco_1(current_schedule_list, to_schedule_read, mas_read, disc_select, tl):

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
    k = 10  # number of solutions in X
    drift_criterion_iter = 15
    tabu_tenure = 5
    time_limit = tl  # seconds
    # iter_max = 200
    soln_list = []
    X = []
    pareto_efficient_set_scores_and_solution = [[9999, 9999, 9999, 'a']]
    pareto_efficient_set_solns = []
    for _ in range(k):  # generate parallel initial solution list
        soln = initial_solution_random_fit(current_schedule, to_schedule, MAS_allowed, day_index, OT_indexes)
        score = MO_calculate(soln)
        score_and_soln = score.tolist() + [soln]
        X.append(score_and_soln)

    count = 1
    pi_k = np.array([1 / 3, 1 / 3, 1 / 3],
                    dtype=float)  # initalize pi_k as all 1/3, will change according to scale of solutions in pareto frontier later
    tabu_list = [[None] for i in range(k)]
    # for _ in range(iter_max):
    while time.time() - t0 < time_limit:
        for index, score_and_soln in enumerate(X):  # a parallel tabu search
            flag = 0
            score_i = score_and_soln[:3]
            lambda_ = np.array([0, 0, 0])
            soln = score_and_soln[3]
            for score_and_soln2 in X:  # gotta adjust the weights to spread the pareto solutions
                score_j = score_and_soln2[:3]
                if not score_i == score_j:  # it will be based on how far it is from other solutions
                    if (np.array(score_i) > np.array(score_j)).any():  # check if i dominates j
                        lambda_ = new_lambda(score_i, score_j, pi_k, lambda_)
            # generate all legal swaps
            legal_swaps = fd.all_legal_swaps_subset(soln, to_schedule, MAS_allowed, day_index, OT_indexes)
            fy = []

            for swaps in legal_swaps:  # calculate score vector for each swap
                vec_score = MO_calculate(sp.swapping(soln, swaps))
                scaler_score = np.sum(np.multiply(vec_score, lambda_))
                fy.append(scaler_score)
            min_index = fy.index(min(fy))  # chosen solution
            new_soln = sp.swapping(soln, legal_swaps[min_index])
            new_vec_score = MO_calculate(new_soln).tolist()
            new_score_and_soln = new_vec_score + [new_soln]
            while "".join([str(i) for i in new_vec_score]) in tabu_list[index]:
                print("tabu!")
                fy.pop(min_index)
                if len(fy) == 0:
                    flag == 1
                    print("All nieghboring solutions are tabooed, jumping to next search instead")
                    break
                min_index = fy.index(min(fy))
                new_soln = sp.swapping(soln, legal_swaps[min_index])
                new_vec_score = MO_calculate(new_soln).tolist()
                new_score_and_soln = new_vec_score + [new_soln]
            if flag == 1: continue
            X[index] = new_score_and_soln
            tabu_list[index] = pop_tabu_list(tabu_list[index])
            tabu_list[index] = tabu_list[index] + ["".join([str(i) for i in new_vec_score])] * tabu_tenure
            pareto_efficient_set_scores_and_solution.append(new_score_and_soln)
            pareto_efficient_set_scores_and_solution = pt.eps_sort(pareto_efficient_set_scores_and_solution,
                                                                   objectives=[0, 1, 2])
            pi_k = adjust_pi_k(pi_k, pareto_efficient_set_scores_and_solution)
            count += 1
            if count == drift_criterion_iter:
                print("drift criterion reached: randomly assigning X")
                r1 = random.randint(0, len(X) - 1)
                r2 = random.randint(0, len(X) - 1)
                X[r1] = X[r2]  # randomly change a solution to another
            print([[j[0], j[1], j[2]] for j in pareto_efficient_set_scores_and_solution])
        if time.time() - t0 > time_limit: break

    print("TIMEOUT: " + str(time_limit) + " seconds")
    pareto_efficient_set_scores_and_solution = pd.DataFrame(pareto_efficient_set_scores_and_solution)
    pareto_solns = pareto_efficient_set_scores_and_solution.iloc[:, 3]
    pareto_solns = pareto_solns.tolist()
    pareto_scores = pareto_efficient_set_scores_and_solution.iloc[:, 0:3]
    print("Pareto Front Scores:")
    print(pareto_scores)
    t1 = time.time()
    print("Time Taken for TAMOCO: " + str(t1 - t0) + ' seconds')

    # sol_list = [pareto_solns[0], schedule_days, schedule_date, to_schedule_dict]
    # thread1 = Thread(target=show_timetable, args=[sol_list])
    sol_list = [pareto_solns, schedule_days, schedule_date, to_schedule_dict]
    thread1 = Thread(target=show_timetable_1, args=[sol_list])
    thread1.start()

    plot_front_only(np.array(pareto_scores))