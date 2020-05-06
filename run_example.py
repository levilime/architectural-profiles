from run_utils.runprofile import run_profile_from_file
from solving.util import color_connected_parts
from voxels.magicavoxwrapper import visualize_voxel, export

grid_size = {"x":1, "y":1, "z":1}
cell_size = {"x": 5, "y": 4, "z": 5}
block_size = {"x": 5, "y":4, "z":5}

result = run_profile_from_file("profiles/base/base.json", grid_size, block_size, cell_size, False, {}, 0)
export(result.show(), "result.vox")
visualize_voxel(result.show())
routing = color_connected_parts(result.show_adjacency_type("routing"))
visualize_voxel(color_connected_parts(result.show_adjacency_type("routing")))
export(routing, "routing.vox")
visualize_voxel(result.show_adjacency_type("construction"))



