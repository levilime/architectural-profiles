from functools import reduce
from subprocess import Popen, PIPE
import json
import shutil

from profileimporter import import_profile
from solving.util import merge_dicts, dimensional_dict_to_tuple
from tile.allconnected import AllConnected, AllConnectedPart
from tile.connectivity import Connectivities, Connectivity
from tile.density import Density

import time

python_location = "./venv/Scripts/python.exe"


def f(tileset, block_x, block_y, block_z, save_location, grid_x_dim, grid_y_dim, grid_z_dim):
    query = [python_location, "runprofilecl.py",
             tileset,
             str(block_x),
             str(block_y),
             str(block_z),
             save_location,
             str(grid_x_dim),
             str(grid_y_dim),
             str(grid_z_dim)]
    start = time.time()
    print(" ".join(query))
    p = Popen(query, stdin=PIPE, stdout=PIPE)
    output = p.stdout.readlines()
    f = open(save_location + ".log", "w+")
    end = time.time()
    time_taken = "total time taken: " + str(end - start)
    log = output + [time_taken]
    f.write("\n".join(map(str , log)))
    f.close()
    shutil.copyfile(tileset, save_location + ".json")
    print(log)

def transformed_profile(profile, profile_transformation, save_location):
    serialized_profile = json.dumps(merge_dicts(profile, profile_transformation))
    f = open(save_location, "w+")
    f.write(serialized_profile)
    f.close()


def adjust_profile(profile, connectivities, all_connected, density):
    return reduce(merge_dicts, [e.serialize() for e in [connectivities, all_connected, density]], profile)


cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_t = dimensional_dict_to_tuple(cell_size)
profile_location = "profiles/mountaintownblank.json"
edited_profile = "mountaintownedited.json"
with open(profile_location, 'r') as rr:
    profile_json = json.load(rr)
base_profile = import_profile(profile_json, '5x4x5x', cell_size_t)

# ### START MORE STAIRS
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 1)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
#     Connectivity("directconstruction", ["support"], ["built"], ["built"], (0,3)),
#     Connectivity("directconstruction", ["support"], ["built"], ["interior"], (0,3))
# ]
# density = Density({})
# density.density = {"filled": -2, "void": -2, "elevate": 1, "interior": -1}
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintownmorestairs.vox", 2, 1, 2)
# ### END MORE STAIRS
#
# ### START LESS STAIRS
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 1)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
#     Connectivity("directconstruction", ["support"], ["built"], ["built"], (0,3)),
#     Connectivity("directconstruction", ["support"], ["built"], ["interior"], (0,3))
# ]
# density = Density({"filled": -2, "void": -2, "elevate": -1, "interior": 1})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintownlessstairs.vox", 2, 1, 2)
# ### END LESS STAIRS

### START SMALL BUILDINGS
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 1)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
#     Connectivity("directconstruction", ["support"], ["built"], ["built"], (0,3)),
#     Connectivity("directconstruction", ["support"], ["built"], ["interior"], (0,1))
# ]
# density = Density({"filled": -2, "void": -2})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintownsmallestbuilding.vox", 2, 1, 2)
# ### END SMALL BUILDINGS
#
# ### START SMALL BUILDINGS
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 1)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
#     Connectivity("directconstruction", ["support"], ["built"], ["built"], (0,3)),
#     Connectivity("directconstruction", ["support"], ["built"], ["interior"], (1,1))
# ]
# density = Density({"filled": -2, "void": -2})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintownsmallbuilding.vox", 2, 1, 2)
# ### END SMALL BUILDINGS
#
# ### START LARGE BUILDINGS
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 1)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
#     Connectivity("directconstruction", ["support"], ["built"], ["built"], (0,3)),
#     Connectivity("directconstruction", ["support"], ["built"], ["interior"], (2,3))
# ]
# density = Density({"filled": -2, "void": -2})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintownsmallbuilding.vox", 2, 1, 2)
# ### END LARGE BUILDINGS
#
# ### START ANY SUPPORT
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 1)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
#     Connectivity("construction", ["support"], ["built"], ["built"], (0,10)),
# ]
# density = Density({"filled": -2, "void": -2})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintowncubeanysupportstraight.vox", 2, 1, 2)
# ### START CUBE CITY

### START CUBE CITY FLOATING SUPPORT ANY DIRECTION 1
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 1)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
#     Connectivity("construction", ["support"], ["built"], ["built"], (0,10)),
# ]
# density = Density({"filled": -2, "void": -2})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintowncubeanysupport1.vox", 3, 3, 3)
# ### START CUBE CITY
#
# ### START CUBE CITY FLOATING SUPPORT ANY DIRECTION 2
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 2)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
# ]
# density = Density({"filled": -2, "void": -2})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintowncubeanysupport2.vox", 3, 3, 3)
# ### END CUBE CITY
#
# ### START CUBE CITY FLOATING CONNECTIVITY 1
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 1)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
# ]
# density = Density({"filled": -2, "void": -2})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintowncube1.vox", 3, 3, 3)
# ### START CUBE CITY
#
# ### START CUBE CITY FLOATING CONNECTIVITY 2
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 2)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
# ]
# density = Density({"filled": -2, "void": -2})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintowncube2.vox", 3, 3, 3)
# ### START CUBE CITY
#
# ### START CUBE CITY SUPPORTED 1
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 1)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
#     Connectivity("directconstruction", ["support"], ["built"], ["built"], (0,3)),
#     Connectivity("directconstruction", ["support"], ["built"], ["interior"], (0,20))
# ]
# density = Density({"filled": -2, "void": -2})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintowncubesupport1.vox", 3, 3, 3)
# ### START CUBE CITY
#
# ### START CUBE CITY SUPPORTED 2
# allconnected = AllConnected([])
# allconnected.all_connected = [AllConnectedPart("routing", "routing", 2)]
# connectivities = Connectivities({})
# connectivities.connectivities = [
#     Connectivity("directconstruction", ["support"], ["built"], ["built"], (0,3)),
#     Connectivity("directconstruction", ["support"], ["built"], ["interior"], (0,20))
# ]
# density = Density({"filled": -2, "void": -2})
#
# adjusted_profile = adjust_profile(profile_json, connectivities, allconnected, density)
# transformed_profile(adjusted_profile, {}, edited_profile)
# f(edited_profile, 4, 4, 4, "results/mountaintowncubesupport1.vox", 3, 3, 3)
# ### START CUBE CITY



