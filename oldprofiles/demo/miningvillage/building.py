import os

from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint
from run_utils.habitationresolver import habitation_resolver
from solving.util import dimension_order
from voxels.load_habitation_profile import load
from voxels.magicavoxwrapper import visualize_voxel


class BuildingAndPathConnected(DeclarativeConstraints):


    # the valid blocksize for this demo is x=3, y=3,z=5
    def __init__(self):
        building = DeclarativeConstraint(
        "A valid building with a path",
        ""
            #"assign(0,1,0,corner_boundary0).\n"
        # "assign(0,1,0,roof)."
        "assign(1, 1, 0, front_wall_with_window_boundary2).\n"
        "assign(1, 1, 2, front_wall_with_window_boundary0).\n"
        "assign(2, 1, 1, front_wall_with_window_boundary3).\n"
        "assign(0, 1, 1, front_wall_with_door_opening_boundary1).\n"
        # "assign(0, 1, 1, front_wall_with_window_boundary1).\n"
            "assign(1,1,1,inside).\n"
        #"assign(1, 2, 1, roof).\n"

        #"assign(0,1,0, inside).\n"

        # #"assign(2,2,1, roof).\n"
        # "assign(2,1,2, inside).\n"
        # #"assign(2,0,1, foundation).\n"
        # #"assign(1,1,3, front_wall_with_door_opening_boundary0).\n"
        # #"assign(1,1,1, front_wall_with_door_opening_boundary2).\n"
        # #"assign(1,1,0, straight_path0).\n"
        # #"assign(1,1,4, straight_path0).\n"
        # #"assign(1,1,0, straight_path0).\n"
        # "assign(0,0,0, filled_space).override(0,0,0).\n"
        )
        super().__init__([building])

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_as_tuple = tuple(map(lambda key: cell_size[key], dimension_order))
profile = "minecraft_village_not_connected"

habitation_profile = load(profile, os.path.join("voxels",  profile + ".pickle"),
                          cell_size_as_tuple, cell_size_as_tuple)

habitation_profile.add_rule(BuildingAndPathConnected())

result = habitation_resolver(habitation_profile, {"x":3, "y":3, "z":3}, cell_size, [(0,0,0)],
                             {(0,0,0):
                                  {"filled_assignment":
                                       {
                                           (0, 0, 0): True,
                                        (1, 0, 1): True,
                                        (0, 0, 1): True,
                                        (1, 0, 0): True,
                                        (2, 0, 2): True,
                                        (1, 0, 2): True,
                                        (2, 0, 1): True,
                                        (2, 0, 0): True,
                                        (0, 0, 2): True
                                        }
                                   }})
visualize_voxel(result)
