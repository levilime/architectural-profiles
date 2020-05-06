from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint
from run_utils.habitationresolver import habitation_resolver
from oldprofiles.profiles.minecraftcastle import MinecraftCastle
from oldprofiles.util import fill_block_floor
from solving.util import dimension_order
from voxels.magicavoxwrapper import visualize_voxel


class BuildingAndPathConnected(DeclarativeConstraints):


    # the valid blocksize for this demo is x=3, y=3,z=5
    def __init__(self):
        building = DeclarativeConstraint(
        "there must be at least one castle tile",
            "1 {assign(X,Y,Z, ID):cell(X, Y, Z), category(ID, fortified)}.\n"
            "assign(0,1,1, double_wall_gate1).\n"
            "assign(0,1,0, double_wall_under1).\n"
            "assign(0,1,2, double_wall_under1).\n"
        )
        super().__init__([building])

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_as_tuple = tuple(map(lambda key: cell_size[key], dimension_order))
habitation_profile = MinecraftCastle(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22})
# load(profile, "voxels/" + profile + ".pickle",
#                       cell_size_as_tuple, cell_size_as_tuple)

c = 5
block_shape = {"x":1, "y":4, "z":3}
block_shape_as_tuple = tuple(map(lambda key: block_shape[key], dimension_order))
habitation_profile.add_rule(BuildingAndPathConnected())

result = habitation_resolver(habitation_profile, block_shape, cell_size, [(0,0,0)],
                             {(0,0,0):
                                  {"filled_assignment":
                                    fill_block_floor(block_shape_as_tuple)
                                   }}
                                                                                         # {}

                             )
visualize_voxel(result)
