from oldprofiles.habitationprofile import HabitationProfile
from oldprofiles.rulecombiner import combine_rules
from oldprofiles.rules.boundary.emptyboundarymatch import EmptyBoundaryMatch
from oldprofiles.rules.boundary.emptyboundarymatchignoredoor import EmptyBoundaryMatchIgnoreDoor
from oldprofiles.rules.castle.castlewalls import CastleWalls
from oldprofiles.rules.maximumvariety import MaximizeVariety
from oldprofiles.rules.routing.connectroomswithpaths import ConnectRoomsAndPaths
from oldprofiles.rules.boundary.emptyboundarymatchignoreconstruction import EmptyBoundaryMatchIgnoreContruction
from oldprofiles.rules.boundary.emptyboundarymatchignoreroute import EmptyBoundaryMatchIgnoreRoute
from oldprofiles.rules.building.nocorneradjacency import NoCornerAdjacency
from oldprofiles.rules.exterior.nofilledtiles import NoFilledTiles
from oldprofiles.tilecombiner import combine_tilesets, materialize_tilesets
from oldprofiles.tilecollections.defaulttileset import DefaultTileSet
from oldprofiles.tilecollections.minecraftcastle import MineCraftCastle
from oldprofiles.tilecollections.minecraftpathway import MineCraftPathway


class MinecraftCastle(HabitationProfile):
    def __init__(self, cell_size, materialization):
        tiles = combine_tilesets(materialize_tilesets(materialization,
                                                      [DefaultTileSet,
                                                       MineCraftCastle,
                                                       MineCraftPathway,
                                                       ]))
        rules = combine_rules([NoFilledTiles(),
                               NoCornerAdjacency(),
                               ConnectRoomsAndPaths(),
                               CastleWalls(),
                               #RouteInEdge(),
                               EmptyBoundaryMatch(),
                               EmptyBoundaryMatchIgnoreRoute(),
                               EmptyBoundaryMatchIgnoreContruction(),
                               EmptyBoundaryMatchIgnoreDoor(),
                               # PathToEmptyEdge(),
                               # MaximizeInside(),
                               MaximizeVariety()
                               # BlockFloorIsFilled()
                               ])
        super().__init__("minecraft_castle", tiles, rules, cell_size)

# MinecraftMiningVillage((5,4,5), {}).export_visualization()



