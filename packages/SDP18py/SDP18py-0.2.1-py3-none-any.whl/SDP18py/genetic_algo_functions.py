import numpy as np
import numpy_indexed as npi
import random
import copy
import pareto as pt
from operator import itemgetter
from SDP18py.Generate_initial_solution import initial_solution_random_fit



def pareto_ranking(scores1, solns, n):
	scores = copy.deepcopy(scores1)
	pareto_rankings = {}
	pareto_sorted_scores = []
	pareto_sorted_soln = []
	rank = 0
	n_pop = 0
	while len(scores) != 0:
		pareto_efficient_pts = pt.eps_sort(scores)
		l = len(pareto_efficient_pts)
		n_pop += l
		if n_pop >= n:
			overshot = n_pop-n
			pareto_efficient_pts = pareto_efficient_pts[0:(l-overshot)]
			pareto_rankings[rank] = pareto_efficient_pts
			pareto_sorted_scores = pareto_sorted_scores + pareto_efficient_pts
			scores = [x for x in scores if x not in pareto_efficient_pts]
			rank += 1
			for i in pareto_efficient_pts:
				loc = np.where((scores1 == np.array(i)).all(axis=1))[0][0]
				pareto_sorted_soln.append(solns[loc])
			return pareto_rankings, pareto_sorted_scores, pareto_sorted_soln
		pareto_rankings[rank] = pareto_efficient_pts
		pareto_sorted_scores = pareto_sorted_scores + pareto_efficient_pts
		scores = [x for x in scores if x not in pareto_efficient_pts]
		rank += 1
		for i in pareto_efficient_pts:
			loc = np.where((scores1 == np.array(i)).all(axis=1))[0][0]
			pareto_sorted_soln.append(solns[loc])
	return pareto_rankings, pareto_sorted_scores, pareto_sorted_soln


def pareto_score_soln_sore(scores1, soln):
	scores = copy.deepcopy(scores1)
	pareto_sorted_scores = []
	pareto_sorted_soln = []


