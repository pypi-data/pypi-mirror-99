from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as mtri
import pareto as pt
import copy

def plot_front2(dp, pp, iter):

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(dp[:,0],dp[:,1],dp[:,2])
	ax.scatter(pp[:,0],pp[:,1],pp[:,2],color='red')

	triang = mtri.Triangulation(pp[:, 0], pp[:, 1])
	ax.plot_trisurf(triang, pp[:, 2], color='red')
	ax.set_xlim(0, 2500)
	ax.set_ylim(650, 720)
	ax.set_zlim(70, 160)
	#plt.show()
	plt.savefig('plt' + str(iter) + '.png')

	return

def plot_front(dp, pp):

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(dp[:,0],dp[:,1],dp[:,2])
	ax.scatter(pp[:,0],pp[:,1],pp[:,2],color='red')

	triang = mtri.Triangulation(pp[:, 0], pp[:, 1])
	ax.plot_trisurf(triang, pp[:, 2], color='red')
	plt.show()
	return


def plot_front_only(pp):

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(pp[:,0],pp[:,1],pp[:,2],color='blue')

	triang = mtri.Triangulation(pp[:, 0], pp[:, 1])
	ax.plot_trisurf(triang, pp[:, 2], color='blue')
	plt.show()
	return



def pareto_ranking(scores1):
	scores = copy.deepcopy(scores1).tolist()
	rankswanted = 5
	n = 10
	pareto_chosen = []
	for _ in range(rankswanted):
		pareto_efficient_pts = pt.eps_sort(scores)
		for sc in pareto_efficient_pts:
			pareto_chosen.append(sc)
		scores = [x for x in scores if x not in pareto_efficient_pts]
	return pareto_chosen[0:n]


def plot_front_multiple(pp_hco, pp_sa, pp_ts, pp_ga):

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	#hco - red
	ax.scatter(pp_hco[:,0],pp_hco[:,1],pp_hco[:,2],color='red')
	triang = mtri.Triangulation(pp_hco[:, 0], pp_hco[:, 1])
	ax.plot_trisurf(triang, pp_hco[:, 2], color='red')

	#sa - blue
	ax.scatter(pp_sa[:,0],pp_sa[:,1],pp_sa[:,2],color='blue')
	triang = mtri.Triangulation(pp_sa[:, 0], pp_sa[:, 1])
	ax.plot_trisurf(triang, pp_sa[:, 2], color='blue')

	#ts - green
	ax.scatter(pp_ts[:,0],pp_ts[:,1],pp_ts[:,2],color='green')
	triang = mtri.Triangulation(pp_ts[:, 0], pp_ts[:, 1])
	ax.plot_trisurf(triang, pp_ts[:, 2], color='green')

	#ga - pink
	ax.scatter(pp_ga[:,0],pp_ga[:,1],pp_ga[:,2],color='pink')
	triang = mtri.Triangulation(pp_ga[:, 0], pp_ga[:, 1])
	ax.plot_trisurf(triang, pp_ga[:, 2], color='pink')
	plt.show()
	return