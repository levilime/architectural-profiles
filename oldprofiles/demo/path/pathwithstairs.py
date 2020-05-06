import os

from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint
from run_utils.habitationresolver import habitation_resolver
from solving.util import dimension_order
from voxels.load_habitation_profile import load
from voxels.goxelviewer import visualize_voxel


class PathWithStairs(DeclarativeConstraints):


    # the valid blocksize for this demo is x=3, y=3,z=5
    def __init__(self):
        stairs = DeclarativeConstraint(
        "A valid building with a path",
        "assign(0,0,0, stairs0).\n"
        #"assign(0,1,1, straight_path0).\n"
        "assign(0,1,1, stairs0).\n"
        # "assign(0,2,2, stairs0).\n"
        # "assign(1,1,3, x_path).\n"
        )
        super().__init__([stairs])

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_as_tuple = tuple(map(lambda key: cell_size[key], dimension_order))
profile = "minecraft_pathway"

habitation_profile = load(profile, os.path.join("voxels", profile + ".pickle"),
                          cell_size_as_tuple, cell_size_as_tuple)

habitation_profile.add_rule(PathWithStairs())

result = habitation_resolver(habitation_profile, {"x":1, "y":1, "z":3}, cell_size, [(0,0,0)])
visualize_voxel(result)
