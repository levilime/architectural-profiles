from constraints.volumetexture import VolumeTexture
from oldprofiles.tilecollections.abstractbuilder import AbstractBuilder
from oldprofiles.tiles.tiles import empty_space, filled_space

"""
created solely for the purpose of seeing if segment is filled correctly
"""
class FillTestSet(AbstractBuilder):

    def __init__(self, match_shape, visual_shape, materials):
        super().__init__(match_shape, visual_shape, materials)
        normal_tiles = [
            VolumeTexture("empty_space_outside",
                          empty_space(match_shape),
                          empty_space(visual_shape),
                          ["empty", "inside", "void"]),
            *super().VTOM("filled_space",
                         filled_space(visual_shape),
                         ["filled"],
                         [{"x": "empty_space_outside",
                          "-x": "empty_space_outside",
                          "z": "empty_space_outside",
                          "-z": "empty_space_outside",
                          "y": "empty_space_outside",
                          "-y": "empty_space_outside"}]
                         )
            ]
        self.realized_textures = super().create_tiles([], [], normal_tiles)

