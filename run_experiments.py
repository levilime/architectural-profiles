import json
import os
import time
from functools import reduce
from itertools import product

from deepmerge import Merger

from run_utils.runprofile import run_profile_from_json
from solving.util import color_connected_parts
from voxels.magicavoxwrapper import export

grid_size_one_block = {"x":1, "y":1, "z":1}
grid_size_horizontal = {"x":2, "y":1, "z":2}
grid_size_horizontal_big = {"x":3, "y":1, "z":3}
grid_size_full = {"x":3, "y":3, "z":3}
cell_size = {"x": 5, "y": 4, "z": 5}
block_size = {"x":3, "y":3, "z":3}

# grid_size_t = dimensional_dict_to_tuple(grid_size)
# cell_size_t = dimensional_dict_to_tuple(cell_size)
# block_size_t = dimensional_dict_to_tuple(block_size)

SAVE_LOCATION = "experiments/"
TEMPLATE_PROFILE_LOCATION = "profiles/base/base.json"

with open(TEMPLATE_PROFILE_LOCATION, 'r') as f:
    profile_json = json.load(f)


def deep_merge(dict1, dict2):
    my_merger = Merger(
        # pass in a list of tuple, with the
        # strategies you are looking to apply
        # to each type.
        [
            (list, ["override"]),
            (dict, ["merge"])
        ],
        # next, choose the fallback strategies,
        # applied to all other types:
        ["override"],
        # finally, choose the strategies in
        # the case where the types conflict:
        ["override"]
    )
    return my_merger.merge(dict1, dict2)

def create_result(profile_json, added_rules_json, grid_size, name):
    new_profile_json = deep_merge(profile_json, added_rules_json)
    os.mkdir(SAVE_LOCATION + name)
    start = time.time()
    result = run_profile_from_json(new_profile_json, grid_size, block_size, cell_size, False)
    end = time.time()

    def create_file(file_name, data):
        f = open(SAVE_LOCATION + name + "/" + file_name, "w+")
        f.write(data)
        f.close()

    create_file("log.txt", "total time taken: " + str(end - start))
    create_file("profile.json", json.dumps(new_profile_json))
    create_file("solutions.json", json.dumps({"solutions": result.logger.output_events()}))

    export(result.show(), SAVE_LOCATION +name + "/result.vox")
    export(color_connected_parts(result.show_adjacency_type("routing")), SAVE_LOCATION +name + "/routing.vox")
    export(color_connected_parts(result.show_adjacency_type("construction")), SAVE_LOCATION +name + "/construction.vox")
    export(color_connected_parts(result.show_adjacency_type("directconstruction")), SAVE_LOCATION +name + "/directconstruction.vox")


allconnected_experiments = [
    ({"allconnected": [
        {
    "type": "routing",
    "category": "routing",
    "level":1
  }
]},"only-all-1-connected"),
    ({"allconnected": [
        {
    "type": "routing",
    "category": "routing",
    "level":2
  }
]},"only-all-2-connected")
]

blobs_to_side = [
({  "blobstoside": [
    {
      "category": "built",
      "type": "directconstruction",
      "side": "-y"
    }
  ]}, "blobsonside-ybuiltdirectconstruction"),
]

cut_off = [
    ({"cutoff": [{"categories": ["routing"], "types": ["routing"]}]}, "routingcutoff")
]

blobs = [
    ({ "blobs": [{
        "type": "directconstruction",
        "category": "interior",
        "length": {"minDx": 0,
                   "maxDx": 6,
                   "minDy": 0,
                   "maxDy": 0,
                   "minDz": 0,
                   "maxDz": 6
                   }}]
    }, "blobsonefloor"),
    ({"blobs": [{
        "type": "directconstruction",
        "category": "interior",
        "length": {"minDx": 0,
                   "maxDx": 6,
                   "minDy": 0,
                   "maxDy": 1,
                   "minDz": 0,
                   "maxDz": 6
                   }}]
     }, "blobs2floors")
]

density = [
    (  {"density": {
    "void": -1,
    "interior":1
  }}, "densityinterior")
]

for experiment in product(*[[({}, "")] + e for e in [allconnected_experiments,
                                               blobs_to_side,
                                               blobs,
                                               density]]):

    combined_experiment = reduce(lambda agg, t: (deep_merge(agg[0], t[0]), agg[1] + "E" + t[1]), experiment, ({}, ""))
    try:
        print(combined_experiment[1])
        create_result(profile_json, combined_experiment[0], grid_size_one_block, combined_experiment[1] + "small")
        create_result(profile_json, combined_experiment[0], grid_size_horizontal, combined_experiment[1] + "medium")
    except Exception as e:
        raise e
        print(e)
        print(combined_experiment[1] + " failed.")

for experiment in product(*[[({}, "")] + e for e in [allconnected_experiments,
                                               blobs_to_side,
                                               blobs,
                                               density]]):

    combined_experiment = reduce(lambda agg, t: (deep_merge(agg[0], t[0]), agg[1] + "E" + t[1]), experiment, ({}, ""))
    try:
        print(combined_experiment[1])
        create_result(profile_json, combined_experiment[0], grid_size_horizontal_big, combined_experiment[1] + "horizontalbig")
        # create_result(profile_json, combined_experiment[0], grid_size_full, combined_experiment[1] + "full")
    except:
        print(combined_experiment[1] + " failed.")

for experiment in product(*[[({}, "")] + e for e in [allconnected_experiments,
                                               blobs_to_side,
                                               blobs,
                                               density]]):

    combined_experiment = reduce(lambda agg, t: (deep_merge(agg[0], t[0]), agg[1] + "E" + t[1]), experiment, ({}, ""))
    try:
        print(combined_experiment[1])
        # create_result(profile_json, combined_experiment[0], grid_size_horizontal_big, combined_experiment[1] + "horizontalbig")
        create_result(profile_json, combined_experiment[0], grid_size_full, combined_experiment[1] + "full")
    except:
        print(combined_experiment[1] + " failed.")
