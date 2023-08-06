import numpy as np
import pandas as pd
from SDP18py.Generate_initial_solution import initial_solution_random_fit
from SDP18py.MO_fitting_func_calc import MO_calculate
import pareto as pt
from SDP18py import genetic_algo_functions as ga
from SDP18py.plot_pareto_front import plot_front_only
import time
import copy
from SDP18py.view_timetable1 import show_timetable_1
from SDP18py.view_timetable1 import show_timetable
from threading import Thread


def run_nsga2(current_schedule_list, to_schedule_read, mas_read, disc_select, tl):

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
    # current_schedule = read_csv()
    # current_schedule = current_schedule[0]
    empty_schedule = copy.deepcopy(current_schedule)
    # to_schedule = read_toschedule()
    MAS_full = mas_read
    # MAS_full = read_mas()

    # MAS_allowed = MAS_full['OTO']
    MAS_allowed = MAS_full[disc_select]

    # first fit or random fit
    print("GENETIC ALGORITHM")
    n_pop = 100
    list_soln = []
    list_scores = []
    soln_list = []
    iter_ = 100
    t0 = time.time()
    time_limit = tl # seconds
    # Generate population of solutions first
    for i in range(n_pop):
        current_schedule_temp = copy.deepcopy(current_schedule)
        soln = initial_solution_random_fit(current_schedule_temp, to_schedule, MAS_allowed, day_index, OT_indexes)
        score = MO_calculate(soln).tolist()
        list_soln.append(soln)
        list_scores.append(score)

    old_pop = list_soln
    # do non domintated sort
    pareto_ranks, pareto_sorted_scores, pareto_sorted_solns = ga.pareto_ranking(list_scores, old_pop, n_pop)
    #for i in range(iter_):
    while time.time() -t0 < time_limit:
        child_pop = []
        for _ in range(n_pop):
            # parent selection
            p1, p2 = ga.select_two_parent(pareto_ranks, list_scores, old_pop)
            # crossover + mutation
            child, clashes = ga.GA_crossover(p1, p2, to_schedule, empty_schedule)
            child = ga.GA_mutate(child, clashes, MAS_allowed, OT_indexes, day_index)
            child_pop.append(child)
        total_pop = old_pop + child_pop
        # calculate the new population scores, which consists of all new and old populations
        list_scores = []
        for soln in total_pop:
            list_scores.append(MO_calculate(soln).tolist())

        pareto_ranks, pareto_sorted_scores, pareto_sorted_solns = ga.pareto_ranking(list_scores, total_pop, n_pop)
        # take top n_pop solutions
        old_pop = pareto_sorted_solns[0:n_pop]
        list_scores = pareto_sorted_scores[0:n_pop]
        print(pareto_sorted_scores[0:n_pop])

        if time.time() - t0 > time_limit: break
    print("TIMEOUT: " + str(time_limit) + " seconds")
    pareto_pop = []
    for index, scores in enumerate(pareto_sorted_scores):
        scores.append(pareto_sorted_solns[index])

    pareto_efficient_set_scores_and_solution = pt.eps_sort(pareto_sorted_scores, objectives=[0, 1, 2])

    pareto_efficient_set_scores_and_solution = pd.DataFrame(pareto_efficient_set_scores_and_solution)
    pareto_solns = pareto_efficient_set_scores_and_solution.iloc[:, 3]
    pareto_solns = pareto_solns.tolist()
    pareto_scores = pareto_efficient_set_scores_and_solution.iloc[:, 0:3]
    print("Pareto Front Scores:")
    print(pareto_scores)

    t1 = time.time()
    print("Time Taken for GA: " + str(t1 - t0) + ' seconds')
    #plot_front_only(np.array(pareto_scores))
    return pareto_scores


def run_nsga2_1(current_schedule_list, to_schedule_read, mas_read, disc_select):

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
    # current_schedule = read_csv()
    # current_schedule = current_schedule[0]
    empty_schedule = copy.deepcopy(current_schedule)
    # to_schedule = read_toschedule()
    MAS_full = mas_read
    # MAS_full = read_mas()

    # MAS_allowed = MAS_full['OTO']
    MAS_allowed = MAS_full[disc_select]

    # first fit or random fit
    print("GENETIC ALGORITHM")
    n_pop = 50
    list_soln = []
    list_scores = []
    soln_list = []
    iter_ = 200
    t0 = time.time()
    time_limit = 180 # seconds
    # Generate population of solutions first
    for i in range(n_pop):
        current_schedule_temp = copy.deepcopy(current_schedule)
        soln = initial_solution_random_fit(current_schedule_temp, to_schedule, MAS_allowed, day_index, OT_indexes)
        score = MO_calculate(soln).tolist()
        list_soln.append(soln)
        list_scores.append(score)

    old_pop = list_soln
    # do non domintated sort
    pareto_ranks, pareto_sorted_scores, pareto_sorted_solns = ga.pareto_ranking(list_scores, old_pop, n_pop)
    for i in range(iter_):
        child_pop = []
        for _ in range(n_pop):
            # parent selection
            p1, p2 = ga.select_two_parent(pareto_ranks, list_scores, old_pop)
            # crossover + mutation
            child, clashes = ga.GA_crossover(p1, p2, to_schedule, empty_schedule)
            child = ga.GA_mutate(child, clashes, MAS_allowed, OT_indexes, day_index)
            child_pop.append(child)
        total_pop = old_pop + child_pop
        # calculate the new population scores, which consists of all new and old populations
        list_scores = []
        for soln in total_pop:
            list_scores.append(MO_calculate(soln).tolist())

        pareto_ranks, pareto_sorted_scores, pareto_sorted_solns = ga.pareto_ranking(list_scores, total_pop, n_pop)
        # take top n_pop solutions
        old_pop = pareto_sorted_solns[0:n_pop]
        list_scores = pareto_sorted_scores[0:n_pop]
        print(pareto_sorted_scores[0:n_pop])

        if time.time() - t0 > time_limit:
            print("TIMEOUT: " + str(time_limit) + " seconds")
            break
    pareto_pop = []
    for index, scores in enumerate(pareto_sorted_scores):
        scores.append(pareto_sorted_solns[index])

    pareto_efficient_set_scores_and_solution = pt.eps_sort(pareto_sorted_scores, objectives=[0, 1, 2])

    pareto_efficient_set_scores_and_solution = pd.DataFrame(pareto_efficient_set_scores_and_solution)
    pareto_solns = pareto_efficient_set_scores_and_solution.iloc[:, 3]
    pareto_solns = pareto_solns.tolist()
    pareto_scores = pareto_efficient_set_scores_and_solution.iloc[:, 0:3]
    print("Pareto Front Scores:")
    print(pareto_scores)

    t1 = time.time()
    print("Time Taken for GA: " + str(t1 - t0) + ' seconds')

    # sol_list = [pareto_solns[0], schedule_days, schedule_date, to_schedule_dict]
    # thread1 = Thread(target=show_timetable, args=[sol_list])
    sol_list = [pareto_solns, schedule_days, schedule_date, to_schedule_dict]
    thread1 = Thread(target=show_timetable_1, args=[sol_list])
    thread1.start()

    plot_front_only(np.array(pareto_scores))
