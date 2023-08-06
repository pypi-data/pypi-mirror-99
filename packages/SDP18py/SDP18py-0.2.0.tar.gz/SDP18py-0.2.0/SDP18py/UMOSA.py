import numpy as np
import pandas as pd
from SDP18py.Generate_initial_solution import initial_solution_random_fit
from SDP18py.MO_fitting_func_calc import MO_calculate
from SDP18py.MO_fitting_func_calc import calculate_delta_S
from SDP18py.MO_fitting_func_calc import calculate_delta_S2
from SDP18py import find_legal_neighbors as fd, swapper as sp
from SDP18py.plot_pareto_front import plot_front_only
import time
import copy
import random
import pareto as pt
import itertools
from SDP18py.view_timetable1 import show_timetable
from SDP18py.view_timetable1 import show_timetable_1
from threading import Thread


def generate_weight_vectors():
    # these weights guide the search in a particlar direction, can add more if needed
    a = np.array(list(itertools.permutations([7, 2, 1])))
    a = np.divide(a, np.sum(a[0]))
    b = np.array(list(itertools.permutations([100, 1, 1])))
    b = np.divide(b, np.sum(b[0]))
    c = np.concatenate((a, b), axis=0)
    return c # the weights add up to 1


def run_umosa(current_schedule_list, to_schedule_read, mas_read, disc_select, tl):

    random.seed(10)

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
    lambdas_ = generate_weight_vectors() # weights
    t0 = time.time()

    # first fit or random fit
    soln = initial_solution_random_fit(current_schedule, to_schedule, MAS_allowed, day_index, OT_indexes)
    # SIMULATED ANNEALING ALGORITHM
    print("SIMULATED ANNEALING Algorithm") # hello

    alpha = 0.98  # cooling rate
    non_improve_soln_max = 30 #number of iteration of non improving solution before going to next weight
    period = 30  # periodically restarting at a randomly selected solution in pareto set, higher period deepersearch, lower period wider search
    pareto_efficient_set_scores_and_solution = [[9999,9999,9999, soln]]
    max_iter = 200
    time_limit = tl # seconds
    duration_per_weight = time_limit/len(lambdas_) #number of iteration of non improving solution before going to next weight
    print(duration_per_weight)
    for weights_vec in lambdas_:
        print("Weights:" + str(weights_vec))
        T = 1000  # higher temperature, higher chance of accepting bad solution (more diversed solution)
        i = 1
        tx = time.time()
        #non_improve_soln_count = 0
        #for _ in range(max_iter):
        while time.time() - tx < duration_per_weight:
            sp.pushback2(soln)
            past_pareto_scores_and_soln = copy.deepcopy(pareto_efficient_set_scores_and_solution)
            curr_score = MO_calculate(soln)
            legal_swaps = fd.all_legal_swaps(soln, to_schedule, MAS_allowed, day_index, OT_indexes)
            neighbour = random.choice(legal_swaps)  # draw a random solution Y from neighbourhood of X
            perturb_soln = sp.swapping(soln, neighbour)
            perturb_score = MO_calculate(perturb_soln)
            perturb_score_and_soln = perturb_score.tolist() + [perturb_soln]
            pareto_efficient_set_scores_and_solution.append(perturb_score_and_soln)
            pareto_efficient_set_scores_and_solution = pt.eps_sort(pareto_efficient_set_scores_and_solution, objectives=[0,1,2])
            if perturb_score_and_soln in pareto_efficient_set_scores_and_solution: # if after sort its still around
                curr_score = perturb_score  # assign current soln to perturb soln
                soln = perturb_soln
            else:
                p = calculate_delta_S2(curr_score, perturb_score, T, weights_vec, pareto_efficient_set_scores_and_solution)
                if p > random.uniform(0, 1):
                    soln = perturb_soln
                    curr_score = perturb_score
            if i%period == 0:
                soln = random.choice(pareto_efficient_set_scores_and_solution)[3]
            print([[j[0], j[1], j[2]] for j in pareto_efficient_set_scores_and_solution])
            i += 1
            T = T * alpha
            if time.time() - t0 > time_limit: break
        # if time.time() - t0 > time_limit:
        #     print("TIMEOUT: " + str(time_limit) + " seconds")
        #     break
    print("TIMEOUT: " + str(time_limit) + " seconds")
    pareto_efficient_set_scores_and_solution = pd.DataFrame(pareto_efficient_set_scores_and_solution)
    pareto_solns = pareto_efficient_set_scores_and_solution.iloc[:, 3]
    pareto_solns = pareto_solns.tolist()
    pareto_scores = pareto_efficient_set_scores_and_solution.iloc[:, 0:3]
    print("Pareto Front Scores:")
    print(pareto_scores)
    t1 = time.time()
    print("Time Taken for UMOSA: " + str(t1 - t0) + ' seconds')
    #plot_front_only(np.array(pareto_scores))
    return pareto_scores


