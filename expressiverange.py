import json
import math

import numpy as np

from functools import reduce

from metrics.expressivemetrics import density_metric, repetition_metric
from metrics.getexperiments import create_2d_bucket_plot
from run_utils.profileimporter import import_example_as_block
from run_utils.runprofile import get_profile_from_file
from solving.util import dimensional_tuple_to_dict, deep_merge
import matplotlib.pyplot as plt

import os

cell_size = (5,4,5)

def compute_expressive_range(name, blocks, empty_ids, no_repetition_ids, profile, amount, i=0):
    density = [(density_metric(block, empty_ids)) for block in blocks]
    # variety = [(variety_metric(block, profile, empty_ids)) for block in blocks]
    repetition = [(repetition_metric(block, profile, no_repetition_ids)) for block in blocks]
    def to_format(name_1, name_2, data):
        result = {name_1: [t[0] for t in data], name_2: [t[1] for t in data]}
        print(result)
        return result
    # plt.subplot(amount, 2, i*2+1)
    # create_2d_bucket_plot(name, "density", "variety", to_format("density", "variety", list(zip(density, variety))), False)
    # plt.subplot(amount, 2, i*2+2)
    a, b = math.ceil(math.sqrt(amount)), math.floor(math.sqrt(amount))
    plt.subplot(a, b + (1 if a * b < amount else 0), i + 1)
    result = to_format("density", "repetition", list(zip(density, repetition)))
    return result


def compute_all_from_folders(profile, main_folder):
    folders = [folder for folder in
                 os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, folder))]
    results = {}

    for i, folder in enumerate(folders):
        blocks = [import_example_as_block(os.path.join(os.path.join(main_folder, folder), "result.vox"), (5, 4, 5), profile)]
        result = compute_expressive_range(folder, blocks, ["void", "flatsurface"], ["void", "flatsurface"], profile, len(folders), i)
        results = deep_merge(results, {folder: result})
        with open('resultexpressiverange.json', 'w') as outfile:
            json.dump(results, outfile)
    return results


def plot_from_json(results, latex=False, seperate=False):
    if latex:
        import matplotlib
        matplotlib.use("pgf")
        matplotlib.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
        })

    flattened_results = reduce(lambda agg, k: deep_merge(agg, results[k]), results, {})
    complete = create_2d_bucket_plot("completelog", "density", "repetition", flattened_results, log=True, bar=False, grid=False, grayscale=True)
    plt.show()
    # max value is the closest power to 10 rounded above
    max_value = int(np.max(np.nan_to_num(complete[0])))
    max_value = 10 ** np.ceil(np.log10(max_value))
    print(max_value)
    create_2d_bucket_plot("complete", "density", "repetition", flattened_results, False, grayscale=False)
    plt.show()
    create_2d_bucket_plot("complete", "density", "repetition", flattened_results, False, grayscale=False, log=True, bar=True)
    plt.show()
    create_2d_bucket_plot("Expressive Range", "density", "repetition", flattened_results, max_val=max_value,
                          log=True, bar=True, grid=False, grayscale=True)
    plt.show()
    plt.savefig(f'{"Expressive Range"}.pgf')



def draw_subplots(results, log=False):
    amount = len(results)
    for i, k in enumerate(results):
        a, b = math.ceil(math.sqrt(amount)), math.floor(math.sqrt(amount))
        plt.subplot(a, b + (1 if a * b < amount else 0), i + 1)
        create_2d_bucket_plot(k, "density", "repetition", results[k], False, log)
    plt.show()

profile = get_profile_from_file("profiles/base/base.json", dimensional_tuple_to_dict(cell_size))
results = compute_all_from_folders(profile, "experiments")
plot_from_json(results, latex=False, seperate=False)