import json
import time
from functools import reduce
from itertools import product

from ast import literal_eval

import math

import numpy as np

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

from batch import batch_list
from runprofile import run_profile_from_file, get_profile_from_file, run_profile
from shaperun import create_from_profile
from solving.util import color_connected_parts, merge_dicts, dimensional_tuple_to_dict, dimensional_dict_to_tuple
from voxels.magicavoxwrapper import visualize_voxel, export

grid_size = {"x":1, "y":1, "z":1}
cell_size = {"x": 5, "y": 4, "z": 5}
block_size = {"x": 5, "y":3, "z":5}

with open("../profiles/base/shapebasestairsstreetconstruction.json", 'r') as f:
    profile_json = json.load(f)

profile = "profiles/1story/flathouses.json"
# profile = get_profile_from_file("profiles/mountaintownbasicconnected.json", cell_size)

# min_block = (1,1,1)
# max_block = (8, 4, 8)
# possible_sizes = product(*[range(mi, ma + 1) for mi, ma in
#                                    zip(min_block,
#                                    max_block)])

# min_size = 1
# max_size = 500
# amount_sizes = 10
#
# possible_sizes = [(1,1,1)] + [(math.ceil(a),math.ceil(a/2),math.ceil(a)) for a in map(lambda v: v ** (1/3),
#                                        range(int(max_size/amount_sizes), int(max_size), int(max_size/amount_sizes)))]

max_size = 10
possible_sizes = [(x, math.ceil(x/2), x) for x in range(1, 10 + 1)] + [(7,7,7)]

# times = {}
# for i, batch in zip(map(str, range(0, len(batch_list))), batch_list):
#     profile, location = batch
#     profile_name = i
#     create_from_profile(profile_json, profile, location, 0, True, input_size=dimensional_tuple_to_dict((1,1,1)))
#     times[profile_name] = {}
#     for size in possible_sizes:
#         #for i in range(0, 3):
#         amount = 10
#         start = time.time()
#         # run_profile(profile, grid_size, dimensional_tuple_to_dict(size), cell_size)
#         create_from_profile(profile_json, profile, location, amount, False, input_size=dimensional_tuple_to_dict(size))
#         end = time.time()
#         time_used = end - start
#         print(f"{location}, time: {time_used}, amount: {amount}")
#         average_time = time_used/amount
#         if size in times:
#             times[profile_name][str(size)].append(average_time)
#         else:
#             times[profile_name][str(size)] = [average_time]
#         with open('runtimeresults.json', 'w') as outfile:
#             json.dump(times, outfile)

# with open('runtimeresults.json', 'w') as outfile:
#     json.dump(times, outfile)
with open('runtimeresults.json') as json_file:
    times = json.load(json_file)

print(times)
entries = []
for profile in times:
    for size in times[profile]:
        entries += [(profile, literal_eval(size), np.average(times[profile][size]))]


# summed_times = reduce(lambda agg, k: merge_dicts(agg, {k: np.average(times[k])}), times, {})
# print(summed_times)
#
# import matplotlib.pyplot as plt
#
# zipped_times = sorted([((np.prod(k), k), summed_times[k]) for k in summed_times], key=lambda t: t[0][0])
#
# # plotting points as a scatter plot
# plt.scatter([t[0][0] for t in zipped_times], [t[1] for t in zipped_times], label="stars", color="black",
#             marker="*", s=30)



def take_i_ll(ll, i):
    return [e[i] for e in ll]

def surface_plot():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x = list(map(lambda x: np.prod(literal_eval(x)), list(times[list(times)[0]])))
    y = list(times)
    X = np.zeros((len(x), len(y)))
    for i in range(0, len(x)):
        X[i, :] = x[i]
    Y = np.zeros((len(x), len(y)))
    for i in range(0, len(y)):
        Y[:, i] = y[i]
    Z = np.zeros((len(x), len(y)))
    for i, t in enumerate(product(range(0, len(y)), range(0, len(x)))):
        Z[t[1], t[0]] = entries[i][2] if i < len(entries) else np.max(Z)#0

    ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    # # x-axis label
    # plt.xlabel('(cell amount)')
    # frequency label
    # plt.ylabel('average time (s)')
    # plot title
    ax.set_title('Run time of profiles at different sizes')
    # showing legend
    # plt.legend()

    # function to show the plot
    plt.show()

def scatter_plot():
    fig= plt.figure()
    ax = plt.axes()
    gg= ["b","g", "i", "j", "k"]
    for i, p in enumerate([list(times)[1], list(times)[3], list(times)[7], list(times)[10], list(times)[14]]):
        x,y = list(map(lambda x: np.prod(literal_eval(x)), times[p])), [np.average(times[p][x]) for x in times[p]]
        # plt.xlim(right=np.max(x))
        x,y = list(zip(*sorted(zip(x,y), key=lambda t: t[0])))
        plt.plot(x, y, marker="."#f"${p}$"
                 , label=gg[i], markeredgecolor="black")
        # plt.scatter(x,y, label=p, color="black",
        #             marker="$a$", s=30)
    plt.ylim(bottom=0)

    plt.ylim(top=12)
    ax.set_title('Run time of profiles for different Model sizes')
    # x-axis label
    plt.xlabel('(cell amount)')
    # frequency label
    plt.ylabel('average time (s)')

    plt.legend()
    plt.show()

scatter_plot()

