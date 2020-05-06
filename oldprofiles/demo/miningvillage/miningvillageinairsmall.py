from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint
from run_utils.habitationresolver import habitation_resolver
from oldprofiles.profiles.minecraftminingvillage import MinecraftMiningVillage
from solving.util import dimension_order
from voxels.magicavoxwrapper import visualize_voxel


class BuildingAndPathConnected(DeclarativeConstraints):


    # the valid blocksize for this demo is x=3, y=3,z=5
    def __init__(self):
        building = DeclarativeConstraint(
        "A valid building with a path",
            #"assign(1,1,2,front_wall_with_window_boundary1)."
            #"assign(3,1,2,front_wall_with_window_boundary3)."
            "1 {assign(X,Y,Z, ID):cell(X, Y, Z), category(ID, building)}.\n"
        )
        super().__init__([building])

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_as_tuple = tuple(map(lambda key: cell_size[key], dimension_order))
habitation_profile = MinecraftMiningVillage(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22})
# load(profile, "voxels/" + profile + ".pickle",
#                       cell_size_as_tuple, cell_size_as_tuple)

c = 3
block_shape = {"x":4, "y":4, "z":4}
block_shape_as_tuple = tuple(map(lambda key: block_shape[key], dimension_order))
habitation_profile.add_rule(BuildingAndPathConnected())

# result = habitation_resolver(habitation_profile, block_shape, cell_size, [(0,0,0), (0,1,0)],
#                              {(0,0,0): {
#                                  "filled_assignment":
#                                     fill_block_floor(block_shape_as_tuple, None)
#                              }}
#                              #{}
#                              )

result = habitation_resolver(habitation_profile, block_shape, cell_size, [(0,0,0), (0,1,0)],
                             # {(0,0,0): {
                             #     "filled_assignment":
                             #        fill_block_floor(block_shape_as_tuple, int(4 ** 2 / 2))
                             # }}
                             {}
                             )
visualize_voxel(result)
