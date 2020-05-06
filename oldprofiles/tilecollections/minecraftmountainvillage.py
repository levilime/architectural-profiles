import numpy as np

from constraints.volumetexture import VolumeTexture
from oldprofiles.tilecollections.abstractbuilder import AbstractBuilder
from oldprofiles.tiles.mountainvillage import front_wall, front_wall_with_door, front_wall_with_window, corner, \
    flipped_corner, front_fence, corner_fence, flipped_corner_fence, stairs, stairs_above_connector, \
    front_wall_template, ceiling, front_wall_middle, front_wall_with_door_opening_middle
from oldprofiles.tiles.tiles import roof, floor, front_wall_with_door_opening, empty_space
from solving.util import rotational_order

x = 0
y = 1
z = 2

BORDER = 1


class MineCraftMountainVillage(AbstractBuilder):
    # A cell is a voxel grid of booleans:
    # M = array([[[True, True],
    #         [False, False]],
    #        [[False, False],
    #         [False, False]]])
    # M[x,y,z]

    def __init__(self, match_shape, visual_shape, materials):
        super().__init__(match_shape, visual_shape, materials)
        self.material_assignments = {1: "building"}
        normal_tiles = [
        ]

        rotated_tiles = [
            *super().VTOM("stairs",
                         stairs(visual_shape),
                         ["routing", "outside", "vertical", "path", "stairs"],
                         [{"-z": "floorroof", "-y": "filled_space", "z": "filled_space", "x": "filled_space",
                          "-x": "filled_space"},
                          {"-z": "floorroof", "-y": "filled_space", "z": "filled_space", "x": "floorroof",
                           "-x": "floorroof"},
                          {"-z": "floorroof", "-y": "filled_space", "z": "filled_space", "x": "floorroof",
                           "-x": "filled_space"},
                          {"-z": "floorroof", "-y": "filled_space", "z": "filled_space", "x": "filled_space",
                           "-x": "floorroof"}
                          ],
                          [["-z", "y"]]
                          ),
            *super().VTOM("stairs_above_connector",
                         empty_space(visual_shape),
                         ["routing", "outside", "vertical", "path", "void"],
                         {"-y": "stairs", "z": "floorroof"},
                          [["-y", "z"]]
                          ),



        ]

        flip_and_rotate_tiles = []
        self.realized_textures = super().create_tiles(flip_and_rotate_tiles, rotated_tiles, normal_tiles)
