from constraints.declarativeconstraint import DeclarativeConstraints, DeclarativeConstraint
from constraints.volumeconstraints import VolumeConstraints
from run_utils.habitationresolver import habitation_resolver
from oldprofiles.habitationprofile import HabitationProfile
from oldprofiles.rulecombiner import combine_rules
from oldprofiles.rules.building.nocorneradjacency import NoCornerAdjacency
from oldprofiles.rules.exterior.nofilledtiles import NoFilledTiles
from oldprofiles.rules.construction.rooffoundationrules import RoofFoundationRules
from oldprofiles.tilecombiner import combine_tilesets
from oldprofiles.tilecollections.defaulttileset import DefaultTileSet
from oldprofiles.tilecollections.minecraftbuilding import MineCraftBuilding
from oldprofiles.tilecollections.minecraftpathway import MineCraftPathway
from solving.util import dimension_order
from voxels.goxelviewer import visualize_voxel


class OnlyPathAndDoor(DeclarativeConstraints):
    def __init__(self):
        # x = 1, y = 1, z = 2
        # doorandpath = DeclarativeConstraint(
        # "Door and path connected",
        # "assign(0,0,0, front_wall_with_door_opening_boundary0).\n"
        # "assign(0,0,1, x_path).\n"
        # )

        doorandpath = DeclarativeConstraint(
        "Door and path connected",
        "assign(0,1,0, front_wall_with_door_opening_boundary0).\n"
        #"assign(0,1,1, x_path).\n"
        )
        super().__init__([doorandpath])

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_as_tuple = tuple(map(lambda key: cell_size[key], dimension_order))

tiles_and_rules = {"tiles": combine_tilesets([DefaultTileSet, MineCraftBuilding, MineCraftPathway]),
                                  "rules": combine_rules([NoFilledTiles(),
                                                          RoofFoundationRules(),
                                                          #ConnectRoomsAndPaths(),
                                                          #MinimizeEmptySpace(),
                                                          NoCornerAdjacency()
                                                          ])}

tiles = VolumeConstraints(tiles_and_rules["tiles"](cell_size_as_tuple, cell_size_as_tuple)
            .realized_textures).realized_textures
rules = tiles_and_rules["rules"]
profile = "minecraft_village"
habitation_profile = HabitationProfile(profile, tiles, rules)

habitation_profile.add_rule(OnlyPathAndDoor())

result = habitation_resolver(habitation_profile, {"x":1, "y":2, "z":2}, cell_size, [(0,0,0)])
visualize_voxel(result)
