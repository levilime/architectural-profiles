from functools import reduce

from constraints.volumetexture import VolumeTexture
from voxels.tilecombiner import all_rotations_on_y

import numpy as np

import re

ALT_IDENTIFIER = "Alt"


def remove_alt_from_texture_name(identifier):
    return re.sub(r"" + ALT_IDENTIFIER + "[0-9]*" + ALT_IDENTIFIER, "", identifier)


def add_alt_texture_name(identifier, i):
    return identifier + ALT_IDENTIFIER + str(i) + ALT_IDENTIFIER

class AbstractBuilder:

    def __init__(self, match_shape, visual_shape, materialization):
        self.match_shape = match_shape
        self.visual_shape = visual_shape
        self.materialization = materialization
        self.material_assignments = {1: "general"}



    def change_materials_tiles(self, tiles):
        for tile in tiles:
            new_visual_volume = np.copy(tile.visual_volume) # np.empty(np.shape(tile), dtype=int)
            it = np.nditer(new_visual_volume, flags=['multi_index'])
            while not it.finished:
                value = int(it[0])
                if value in self.material_assignments and self.material_assignments[value] in self.materialization:
                    new_visual_volume[it.multi_index] = self.materialization[self.material_assignments[value]]
                it.iternext()
            tile.visual_volume = new_visual_volume
        return tiles

    def create_tiles(self, tiles_to_rotate_and_flip, tiles_to_rotate, tiles):
        rotated_tiles = reduce(lambda agg, t: agg +
                                list(map(
                                    lambda rotated_texture:
                                    VolumeTexture(str(t.id) + str(rotated_texture[0]),
                                                  rotated_texture[1][0],
                                                  rotated_texture[1][1],
                                                  t.categories,
                                                  rotated_texture[0],
                                                  str(t.id),
                                                  reduce(lambda agg, overriding_edge_key:
                                                         dict(agg, **{
                                                             overriding_edge_key: [t.overriding_edges[overriding_edge_key][0]
                                                                                  + str(rotated_texture[0])]})
                                                         , t.overriding_edges, {}),
                                                  VolumeTexture.resolve_route_connections(t.route_connections, rotated_texture[0],
                                                                                          ),
                                                  t.mastergroup
                                                  ),
                                    enumerate(zip(list(all_rotations_on_y(t.match_volume)),
                                                  list(all_rotations_on_y(t.visual_volume)))))
        ), tiles_to_rotate + tiles_to_rotate_and_flip, [])

        return self.change_materials_tiles(rotated_tiles + tiles)

    def match_visual_pair(self):
        return self.match_shape, self.visual_shape

    def VTOM(self, identifier, visual_volume, categories, overriding_edges={}, route_connections = [], direction=0, group=None):
        """
        Stands for Volume Tile Overriding edges.
        :param id:
        :param visual_volume:
        :return:
        """
        # make all overriding edge values a list if not a list already, done to make merging volume textures seamless
        overriding_edges = overriding_edges if isinstance(overriding_edges, list) else [overriding_edges]
        textures = []

        if len(categories) == 0:
            raise ValueError("Categories may not be empty, the rule noemptyboundary and maybe others do not handle no categories well")
        first = True
        for i, overriding_edges_object in enumerate(overriding_edges):
            adjusted_overriding_edges = reduce(lambda agg, key: dict(agg, **{key: overriding_edges_object[key]
            if isinstance(overriding_edges_object[key], list) else [overriding_edges_object[key]]}), overriding_edges_object, {})

            texture = VolumeTexture(identifier if first else add_alt_texture_name(identifier, i), visual_volume, visual_volume,
                              categories, direction, group, adjusted_overriding_edges, route_connections, first)
            texture.group = identifier
            textures.append(texture)
            first = False
        return textures
