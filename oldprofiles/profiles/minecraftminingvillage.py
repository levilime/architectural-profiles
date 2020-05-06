from oldprofiles.habitationprofile import HabitationProfile
from oldprofiles.rulecombiner import combine_rules
from oldprofiles.rules.boundary.emptyboundarymatch import EmptyBoundaryMatch
from oldprofiles.rules.boundary.emptyboundarymatchignoredoor import EmptyBoundaryMatchIgnoreDoor
from oldprofiles.rules.building.connectrooms import ConnectRooms
from oldprofiles.rules.building.maximizeinside import MaximizeInside
from oldprofiles.rules.building.maximizeinterior import MaximizeInterior
from oldprofiles.rules.building.roofonlydirectlyabovebuilding import RoofOnlyDirectlyAboveBuilding
from oldprofiles.rules.maximumvariety import MaximizeVariety
from oldprofiles.rules.mining.filledconnectedbuildings import FilledConnectedBuildings
from oldprofiles.rules.notiletemplate import NoTileTemplateUsage
from oldprofiles.rules.routing.connectroomswithpaths import ConnectRoomsAndPaths
from oldprofiles.rules.construction.constructionunderbuildings import ConstructionUnderBuildings
from oldprofiles.rules.boundary.emptyboundarymatchignoreconstruction import EmptyBoundaryMatchIgnoreContruction
from oldprofiles.rules.boundary.emptyboundarymatchignoreroute import EmptyBoundaryMatchIgnoreRoute
from oldprofiles.rules.building.nocorneradjacency import NoCornerAdjacency
from oldprofiles.rules.exterior.nofilledtiles import NoFilledTiles
from oldprofiles.rules.construction.rooffoundationrules import RoofFoundationRules
from oldprofiles.rules.routing.routeinedge import RouteInEdge
from oldprofiles.rules.building.smallhouses import SmallHouses
from oldprofiles.rules.smallbuilding.onlysmallbuilding import OnlySmallBuilding
from oldprofiles.tilecollections.filltestset import FillTestSet
from oldprofiles.tilecollections.minecraftbasicbuilding import MineCraftBasicBuilding
from oldprofiles.tilecollections.minecraftconstruction import MineCraftConstruction
from oldprofiles.tilecollections.minecraftsmallbuilding import MineCraftSmallBuilding
from oldprofiles.tilecombiner import combine_tilesets, materialize_tilesets
from oldprofiles.tilecollections.defaulttileset import DefaultTileSet
from oldprofiles.tilecollections.minecraftbuilding import MineCraftBuilding
from oldprofiles.tilecollections.minecraftpathway import MineCraftPathway


class MinecraftMiningVillage(HabitationProfile):
    def __init__(self, cell_size, materialization):
        tiles = combine_tilesets(materialize_tilesets(materialization,
                                                      [DefaultTileSet,
                                                       MineCraftBasicBuilding,
                                                       MineCraftSmallBuilding,
                                                       MineCraftPathway
                                                          #FillTestSet
                                                       ]))
        rules = combine_rules([NoFilledTiles(),
                               # RoofFoundationRules(),
                               # NoCornerAdjacency(),
                               NoTileTemplateUsage(),
                               OnlySmallBuilding(),
                               # ConnectRoomsAndPaths(),
                               # ConnectRooms(),
                               # RouteInEdge(),
                               # PathToEmptyEdge(),
                               SmallHouses(),
                               # MaximizeInterior(),
                               FilledConnectedBuildings(),
                               MaximizeVariety(),
                               # BlockFloorIsFilled()
                               # RoofOnlyDirectlyAboveBuilding(),
                               ])
        super().__init__("minecraft_mining_village", tiles, rules, cell_size)



