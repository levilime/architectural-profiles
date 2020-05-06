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
             #"assign(0,1,0,corner_boundary2).\n"
             #"assign(0,0,0, pillars_quarter2).\n"
            # "assign(1,2,1,roof).\n"
            # "assign(1,1,1,inside).\n"
            #"assign(1,0,1,pillars).\n"
          # "assign(1,0,1,pillars).\n"
        #"assign(1, 1, 0, front_wall_with_window_boundary2).\n"
        #"assign(1, 1, 2, front_wall_with_window_boundary0).\n"
        #"assign(2, 1, 1, front_wall_with_window_boundary3).\n"
         "assign(2, 2, 2, front_wall_with_door_opening_boundary1).\n"
        #     "assign(1,0,2, pillars_half0).\n"
        #     "assign(1,0,0, pillars_half2).\n"
        )
        super().__init__([building])

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_as_tuple = tuple(map(lambda key: cell_size[key], dimension_order))
habitation_profile = MinecraftMiningVillage(cell_size_as_tuple, {"building": 7, "path":15, "construction": 22})
# load(profile, "voxels/" + profile + ".pickle",
#                       cell_size_as_tuple, cell_size_as_tuple)

#habitation_profile.add_rule(BuildingAndPathConnected())

result = habitation_resolver(habitation_profile, {"x":5, "y":3, "z":5}, cell_size, [(0,0,0), (1,0,0), (0,0,1), (1,0,1)],
                             {(0,0,0):
                                  {"filled_assignment":
                                       {}
                                   }})
visualize_voxel(result)
