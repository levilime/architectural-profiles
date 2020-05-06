from itertools import product

from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint
from run_utils.habitationresolver import habitation_resolver
from oldprofiles.profiles.minecraftwatervillage import MinecraftWaterVillage
from solving.util import dimension_order
from voxels.magicavoxwrapper import visualize_voxel


class BuildingAndPathConnected(DeclarativeConstraints):


    # the valid blocksize for this demo is x=3, y=3,z=5
    def __init__(self):
        building = DeclarativeConstraint(
        "A valid building with a path",
            #"assign(1,1,2,front_wall_with_window_boundary1)."
            #"assign(3,1,2,front_wall_with_window_boundary3)."
            "assign(1,1,2,front_wall_with_door_opening_boundary1)."
            "assign(3,1,2,front_wall_with_door_opening_boundary3)."
        )
        super().__init__([building])

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_as_tuple = tuple(map(lambda key: cell_size[key], dimension_order))
habitation_profile = MinecraftWaterVillage(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22})
# load(profile, "voxels/" + profile + ".pickle",
#                       cell_size_as_tuple, cell_size_as_tuple)

block_shape = {"x":5, "y":3, "z":5}
block_shape_as_tuple = tuple(map(lambda key: block_shape[key], dimension_order))
# habitation_profile.add_rule(BuildingAndPathConnected())

result = habitation_resolver(habitation_profile, block_shape, cell_size, list(product(list(range(0,3)), [0], list(range(0,3)))),
                             {(0,0,0):
                                  {"filled_assignment":
                                       {}# fill_block_floor(block_shape_as_tuple)
                                   }})
visualize_voxel(result)
