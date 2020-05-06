import json
import os
import pickle
import time

from expressiverange import plot_expressive_range
from profileimporter import import_reflection_shapes, import_profile
from runprofile import run_profile_from_file
from shapegenerator import solve_input_without_shapes
from solving.blocksignature import remove_duplicate_blocks
from solving.blocksolver import create_block_from_result
from solving.util import dimensional_dict_to_tuple
from voxels.magicavoxwrapper import export, visualize_voxel

grid_size = {"x":1, "y":1, "z":1}
cell_size = {"x": 5, "y": 4, "z": 5}
block_size = {"x": 5, "y":5, "z":5}

cell_size_t = dimensional_dict_to_tuple(cell_size)

with open("profiles/base.json", 'r') as f:
    profile_json = json.load(f)

profile = import_profile(profile_json, '5x4x5x', cell_size_t)

time_start = time.clock()
# put solving contraption here
solution = solve_input_without_shapes(block_size, profile, cell_size, 1000)
# end
time_elapsed = (time.clock() - time_start)
print(time_elapsed)
unique_blocks = remove_duplicate_blocks((create_block_from_result(solution, profile, cell_size)
                                         for solution in solution.solutions))

# plot_expressive_range(unique_blocks, ["void", "flatsurface"], profile)

directory = "unconstrainedshapes"
if not os.path.exists(directory):
    os.mkdir(directory)
for i, result in enumerate(unique_blocks):
    print("exporting")
    export(result.show(), f"{directory}/result{str(i)}.vox")
