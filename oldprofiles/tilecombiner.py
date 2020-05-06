from constraints.declarativeconstraint import DeclarativeConstraints
from constraints.volumeconstraints import VolumeConstraints
from functools import reduce

from oldprofiles.habitationprofile import HabitationProfile


def combine_tilesets(tilesets):
    def f(match_shape, visual_shape):
        tile_dict = {}
        for tileset in tilesets:
            tile_dict = dict(tile_dict, **reduce(lambda agg, tile: dict(agg, **{tile.id:  tile}),
                               tileset(match_shape, visual_shape).realized_textures, {}))
        return TileAccepter(list(map(lambda key: tile_dict[key], tile_dict)))
    return f


class TileAccepter:

    def __init__(self, realized_textures):
        self.realized_textures = realized_textures


def materialize_tiles(tileset, materials):
    return lambda match_shape, visual_shape: tileset(match_shape, visual_shape, materials)

def materialize_tilesets(materialization, tilesets):
    return [materialize_tiles(tileset, materialization) for tileset in tilesets]
