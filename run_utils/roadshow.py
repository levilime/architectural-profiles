import json
import os
import time
from functools import reduce
from itertools import product

from deepmerge import Merger

from run_experiments import deep_merge, create_result
from runprofile import run_profile_from_file, run_profile_from_json
from solving.util import  dimensional_dict_to_tuple, color_connected_parts, merge_dicts
from voxels.magicavoxwrapper import export
grid_size_horizontal = {"x":2, "y":1, "z":2}
grid_size_horizontal_big = {"x":3, "y":1, "z":3}
grid_size_full = {"x":3, "y":3, "z":3}
cell_size = {"x": 5, "y": 4, "z": 5}
block_size = {"x":3, "y":3, "z":3}

# grid_size_t = dimensional_dict_to_tuple(grid_size)
# cell_size_t = dimensional_dict_to_tuple(cell_size)
# block_size_t = dimensional_dict_to_tuple(block_size)

SAVE_LOCATION = "experiments/"
TEMPLATE_PROFILE_LOCATION = "profiles/mountaintowntemplate.json"

with open(TEMPLATE_PROFILE_LOCATION, 'r') as f:
    profile_json = json.load(f)

small_village = [
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
]}, "")
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
        create_result(profile_json, combined_experiment[0], grid_size_full, combined_experiment[1] + "full")
    except:
        print(combined_experiment[1] + " failed.")
