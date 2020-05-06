import json
import sys
import os

from oldprofiles.util import fill_diagonally_upwards, fill_all, fill_block_floor, get_indices, fill_randomely
from profileimporter import import_profile, materialize_profile
from habitationresolver import habitation_resolver
from reflectexample import reflects_examples
from runprofile import run_profile_from_file
from solving.util import dimensional_dict_to_tuple
from voxels.magicavoxwrapper import visualize_voxel, export

profile_location = sys.argv[1]
block_size_x = int(sys.argv[2])
block_size_y = int(sys.argv[3])
block_size_z = int(sys.argv[4])
grid_x_dim = int(sys.argv[6])
grid_y_dim = int(sys.argv[7])
grid_z_dim = int(sys.argv[8])
save_location = sys.argv[5]

cell_size = {"x": 5, "y": 4, "z": 5}
block_size = {"x":block_size_x, "y":block_size_y, "z":block_size_z}
grid_size = {"x": grid_x_dim, "y": grid_y_dim, "z": grid_z_dim}
result = run_profile_from_file(profile_location, grid_size, block_size, cell_size)
os.makedirs("/".join(sys.argv[5].split("/")[:-1]), exist_ok=True)
export(result.show(), save_location)
