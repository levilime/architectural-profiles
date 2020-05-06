import json

from run_utils.profileimporter import import_profile_from_file, import_examples_custom_location
from run_utils.runprofile import run_profile
from voxels.magicavoxwrapper import visualize_voxel

grid_size = {"x":2, "y":1, "z":1}
cell_size = {"x": 5, "y": 4, "z": 5}
block_size = {"x":3, "y":3, "z":3}
location = "evocativeexample/base"

def get_profile():
    return import_profile_from_file(location + "/base.json", "5x4x5x", (5,4,5), None,
                                    lambda profile_json: import_examples_custom_location(
                                        "examples", profile_json, location))

profile = get_profile()
exterior_routing_shape = list(filter(lambda x: x.category == "exterior", profile.shapes))[0]
interior_routing_shape = list(filter(lambda x: x.category == "interior", profile.shapes))[0]
exterior_routing_shape.max_bounding_box = (10,1,10)
exterior_routing_shape.min_bounding_box = (1,1,1)
interior_routing_shape.max_bounding_box = (5,1,5)
interior_routing_shape.min_bounding_box = (3,1,3)

with open(location + "/base.json", 'r') as f:
    profile_json = json.load(f)
output = run_profile(profile, grid_size, block_size, cell_size
                     ,import_examples_custom_location("reflections", profile_json, location)
                     ,import_examples_custom_location("antireflections", profile_json, location)
                     )
visualize_voxel(output.show())

