from oldprofiles.habitationprofile import HabitationProfile
from oldprofiles.rulecombiner import combine_rules
from oldprofiles.rules.boundary.emptyboundarymatchignoredoor import EmptyBoundaryMatchIgnoreDoor
from oldprofiles.rules.construction.constructionunderbuildings import ConstructionUnderBuildings
from oldprofiles.rules.boundary.emptyboundarymatchignoreconstruction import EmptyBoundaryMatchIgnoreContruction
from oldprofiles.rules.boundary.emptyboundarymatchignoreroute import EmptyBoundaryMatchIgnoreRoute
from oldprofiles.rules.maximumvariety import MaximizeVariety
from oldprofiles.rules.building.nocorneradjacency import NoCornerAdjacency
from oldprofiles.rules.exterior.nofilledtiles import NoFilledTiles
from oldprofiles.rules.construction.rooffoundationrules import RoofFoundationRules
from oldprofiles.rules.boundary.emptyboundarymatch import EmptyBoundaryMatch
from oldprofiles.rules.routing.connectroomswithpaths import ConnectRoomsAndPaths
from oldprofiles.rules.routing.nostairs import NoStairs
from oldprofiles.rules.building.smallhouses import SmallHouses
from oldprofiles.rules.routing.routeinedge import RouteInEdge
from oldprofiles.tilecollections.minecraftconstruction import MineCraftConstruction
from oldprofiles.tilecombiner import combine_tilesets, materialize_tilesets
from oldprofiles.tilecollections.defaulttileset import DefaultTileSet
from oldprofiles.tilecollections.minecraftbuilding import MineCraftBuilding
from oldprofiles.tilecollections.minecraftpathway import MineCraftPathway

"""
Minecraft Water village

Water is a flat surface, therefore the water village has only one elevation level. Little houses build on
wooden beams are connected with small wooden paths with each other.
"""

class MinecraftWaterVillage(HabitationProfile):
    def __init__(self, cell_size, materialization):
        tiles = combine_tilesets(materialize_tilesets(materialization,
                                                      [DefaultTileSet,
                                                       MineCraftBuilding,
                                                       MineCraftPathway,
                                                       MineCraftConstruction
                                                       ]))
        rules = combine_rules([NoFilledTiles(),
                               RoofFoundationRules(),
                               NoCornerAdjacency(),
                               ConnectRoomsAndPaths(),
                               RouteInEdge(),
                               NoStairs(),
                               EmptyBoundaryMatch(),
                               EmptyBoundaryMatchIgnoreRoute(),
                               EmptyBoundaryMatchIgnoreContruction(),
                               EmptyBoundaryMatchIgnoreDoor(),
                               #PathToEmptyEdge(),
                               SmallHouses(),
                               ConstructionUnderBuildings(),
                               MaximizeVariety()
                               # BlockFloorIsFilled()
                               ])
        super().__init__("minecraft_water_village", tiles, rules, cell_size)



