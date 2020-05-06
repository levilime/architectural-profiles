from oldprofiles.tilecollections.abstractbuilder import AbstractBuilder
from oldprofiles.tiles.construction import all_construction_pillars, half_construction_pillars, \
    quarter_construction_pillars
from oldprofiles.tilecollections.minecraftpathway import MineCraftPathway

x = 0
y = 1
z = 2

BORDER = 1


class MineCraftConstruction(AbstractBuilder):
    def __init__(self, match_shape, visual_shape, materials):
        super().__init__(match_shape, visual_shape, materials)
        self.material_assignments = {1: "construction"}
        normal_tiles = [
            *super().VTOM("pillars",
                         all_construction_pillars(visual_shape),
                         ["construction"],
                         {"y": "filled_space", "-y": "filled_space",
                          "x": "empty_space_outside", "-x": "empty_space_outside",
                          "z": "empty_space_outside", "-z": "empty_space_outside"
                          }),
        ]

        rotated_tiles = [
            *super().VTOM("pillars_half",
                         half_construction_pillars(visual_shape),
                         ["construction"],
                         {"y": "filled_space_half", "-y": "filled_space_half",
                          "x": "empty_space_outside", "-x": "empty_space_outside",
                          "z": "empty_space_outside", "-z": "empty_space_outside"}),
            *super().VTOM("pillars_quarter",
                         quarter_construction_pillars(visual_shape),
                         ["construction"],
                         {"y": "filled_space_quarter", "-y": "filled_space_quarter",
                          "x": "empty_space_outside", "-x": "empty_space_outside",
                          "z": "empty_space_outside", "-z": "empty_space_outside"
                          }),
        ]

        textures = super().create_tiles([], rotated_tiles, normal_tiles)
        self.realized_textures = textures
        return

        # TODO also add combinations later
        combinations = [(texture, MineCraftPathway(match_shape, visual_shape).realized_textures) for texture in textures]
        # merge this tile collection with Minecraftpathway
        self.realized_textures = textures + [merged_texture for combination in combinations
                                  for merged_texture in
                                  # merge all textures
                                  [texture_to_merge.merge(combination[0]) for texture_to_merge in combination[1]]]
