from oldprofiles.habitationprofile import HabitationProfile
from oldprofiles.rulecombiner import combine_rules
from oldprofiles.rules.boundary.emptyboundarymatch import EmptyBoundaryMatch
from oldprofiles.rules.exterior.hardconstraintfilledtilesinoverride import HardConstraintFilledTilesinOverride
from oldprofiles.rules.exterior.nofilledtiles import NoFilledTiles
from oldprofiles.tilecombiner import combine_tilesets, materialize_tilesets
from oldprofiles.tilecollections.filltestset import FillTestSet


class EmptyProfile(HabitationProfile):
    def __init__(self, cell_size, materialization):
        tiles = combine_tilesets(materialize_tilesets(materialization,
                                                      [FillTestSet
                                                       ]))
        rules = combine_rules([NoFilledTiles(),
                               HardConstraintFilledTilesinOverride()
                               ])
        super().__init__("empty", tiles, rules, cell_size)



