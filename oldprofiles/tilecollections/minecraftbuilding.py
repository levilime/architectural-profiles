from constraints.volumetexture import VolumeTexture
from oldprofiles.tilecollections.abstractbuilder import AbstractBuilder
from oldprofiles.tiles.tiles import *

x = 0
y = 1
z = 2

BORDER = 1


class MineCraftBuilding(AbstractBuilder):
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
            # VolumeTexture("roof",
            #               roof(match_shape),
            #               roof(visual_shape),
            #               ["roof", "boundary", "void", "building"]),
            # super().VTOM("foundation",
            #              empty_space(visual_shape),
            #              ["foundation", "boundary", "void", "building"],
            #              {"y": "filled_space"}),
            *super().VTOM("inside",
                         floor(visual_shape),
                         ["inside", "routing", "building"],
                         {"y": "inside"})
        ]

        rotated_tiles = [
            # Vertical finishes
            VolumeTexture("roof_half",
                          floor_for_wall_between_inside_outside(match_shape),
                          floor_for_wall_between_inside_outside(visual_shape),
                          ["roof", "boundary", "void", "building"]),
            VolumeTexture("roof_quarter",
                          floor_inside_corner(match_shape),
                          floor_inside_corner(visual_shape),
                          ["roof", "boundary", "void", "building"]),
            *super().VTOM("foundation_half",
                          empty_space(visual_shape),
                          ["foundation", "boundary", "void", "building"],
                           {"y": "filled_space_half"}
                       ),
            *super().VTOM("foundation_quarter",
                          empty_space(visual_shape),
                          ["foundation", "boundary", "void", "building"],
                           {"y": "filled_space_quarter"}
                       ),
            # Walls
            *super().VTOM("front_wall_inside",
                          front_wall(visual_shape) + floor(visual_shape),
                          ["wall", "closed", "inside", "boundary", "straight", "building", "interior"],
                         {"y": "front_wall_inside"}
                         ),
            *super().VTOM("front_wall_boundary",
                          front_wall(visual_shape) + floor_for_wall_between_inside_outside(visual_shape),
                          ["wall", "closed", "boundary", "straight", "building", "interior"],
                            {"y": "front_wall_boundary"}
                          ),
            *super().VTOM("front_wall_with_door_opening_inside",
                          front_wall_with_door_opening(visual_shape) +
                          floor(visual_shape),
                          ["wall", "closed", "inside", "door",  "routing", "straight", "building", "interior"],
                         {"y": "front_wall_with_door_opening_inside"}
                         ),
            *super().VTOM("front_wall_with_door_opening_boundary",
                          front_wall_with_door_opening(visual_shape) +
                          floor_for_wall_between_inside_outside(visual_shape) +
                          straight_path(visual_shape),
                          ["wall", "door", "routing", "boundary", "straight", "interior", "building"],
                         {"y": "filled_space_half", "-y": "filled_space_half"}
                         ),
            *super().VTOM("front_wall_with_window_boundary",
                          front_wall_with_window(visual_shape) +
                          floor_for_wall_between_inside_outside(visual_shape),
                          ["wall", "window", "boundary", "building", "interior"],
                         {"y": "filled_space_half", "-y": "filled_space_half"}),
            *super().VTOM("corner_boundary",
                          floor_inside_corner(visual_shape) + corner(visual_shape),
                          ["wall", "closed", "boundary", "corner", "building", "interior"],
                          {"y": "corner_boundary"}),
            *super().VTOM("corner_inside",
                         floor(visual_shape) + corner(visual_shape),
                         ["wall", "inside", "corner", "building", "interior"],
                         {"y": "corner_inside"}),
        ]

        flip_and_rotate_tiles = []
        self.realized_textures = super().create_tiles(flip_and_rotate_tiles, rotated_tiles, normal_tiles)
