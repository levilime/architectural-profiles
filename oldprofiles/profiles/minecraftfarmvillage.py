from oldprofiles.habitationprofile import HabitationProfile
from oldprofiles.rulecombiner import combine_rules
from oldprofiles.rules.boundary.emptyboundarymatch import EmptyBoundaryMatch
from oldprofiles.rules.boundary.emptyboundarymatchignoredoor import EmptyBoundaryMatchIgnoreDoor
from oldprofiles.rules.boundary.emptyboundaryonlyinterior import ExemptAllBoundaryExceptInterior
from oldprofiles.rules.building.connectrooms import ConnectRooms
from oldprofiles.rules.building.housesperiphery import HousesPeriphery
from oldprofiles.rules.building.maximizeinside import MaximizeInside
from oldprofiles.rules.building.maximizeinterior import MaximizeInterior
from oldprofiles.rules.building.onlyonebuildinglevel import OnlyOneBuildingLevel
from oldprofiles.rules.building.roofonlydirectlyabovebuilding import RoofOnlyDirectlyAboveBuilding
from oldprofiles.rules.exterior.hardconstraintfilledtilesinoverride import HardConstraintFilledTilesinOverride
from oldprofiles.rules.exterior.maximizefilledtilesinoverride import MaximizeFilledTilesinOverride
from oldprofiles.rules.exterior.minimizefillednotoverriden import MinimizeFilledNotTilesOverriden
from oldprofiles.rules.maximumvariety import MaximizeVariety
from oldprofiles.rules.mountainvillage.buildingsnotbuiltonair import BuildingsNotBuiltOnAir
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
from oldprofiles.tilecollections.filltestset import FillTestSet
from oldprofiles.tilecollections.minecraftbasicbuilding import MineCraftBasicBuilding
from oldprofiles.tilecollections.minecraftconstruction import MineCraftConstruction
from oldprofiles.tilecollections.minecraftmountainvillage import MineCraftMountainVillage
from oldprofiles.tilecollections.minecraftsmallbuilding import MineCraftSmallBuilding
from oldprofiles.tilecombiner import combine_tilesets, materialize_tilesets
from oldprofiles.tilecollections.defaulttileset import DefaultTileSet
from oldprofiles.tilecollections.minecraftbuilding import MineCraftBuilding
from oldprofiles.tilecollections.minecraftpathway import MineCraftPathway


class MinecraftFarmVillage(HabitationProfile):
    def __init__(self, cell_size, materialization):
        tiles = combine_tilesets(materialize_tilesets(materialization,
                                                      [DefaultTileSet,
                                                       MineCraftBasicBuilding,
                                                       MineCraftSmallBuilding,
                                                       MineCraftMountainVillage,
                                                       # MineCraftPathway
                                                       ]))
        rules = combine_rules([
                                # MountainousTerrain(),
                                ConnectRoomsAndPaths(),
                                ConnectRooms(),
                                MaximizeVariety(),
                                NoTileTemplateUsage(),
                                BuildingsNotBuiltOnAir(),
                                # NoFilledTiles(),
                                # SmallHouses(),
                                HousesPeriphery(),
                                EmptyBoundaryMatch(),
                                ExemptAllBoundaryExceptInterior(),
                                OnlyOneBuildingLevel(),
                                # RoofOnlyDirectlyAboveBuilding(),
                                MinimizeFilledNotTilesOverriden(),
                                MaximizeFilledTilesinOverride(),
                                # HardConstraintFilledTilesinOverride(),
                                MaximizeInterior()
                               ])
        super().__init__("minecraft_farm_village", tiles, rules, cell_size)



