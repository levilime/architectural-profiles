from constraints.volumetexture import VolumeTexture
from oldprofiles.tilecollections.abstractbuilder import AbstractBuilder
from oldprofiles.tiles.tiles import *
import copy

x = 0
y = 1
z = 2

BORDER = 1


class MineCraftPathway(AbstractBuilder):

    # A cell is a voxel grid of booleans:
    # M = array([[[True, True],
    #         [False, False]],
    #        [[False, False],
    #         [False, False]]])
    # M[x,y,z]

    def __init__(self, match_shape, visual_shape, materials):
        super().__init__(match_shape, visual_shape, materials)
        self.material_assignments = {1: "path"}
        normal_tiles = [

        ]

        single_rotate_tiles = [
            *super().VTOM("straight_path",
                          straight_path(visual_shape),
                          ["routing", "outside", "path"],
                          {"-y": "empty_space_outside",
                           "z": "floorroof",
                           "-z": "floorroof"
                           },
                         ["z", "-z"]),
        ]

        rotated_tiles = [
            *super().VTOM("x_path",
                          x_path(visual_shape),
                          ["routing", "outside", "path"],
                          {"-y": "empty_space_outside",
                           "x": "floorroof",
                           "-x": "floorroof",
                           "z": "floorroof",
                           "-z": "floorroof",
                           },
                          ["x", "-x", "z", "-z"]
                          ),


            *super().VTOM("corner_path",
                          corner_path(visual_shape),
                          ["routing", "outside", "path"],
                          {"-y": "empty_space_outside",
                           "-x": "floorroof",
                           "-z": "floorroof",
                           },
                                      ["-x", "-z"]),
                         *super().VTOM("t_path",
                                       t_path(visual_shape),
                                       ["routing", "outside", "path"],
                                       {"-y": "empty_space_outside",
                                        "-x": "floorroof",
                                        "z": "floorroof",
                                        "-z": "floorroof"
                                        },
                                      ["-x", "-z", "z"]),
                         *super().VTOM("stairs",
                                       stairs(visual_shape),
                                       ["routing", "outside", "vertical", "path"],
                                       {"-y": "empty_space_outside",
                                        "-z": "floorroof",
                                        "z": "empty_space_outside"},
                                      ["-z", "y"]),
                         *super().VTOM("stairs_above_connector",
                                       empty_space(visual_shape),
                                       ["routing", "outside", "vertical", "path"],
                                      {"-y": "stairs", "z": "floorroof"},
                                      ["-y", "z"]),
                         ]

        flip_and_rotate_tiles = []
        #     VolumeTexture("corner_boundary",
        #                   *self.consume(lambda shape: floors_inside_corner(shape) + corner(shape)),
        #                   ["wall", "closed", "boundary", "corner"]),
        # ]

        def copy_and_add_filled(tiles):
            ll = []
            for tile in tiles:
                if "-y" in tile.overriding_edges and tile.overriding_edges["-y"][0] == "empty_space_outside":
                    c = copy.deepcopy(tile)
                    c.overriding_edges["-y"] = ["filled_space"]
                    c.id += "filledfoundation"
                    ll.append(c)
            return ll

        flip_and_rotate_tiles += copy_and_add_filled(flip_and_rotate_tiles)
        rotated_tiles += copy_and_add_filled(rotated_tiles)
        single_rotate_tiles += copy_and_add_filled(single_rotate_tiles)
        normal_tiles += copy_and_add_filled(normal_tiles)
        self.realized_textures = super().create_tiles(flip_and_rotate_tiles, rotated_tiles + single_rotate_tiles,
                                                      normal_tiles)
        for texture in self.realized_textures:
            if "filledfoundation" in texture.id:
                texture.group = texture.group.replace("filledfoundation", "")
        pass

    # def consume(self, f):
    #     # return map(lambda shape: f(shape), super().match_visual_pair())
    #     return map(lambda i_shape: f(i_shape[1])
    #     if i_shape[0] < 1 else cut_tile_on_all_positive_sides(f(i_shape[1])),
    #                enumerate([self.match_shape, self.match_shape]))
