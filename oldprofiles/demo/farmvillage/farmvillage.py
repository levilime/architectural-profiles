from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint
from run_utils.habitationresolver import habitation_resolver
from oldprofiles.profiles.minecraftfarmvillage import MinecraftFarmVillage
from oldprofiles.util import fill_block_floor, get_indices
from solving.util import dimension_order


class CustomConstraint(DeclarativeConstraints):
    def __init__(self):
        custom_constraint = DeclarativeConstraint(
        "custom constraint",
            #"6 {assign(X,Y,Z, ID):cell(X, Y, Z), category(ID, interior)}.\n"
            #"1 {assign(X,1,Z, ID):cell(X, 1, Z), texturegroup(ID, floorroof)}."
            #"overrideempty(void)."
            ""
        )
        super().__init__([custom_constraint])

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_as_tuple = tuple(map(lambda key: cell_size[key], dimension_order))
habitation_profile = MinecraftFarmVillage(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22})
# habitation_profile = EmptyProfile(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22})


block_shape = {"x":5, "y":3, "z":5}
block_shape_as_tuple = tuple(map(lambda key: block_shape[key], dimension_order))
habitation_profile.add_rule(CustomConstraint())

result = habitation_resolver(habitation_profile, block_shape, cell_size, get_indices(1,1,2),
                             {
                                 (0,0,0):
                                 {
                                 "filled_assignment":
                                     fill_block_floor(block_shape_as_tuple)
                             },
                                 # (0, 0, 1):
                                 #     {
                                 #         "filled_assignment":
                                 #             fill_block_floor(block_shape_as_tuple)
                                 #     },
                                 #
                                 #     (1, 0, 0):
                                 #         {
                                 #             "filled_assignment":
                                 #                 fill_block_floor(block_shape_as_tuple)
                                 #         },
                                 #     (1, 0, 1):
                                 #         {
                                 #             "filled_assignment":
                                 #                 fill_block_floor(block_shape_as_tuple)
                                 #         }
                             }

                             )
# visualize_voxel(result)
