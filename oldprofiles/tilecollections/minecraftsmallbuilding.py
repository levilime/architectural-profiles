import numpy as np

from constraints.volumetexture import VolumeTexture
from oldprofiles.tilecollections.abstractbuilder import AbstractBuilder
from oldprofiles.tiles.mountainvillage import front_wall, front_wall_with_door, front_wall_with_window, corner, \
    flipped_corner, front_fence, corner_fence, flipped_corner_fence, stairs, stairs_above_connector, \
    front_wall_template, ceiling, front_wall_middle, front_wall_with_door_opening_middle
from oldprofiles.tiles.smallhouses import small_nook, small_room, small_nook_with_window, small_nook_with_door, \
    small_nook_with_side_door
from oldprofiles.tiles.tiles import roof, floor, front_wall_with_door_opening, empty_space
from solving.util import rotational_order

x = 0
y = 1
z = 2

BORDER = 1


class MineCraftSmallBuilding(AbstractBuilder):
    # A cell is a voxel grid of booleans:
    # M = array([[[True, True],
    #         [False, False]],
    #        [[False, False],
    #         [False, False]]])
    # M[x,y,z]

    def __init__(self, match_shape, visual_shape, materials):
        super().__init__(match_shape, visual_shape, materials)
        self.material_assignments = {1: "building"}

        nook_references = [
            {"y": "filled_space",
             "-z": "empty_space_outside",
             "-x": "empty_space_outside",
             "z": "small_nook_template",
             "x": "empty_space_outside",
             "-y": "filled_space"},
            {"y": "filled_space",
             "-z": "empty_space_outside",
             "-x": "small_nook_template",
             "z": "small_nook_template",
             "x": "empty_space_outside",
             "-y": "filled_space"},
            {"y": "filled_space",
             "-z": "small_nook_template",
             "-x": "small_nook_template",
             "z": "small_nook_template",
             "x": "empty_space_outside",
             "-y": "filled_space"},
            {"y": "filled_space",
             "-z": "small_nook_template",
             "-x": "small_nook_template",
             "z": "small_nook_template",
             "x": "empty_space_outside",
             "-y": "filled_space"},
              {"y": "filled_space",
                "-z": "small_nook_template",
                "-x": "small_nook_template",
                "z": "small_nook_template",
                "x": "small_nook_template",
                "-y": "filled_space"},
              {"y": "filled_space",
               "-z": "small_nook_template",
               "-x": "small_nook_template",
               "z": "small_nook_template",
               "x": "small_nook_template",
               "-y": "empty_space_outside"},
              {"y": "filled_space",
               "-z": "small_nook_template",
               "-x": "small_nook_template",
               "z": "small_nook_template",
               "x": "small_nook_template",
               "-y": "empty_space_outside"},
              {"y": "filled_space",
               "-z": "floorroof",
               "-x": "small_nook_template",
               "z": "small_nook_template",
               "x": "small_nook_template",
               "-y": "filled_space"},
              {"y": "filled_space",
               "-z": "floorroof",
               "-x": "small_nook_template",
               "z": "small_nook_template",
               "x": "small_nook_template",
               "-y": "empty_space_outside"},
                           ]

        normal_tiles = [
        ]

        rotated_tiles = [
            *super().VTOM(
                "small_nook_template",
                small_nook(visual_shape) + floor(visual_shape) + ceiling(visual_shape),
                ["template"],
                {}
            ),
            *super().VTOM(
                "small_house_template",
                small_room(visual_shape) + floor(visual_shape) + ceiling(visual_shape),
                ["template"]
            ),
            *super().VTOM("small_nook_window",
                          small_nook_with_window(visual_shape) + floor(visual_shape),
                          ["small_building", "window", "nook", "inside", "boundary", "building", "interior", "routing"],
                          nook_references,
                          [["z"]]
                          ),
            *super().VTOM("small_nook_door",
                          small_nook_with_door(visual_shape) + floor(visual_shape),
                          ["small_building", "door", "nook", "inside", "boundary", "building", "interior", "routing"],
                          nook_references,
                          [["-z", "z"]]
                          ),
            *super().VTOM("small_nook_side_door",
                          small_nook_with_side_door(visual_shape) + floor(visual_shape),
                          ["small_building", "door", "nook", "inside", "boundary", "building", "interior", "routing"],
                          nook_references,
                          [["-x", "z"]]
                          )
        ]
        flip_and_rotate_tiles = []
        self.realized_textures = super().create_tiles(flip_and_rotate_tiles, rotated_tiles, normal_tiles)
