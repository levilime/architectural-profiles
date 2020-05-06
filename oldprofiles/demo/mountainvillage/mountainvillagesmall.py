from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint
from run_utils.habitationresolver import habitation_resolver
from oldprofiles.profiles.minecraftmountainvillage import MinecraftMountainVillage
from solving.util import dimension_order
from voxels.magicavoxwrapper import visualize_voxel


class BuildingAndPathConnected(DeclarativeConstraints):


    # the valid blocksize for this demo is x=3, y=3,z=5
    def __init__(self):
        building = DeclarativeConstraint(
        "A valid building with a path",
            #"assign(1,1,2,front_wall_with_window_boundary1)."
            #"assign(3,1,2,front_wall_with_window_boundary3)."
            # "1 {assign(0,0,Z, ID):cell(0, 0, Z), texturegroup(ID, stairs), direction(ID, 3)}.\n"
            # "assign(1,1,0, floorroof).\n"
            # "assign(0,1,2, roof).\n"
            #"assign(0,0,0, floorroof).\n"
            #"assign(2,1,2, stairs3).\n"
            #"assign(1,0,0, stairs3).\n"
            #"assign(0,0,1, stairs0).\n"
            # "assign(2,1,3, stairs3).\n"
            #"4 {assign(X,1,Z, ID):cell(X, 1, Z), category(ID, building)}.\n"

            #"assign(1,0,0, stairs3).\n"
            #"assign(0,0,1, stairs0).\n"
            #"assign(1,0,1, corner3).\n"
            #"assign(0,0,1, stairs0).\n"
            #"assign(0,0,1, stairs1).\n"
            #"assign(0,0,0, corner2).\n"
            #"assign(1,0,0, stairs2).\n"
            # "level(Y) :- cell(X,Y,Z)."
            #"1 {assign(X,Y,Z, ID):cell(X, Y, Z), texturegroup(ID, stairs)} :- level(Y)."
             "assign(0, 0, 0,front_wall_with_door_opening2)."
             "assign(0, 0, 1, front_wall0)."
            #"assign(0, 0, 0, stairs2)."
            #"assign(0, 0, 1, stairs0)."

        )
        super().__init__([building])

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_as_tuple = tuple(map(lambda key: cell_size[key], dimension_order))
habitation_profile = MinecraftMountainVillage(cell_size_as_tuple, {"building": 7, "path": 15, "construction": 22})


block_shape = {"x":1, "y":1, "z":2}
block_shape_as_tuple = tuple(map(lambda key: block_shape[key], dimension_order))
habitation_profile.add_rule(BuildingAndPathConnected())

# result = habitation_resolver(habitation_profile, block_shape, cell_size, [(0,0,0), (0,1,0)],
#                              {(0,0,0): {
#                                  "filled_assignment":
#                                     fill_block_floor(block_shape_as_tuple, None)
#                              }}
#                              #{}
#                              )

result = habitation_resolver(habitation_profile, block_shape, cell_size, [(0,0,0)],
                             # {(0,0,0): {
                             #     "void_assignment":
                             #         {(4,4,4): True}
                             # }}
                             {}
                             )
visualize_voxel(result)
