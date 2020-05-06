from constraints.volumetexture import VolumeTexture
from oldprofiles.tilecollections.abstractbuilder import AbstractBuilder
from oldprofiles.tiles.tiles import empty_space, filled_space, filled_space_half, filled_space_quarter, floor


class DefaultTileSet(AbstractBuilder):

    def __init__(self, match_shape, visual_shape, materials):
        super().__init__(match_shape, visual_shape, materials)
        normal_tiles = [
            # VolumeTexture("empty_space_inside",
            #               empty_space(match_shape),
            #               empty_space(visual_shape),
            #               ["empty", "inside", "void"]),
            VolumeTexture("empty_space_outside",
                          empty_space(match_shape),
                          empty_space(visual_shape),
                          ["empty", "outside", "void"]),
            *super().VTOM("filled_space",
                          filled_space(visual_shape),
                          ["filled"],
                         [{
                         },
                              {
                                   "y": "empty_space_outside"
                              }
                          ]
                         ),
            *super().VTOM("roof",
                         floor(visual_shape),
                         ["roof", "boundary", "void"],
                         {
                             "x": "empty_space_outside",
                         "-x": "empty_space_outside",
                         "z": "empty_space_outside",
                         "-z": "empty_space_outside",
                          "y": "empty_space_outside",
                          "-y": "filled_space"
                         }),
            ]
        rotated_tiles = [
            # VolumeTexture("filled_space_half",
            #               filled_space_half(match_shape),
            #               filled_space_half(visual_shape),
            #               ["filled"]
            #               ),
            # VolumeTexture("filled_space_quarter",
            #               filled_space_quarter(match_shape),
            #               filled_space_quarter(visual_shape),
            #               ["filled"]
            #               )
        ]
        self.realized_textures = super().create_tiles([], rotated_tiles, normal_tiles)