def select_two_parent(ranks, list_scores, list_soln):
	# crowding distance tournament to select parent
	crowding_dist = list(calc_crowding_distance(np.array(list_scores)))
	tournament_size = 16 # multiples of 8
	tournament_population = random.sample(list_scores, tournament_size)
	random.shuffle(tournament_population)
	#tournament_population_indexes = npi.indices(np.array(list_scores), tournament_population)
	#tournament_crowding_distance = itemgetter(*tournament_population_indexes)(crowding_dist)
	tournament_population = np.array(tournament_population).reshape(tournament_size//2, 2, 3)

	# tournament starts
	two_winners = tournament(tournament_population, crowding_dist, list_scores)

	p1_score_loc = np.where((list_scores == np.array(two_winners[0])).all(axis=1))[0][0]
	p2_score_loc = np.where((list_scores == np.array(two_winners[1])).all(axis=1))[0][0]

	return list_soln[p1_score_loc], list_soln[p2_score_loc]


def GA_crossover(p1, p2, sch_list, empty_schedule):
	child = copy.deepcopy(empty_schedule)
	clashes = []
	for to_sch in sch_list:
		r = random.randint(1, 2)
		surg = to_sch[0]
		if r == 1:
			p1_surg_loc = np.argwhere(p1==surg)
			if check_if_zero(child,p1_surg_loc):
				#put it in
				day = p1_surg_loc[0][0]
				OT = p1_surg_loc[0][1]
				start_ts = p1_surg_loc[0][2]
				end_ts = p1_surg_loc[-1][2] + 1
				np.put(child[day][OT], np.arange(start=start_ts, stop=end_ts), [surg])
			else:
				clashes.append(to_sch)
		elif r == 2:
			p2_surg_loc = np.argwhere(p2==surg)
			if check_if_zero(child,p2_surg_loc):
				#put it in
				day = p2_surg_loc[0][0]
				OT = p2_surg_loc[0][1]
				start_ts = p2_surg_loc[0][2]
				end_ts = p2_surg_loc[-1][2] + 1
				np.put(child[day][OT], np.arange(start=start_ts, stop=end_ts), [surg])
			else:
				clashes.append(to_sch)
	#print(clashes)
	return child, clashes


def GA_mutate(child, clashes, MAS_allowed, OT_indexes, day_of_week_indexes):
	if len(clashes)==0:
		return child
	else:
		child = initial_solution_random_fit(child, clashes, MAS_allowed, day_of_week_indexes, OT_indexes)
		return child


def check_if_zero(empty_schedule, locs):
	len_zero = len(locs)
	day = locs[0][0]
	OT = locs[0][1]
	start_ts = locs[0][2]
	end_ts = locs[-1][2] + 1
	partition = empty_schedule[day][OT][start_ts:end_ts]
	if np.all(partition == np.zeros(len_zero)):
		return True
	else:
		return False


def calc_crowding_distance(F):
	infinity = 1e+14

	n_points = F.shape[0]
	n_obj = F.shape[1]

	if n_points <= 2:
		return np.full(n_points, infinity)
	else:

		# sort each column and get index
		I = np.argsort(F, axis=0, kind='mergesort')

		# now really sort the whole array
		F = F[I, np.arange(n_obj)]

		# get the distance to the last element in sorted list and replace zeros with actual values
		dist = np.concatenate([F, np.full((1, n_obj), np.inf)]) \
		       - np.concatenate([np.full((1, n_obj), -np.inf), F])

		index_dist_is_zero = np.where(dist == 0)

		dist_to_last = np.copy(dist)
		for i, j in zip(*index_dist_is_zero):
			dist_to_last[i, j] = dist_to_last[i - 1, j]

		dist_to_next = np.copy(dist)
		for i, j in reversed(list(zip(*index_dist_is_zero))):
			dist_to_next[i, j] = dist_to_next[i + 1, j]

		# normalize all the distances
		norm = np.max(F, axis=0) - np.min(F, axis=0)
		norm[norm == 0] = np.nan
		dist_to_last, dist_to_next = dist_to_last[:-1] / norm, dist_to_next[1:] / norm

		# if we divided by zero because all values in one columns are equal replace by none
		dist_to_last[np.isnan(dist_to_last)] = 0.0
		dist_to_next[np.isnan(dist_to_next)] = 0.0

		# sum up the distance to next and last and norm by objectives - also reorder from sorted list
		J = np.argsort(I, axis=0)
		crowding = np.sum(dist_to_last[J, np.arange(n_obj)] + dist_to_next[J, np.arange(n_obj)], axis=1) / n_obj

	# replace infinity with a large number
	crowding[np.isinf(crowding)] = infinity

	return crowding

def tournament(tournament_population, crowding_dist, list_scores):
	tournament_population_list = tournament_population.tolist()  # because we will be removing the ones that lost, better to use list
	for index, versus in enumerate(tournament_population):
		score1 = versus[0]
		score2 = versus[1]
		if (score1 <= score2).all():  # score 1 dominiates
			# score2 loses
			tournament_population_list[index].remove(score2.tolist())

		elif (score2 <= score1).all():  # score 2 dominates
			# score1 loses
			tournament_population_list[index].remove(score1.tolist())

		else:  # same rank
			# based on crowding distance instead
			index1_ = list_scores.index(score1.tolist())
			index2_ = list_scores.index(score2.tolist())
			crowd_score1 = crowding_dist[index1_]
			crowd_score2 = crowding_dist[index2_]
			if crowd_score1 > crowd_score2:
				tournament_population_list[index].remove(score2.tolist())
			else:
				tournament_population_list[index].remove(score1.tolist())
	print(tournament_population_list)
	random.shuffle(tournament_population_list)
	new_tournament_pop = np.array(tournament_population_list)
	new_tournament_pop= new_tournament_pop.reshape(-1, 3)
	if len(new_tournament_pop) == 2:
		return new_tournament_pop
	new_tournament_pop = new_tournament_pop.reshape(len(new_tournament_pop)//2, 2, 3)

	winners = tournament(new_tournament_pop, crowding_dist, list_scores)
	return winners