import pickle

from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint
from run_utils.habitationresolver import habitation_resolver
from oldprofiles.profiles.emptyprofile import EmptyProfile
from oldprofiles.profiles.minecraftfarmvillage import MinecraftFarmVillage
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
habitation_profile = MinecraftFarmVillage(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22})
# habitation_profile = EmptyProfile(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22})


block_shape = {"x":4, "y":4, "z":4}
block_shape_as_tuple = tuple(map(lambda key: block_shape[key], dimension_order))
habitation_profile.add_rule(CustomConstraint())
with open("testmetadata.pickle", "rb") as f:
    metadata = pickle.load(f)

result = habitation_resolver(EmptyProfile(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22}),
                             block_shape, cell_size, list(metadata),
                             metadata
                             )
visualize_voxel(result)



result = habitation_resolver(habitation_profile, block_shape, cell_size, [(0,0,0), (0,1,0), (0,0,1), (0,1,1)],
                             metadata
                             )
visualize_voxel(result)
