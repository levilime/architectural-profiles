from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint
from run_utils.habitationresolver import habitation_resolver
from oldprofiles.profiles.minecraftmountainvillagepaper import MinecraftMountainVillage
from oldprofiles.util import get_indices
from solving.util import dimension_order
from voxels.magicavoxwrapper import visualize_voxel

class CustomConstraint(DeclarativeConstraints):
    def __init__(self):
        custom_constraint = DeclarativeConstraint(
        "custom constraint",
            ""
        )
        super().__init__([custom_constraint])

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_as_tuple = tuple(map(lambda key: cell_size[key], dimension_order))
habitation_profile = MinecraftMountainVillage(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22})
# habitation_profile = EmptyProfile(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22})


block_shape = {"x":4, "y":4, "z":4}
block_shape_as_tuple = tuple(map(lambda key: block_shape[key], dimension_order))
habitation_profile.add_rule(CustomConstraint())

result = habitation_resolver(habitation_profile, block_shape, cell_size, get_indices(1,1,2),
                             {(0,0,0):
                                 {
                                 #"filled_assignment":
                                     #{(0,0,0): True}
                                     #fill_diagonally_upwards(block_shape_as_tuple)
                             }}
                             )
visualize_voxel(result)
