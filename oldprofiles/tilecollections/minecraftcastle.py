from oldprofiles.tilecollections.abstractbuilder import AbstractBuilder
from oldprofiles.tiles.castle import *

x = 0
y = 1
z = 2

BORDER = 1


class MineCraftCastle(AbstractBuilder):
    def __init__(self, match_shape, visual_shape, materialization):
        super().__init__(match_shape,  visual_shape, materialization)
        normal_tiles = []
        rotate_tiles = [
            *super().VTOM(
                "double_wall_vertical",
                double_wall_vertical_open(visual_shape),
                ["outside", "fortified"],
                {
                    "z": "empty_space_outside",
                    "-z": "empty_space_outside",
                },
            ),
            *super().VTOM(
                "double_wall_under",
                double_wall_closed_under(visual_shape),
                ["outside", "fortified"],
                {
                    "z": "empty_space_outside",
                    "-z": "empty_space_outside",
                    "-y": "filled_space"
                }
            ),
            *super().VTOM(
                "double_wall_above",
                double_wall_closed_above(visual_shape),
                ["outside", "fortified"],
                {
                    "z": "empty_space_outside",
                    "-z": "empty_space_outside",
                    #"-y": "filled_space",
                          "y": "empty_space_outside"
                },
                ["x", "-x"]
            ),

            *super().VTOM(
                "double_wall_corner_above",
                double_wall_corner_above(visual_shape),
                ["outside", "fortified"],
                {
                    "z": "empty_space_outside",
                    "-x": "empty_space_outside",
                    "y": "empty_space_outside"
                },
                ["-x", "-z"]
            ),

            *super().VTOM(
                "double_wall_corner_vertical",
                double_wall_corner_vertical(visual_shape),
                ["outside", "fortified"],
                {
                    "z": "empty_space_outside",
                    "-x": "empty_space_outside",
                }
            ),

            *super().VTOM(
                "double_wall_corner_below",
                double_wall_corner_under(visual_shape),
                ["outside", "fortified"],
                {
                    "z": "empty_space_outside",
                    "-x": "empty_space_outside",
                    "-y": "filled_space"
                }
            ),
            *super().VTOM(
                "double_wall_gate",
                double_wall_gate(visual_shape),
                ["outside", "fortified", "boundary", "door"],
                {
                    "z": "x_path",
                    "-z": "x_path",
                    "x": "double_wall_under",
                    "-x": "double_wall_under",
                    "-y": "filled_space",
                    "y": "double_wall_vertical"
                },
                ["z", "-z"]
            )]

        flip_and_rotate_tiles = []

        self.realized_textures = super().create_tiles(flip_and_rotate_tiles, rotate_tiles, normal_tiles)