def run_umosa_1(current_schedule_list, to_schedule_read, mas_read, disc_select):

    random.seed(10)

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
    lambdas_ = generate_weight_vectors() # weights
    t0 = time.time()

    # first fit or random fit
    soln = initial_solution_random_fit(current_schedule, to_schedule, MAS_allowed, day_index, OT_indexes)
    # SIMULATED ANNEALING ALGORITHM
    print("SIMULATED ANNEALING Algorithm")
    alpha = 0.98  # cooling rate
    period = 50  # periodically restarting at a randomly selected solution in pareto set, higher period deepersearch, lower period wider search
    pareto_efficient_set_scores_and_solution = [[9999,9999,9999, soln]]
    max_iter = 100
    time_limit = 180 # seconds
    for weights_vec in lambdas_:
        print("Weights:" + str(weights_vec))
        T = 1000  # higher temperature, higher chance of accepting bad solution (more diversed solution)
        i = 1
        non_improve_soln_count = 0
        for _ in range(max_iter):
            sp.pushback2(soln)
            past_pareto_scores_and_soln = copy.deepcopy(pareto_efficient_set_scores_and_solution)
            curr_score = MO_calculate(soln)
            legal_swaps = fd.all_legal_swaps(soln, to_schedule, MAS_allowed, day_index, OT_indexes)
            neighbour = random.choice(legal_swaps)  # draw a random solution Y from neighbourhood of X
            perturb_soln = sp.swapping(soln, neighbour)
            perturb_score = MO_calculate(perturb_soln)
            perturb_score_and_soln = perturb_score.tolist() + [perturb_soln]
            pareto_efficient_set_scores_and_solution.append(perturb_score_and_soln)
            pareto_efficient_set_scores_and_solution = pt.eps_sort(pareto_efficient_set_scores_and_solution, objectives=[0,1,2])
            if perturb_score_and_soln in pareto_efficient_set_scores_and_solution: # if after sort its still around
                curr_score = perturb_score  # assign current soln to perturb soln
                soln = perturb_soln
            else:
                p = calculate_delta_S2(curr_score, perturb_score, T, weights_vec, pareto_efficient_set_scores_and_solution)
                if p > random.uniform(0, 1):
                    soln = perturb_soln
                    curr_score = perturb_score
            if i%period == 0:
                soln = random.choice(pareto_efficient_set_scores_and_solution)[3]
            print([[j[0], j[1], j[2]] for j in pareto_efficient_set_scores_and_solution])
            i += 1
            T = T * alpha
            if time.time() - t0 > time_limit: break
        if time.time() - t0 > time_limit:
            print("TIMEOUT: " + str(time_limit) + " seconds")
            break

    pareto_efficient_set_scores_and_solution = pd.DataFrame(pareto_efficient_set_scores_and_solution)
    pareto_solns = pareto_efficient_set_scores_and_solution.iloc[:, 3]
    pareto_solns = pareto_solns.tolist()
    pareto_scores = pareto_efficient_set_scores_and_solution.iloc[:, 0:3]
    print("Pareto Front Scores:")
    print(pareto_scores)
    t1 = time.time()
    print("Time Taken for UMOSA: " + str(t1 - t0) + ' seconds')

    # sol_list = [pareto_solns[0], schedule_days, schedule_date, to_schedule_dict]
    # thread1 = Thread(target=show_timetable, args=[sol_list])
    sol_list = [pareto_solns, schedule_days, schedule_date, to_schedule_dict]
    thread1 = Thread(target=show_timetable_1, args=[sol_list])
    thread1.start()

    plot_front_only(np.array(pareto_scores))
