from constraints.volumeconstraints import VolumeConstraints
from oldprofiles.rulecombiner import add_rule
# from voxels.magicavoxexporter import export, visualize_voxel

import os

class HabitationProfile:

    def __init__(self, name, tiles, rules, shape):
        """
        :param name: name of the habitation profile.
        :param tiles: consists of tiles, and every tiles knows the constraints with other tiles.
        :param rules: consists of additional rules
        """
        self.name = name
        self.tiles = VolumeConstraints(tiles(shape, shape)
                                  .realized_textures).realized_textures
        self.rules = rules

    def add_rule(self, rule):
        self.rules = add_rule(self.rules, rule)

    def export_visualization(self):
        pass
        # for tile in filter(lambda tile: tile.id.startswith("double_wall_gate") and tile.id.endswith("0"), self.tiles):
        #     visualize_voxel(tile.visual_volume)
