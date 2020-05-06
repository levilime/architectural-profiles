import numpy as np

import networkx as nx
from matplotlib import colors
from matplotlib.colors import LogNorm

from solving.util import dimensional_dict_to_tuple, merge_dicts
import matplotlib.pyplot as plt

SAVE_LOCATION = "experiments"

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_t = dimensional_dict_to_tuple(cell_size)

def create_bucket_plot(name, metrics):
    for i, metric in enumerate(metrics):
        metric_dimension = metric
        metric_data = metrics[metric]
        i = i + 1
        plt.subplot(1, 2, i)
        plt.hist(metric_data, 10, range=(0.0, 1.0), density=True, facecolor='g', alpha=0.75, orientation='horizontal')
        plt.xlabel("amount")
        plt.ylabel(metric_dimension)
        plt.title(name)
    plt.tight_layout()
    plt.show()

def create_2d_bucket_plot(name, metric_1, metric_2, metrics, show=True,  max_val=None, log=False, grayscale=True, bar=False, grid=True, title=True, label=True):
    # plt.plot()
    kwargs = dict(norm=colors.LogNorm()) if log else dict()
    kwargs = merge_dicts(kwargs, dict(cmap='gray_r') if grayscale else dict())
    kwargs = merge_dicts(kwargs, dict(norm=LogNorm(1, max_val)) if max_val else dict())
    plt.figure(name)
    p = plt.hist2d(metrics[metric_1], metrics[metric_2], cmin=0, bins=10, range=([[0.0, 1.0], [0.0, 1.0]])#, norm=colors.LogNorm()
               , **kwargs)
    if label:
        plt.xlabel(metric_1)
        plt.ylabel(metric_2)
    else:
        plt.axes().tick_params(labelbottom=False)
        plt.axes().tick_params(labelleft=False)

    plt.yticks(np.arange(0, 1.0, step=0.1))
    plt.xticks(np.arange(0, 1.0, step=0.1))
    # plt.xticks([])
    # plt.yticks([])
    if grid:
        plt.grid()
    if title:
        plt.title(name)
    if bar:
        plt.colorbar()
    plt.tight_layout()

    if show:
        plt.show()
    return p

def show_graphs(graphs):
    for graph_title in graphs:
        plt.plot()
        plt.title(graph_title)
        nx.draw(graphs[graph_title], with_labels=True, font_weight='bold')
        plt.show()

# solutions = []
#
# for experiment_folder in os.listdir(SAVE_LOCATION):
#     try:
#         with open(os.path.join(SAVE_LOCATION, experiment_folder, "solutions.json")) as json_file:
#             file = json.load(json_file)
#
#         with open(os.path.join(SAVE_LOCATION, experiment_folder, "profile.json")) as json_file:
#             profile = import_profile(json.load(json_file), '5x4x5x', cell_size_t)
#         for raw_result in file["solutions"]:
#             result = Result.create_from_json(raw_result["solution"])
#             blocks = []
#             all_graphs = {}
#             for solution in result.solutions:
#                 graphs = convert_to_graph(block_from_result(
#                     solution, BlockSolver(solution.represented_block_size(), cell_size, profile)), profile)
#                 all_graphs = reduce(lambda agg, k: deep_merge(agg, {k: [graphs[k]]}), graphs, all_graphs)
#                 # show_graphs(graphs)
#                 blocks.append(block_from_result(
#                     solution, BlockSolver(solution.represented_block_size(), cell_size, profile)))
#
#             info = {"density": density_metrics(blocks, {"flatsurface", "void"}),
#                                 "efficiency": efficiency_metrics(all_graphs["routing"])
#                                 }
#             solutions.append((experiment_folder, info))
#             #create_bucket_plot(experiment_folder,info)
#     except:
#         print("files " + experiment_folder + " not found.")

# data = reduce(lambda agg, entry: deep_merge(agg, entry), [x[1] for x in solutions], {})
# create_2d_bucket_plot("all", "density", "efficiency", data)
