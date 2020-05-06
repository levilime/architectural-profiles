from oldprofiles.habitationprofile import HabitationProfile
from oldprofiles.rulecombiner import combine_rules
from oldprofiles.rules.boundary.emptyboundarymatch import EmptyBoundaryMatch
from oldprofiles.rules.exterior.nofilledtiles import NoFilledTiles
from oldprofiles.rules.maximumvariety import MaximizeVariety
from oldprofiles.tilecollections.testtiles import TestTileSet
from oldprofiles.tilecombiner import combine_tilesets, materialize_tilesets
from oldprofiles.tilecollections.filltestset import FillTestSet


class TestProfile(HabitationProfile):
    def __init__(self, cell_size, materialization):
        tiles = combine_tilesets(materialize_tilesets(materialization,
                                                      [TestTileSet]))
        rules = combine_rules([EmptyBoundaryMatch(), MaximizeVariety()])
        super().__init__("test", tiles, rules, cell_size)
