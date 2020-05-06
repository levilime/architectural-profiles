import numpy as np

from constraints.volumetexture import VolumeTexture
from oldprofiles.tilecollections.abstractbuilder import AbstractBuilder
from oldprofiles.tiles.mountainvillage import front_wall, front_wall_with_door, front_wall_with_window, corner, \
    flipped_corner, front_fence, corner_fence, flipped_corner_fence, stairs, stairs_above_connector, \
    front_wall_template, ceiling, front_wall_middle, front_wall_with_door_opening_middle
from oldprofiles.tiles.roof import  roof_full, roof_template, roof_middle
from oldprofiles.tiles.tiles import roof, floor, front_wall_with_door_opening, empty_space
from solving.util import rotational_order

x = 0
y = 1
z = 2

BORDER = 1


class MineCraftBasicBuilding(AbstractBuilder):
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
            *super().VTOM(
                "roof_template",
                roof_template(visual_shape),
                ["template"],
            ),
            # *super().VTOM(
            #     "roof_middle",
            #     roof_middle(visual_shape),
            #     ["building", "roof"],
            # ),
            # *super().VTOM(
            #     "nice_roof_quarter",
            #     roof_quarter(visual_shape),
            #     ["roof", "building"],
            #     {
            #         "x": "empty_space_outside",
            #         "-x": "roof_template",
            #         "-z": "empty_space_outside",
            #         "z": "roof_template",
            #         "y": "empty_space_outside",
            #         "-y": "filled_space"
            #     }
            # ),
            # *super().VTOM(
            #     "nice_roof_half",
            #     roof_half(visual_shape),
            #     ["roof", "building"],
            # ),
            # *super().VTOM(
            #     "nice_roof_full",
            #     roof_full(visual_shape),
            #     ["roof", "building"],
            #     {
            #         "x": "empty_space_outside",
            #         "-x": "empty_space_outside",
            #         "-z": "empty_space_outside",
            #         "z": "empty_space_outside",
            #         "y": "empty_space_outside",
            #         "-y": "filled_space"
            #     }
            # ),

            *super().VTOM(
                "front_wall_template",
                front_wall_template(visual_shape),
                ["template"],
                {}
            ),
            *super().VTOM(
                "corner_wall_template",
                corner(visual_shape) + ceiling(visual_shape) + floor(visual_shape),
                ["template"]

            # {
            #     "x": "filled_space",
            #     "-z": "filled_space",
            # }
            ),

            *super().VTOM(
                "roof_quarter",
                corner(visual_shape) + ceiling(visual_shape) + floor(visual_shape),
                ["template"]

                # {
                #     "x": "filled_space",
                #     "-z": "filled_space",
                # }
            ),
            *super().VTOM(
                "inside_template",
                ceiling(visual_shape) + floor(visual_shape),
                ["template"]
            ),
            *super().VTOM(
                "corner_wall_flipped_template",
                np.flip(corner(visual_shape), 0) + ceiling(visual_shape) + floor(visual_shape),
                ["template"]
                # {
                #  "-x": "filled_space",
                #  "-z": "filled_space",
                #  }
            ),
            *super().VTOM("front_wall_inside_template",
                          front_wall_middle(visual_shape) + floor(visual_shape) + ceiling(visual_shape),
                          ["template"],
                          ),
            *super().VTOM("t_split_inside_template",
                          front_wall_middle(visual_shape) + floor(visual_shape) +
                          np.rot90(front_wall(visual_shape), 1, (0, 2)) + ceiling(visual_shape),
                          ["template"],
                          ),
            *super().VTOM("floorroof",
                          roof(visual_shape),
                          ["roof", "floor", "boundary", "void", "building", "outside", "routing", "optionalrouting"],
                          [{}, {
                              "x": "empty_space_outside",
                              "-x": "empty_space_outside",
                              "z": "empty_space_outside",
                              "-z": "empty_space_outside",
                              "y": "empty_space_outside",
                              "-y": "filled_space"
                          },
                              {
                                  "-x": "empty_space_outside",
                                  "z": "empty_space_outside",
                                  "-z": "empty_space_outside",
                                  "y": "empty_space_outside",
                                  "-y": "filled_space"
                              },
                              {
                                  "-x": "empty_space_outside",
                                  "-z": "empty_space_outside",
                                  "y": "empty_space_outside",
                                  "-y": "filled_space"
                              },
                              {
                                  "x": "empty_space_outside",
                                  "y": "empty_space_outside",
                                  "-y": "filled_space"
                              }
                          ],
                          [["x", "-x", "z", "-z"]]
                          ),
            # Walls
            *super().VTOM("front_wall",
                          front_wall(visual_shape) + floor(visual_shape),
                          ["wall", "closed", "inside", "boundary", "straight", "building", "interior", "routing"],
                         [{"y": "filled_space",
                           "-z":"floorroof",
                           "-x": "front_wall_template",
                           "z": "front_wall_template",
                           "x": "front_wall_template"},
                          {"y": "filled_space",
                           "-z": "floorroof",
                           "-x": "front_wall_template",
                           "z": "front_wall_template",
                           "x": "front_wall_template",
                           "-y": "empty_space_outside"}
                          ],
                          [["x", "-x", "z"]]
                         ),
            *super().VTOM("front_wall_with_door_opening",
                          front_wall_with_door(visual_shape) +
                          floor(visual_shape),
                          ["wall", "closed", "inside", "boundary", "door", "routing", "straight", "building", "interior"],
                         [{"y": "filled_space", "-z":"floorroof",
                          "-x": "front_wall_template",
                          "z": "front_wall_template",
                          "x": "front_wall_template"
                          },
                          {"y": "filled_space", "-z": "floorroof",
                           "-x": "front_wall_template",
                           "z": "front_wall_template",
                           "x": "front_wall_template","-y": "empty_space_outside"
                           }
                          ],
                          [rotational_order]
                         ),
            *super().VTOM("front_wall_with_window",
                          front_wall_with_window(visual_shape) +
                          floor(visual_shape),
                          ["wall", "window", "boundary", "building", "interior", "routing", "straight"],
                         [{"y": "filled_space", "-z":"floorroof",
                          "-x": "front_wall_template",
                          "z": "front_wall_template",
                          "x": "front_wall_template"
                          },
                          {"y": "filled_space", "-z": "floorroof",
                           "-x": "front_wall_template",
                           "z": "front_wall_template",
                           "x": "front_wall_template", "-y": "empty_space_outside"
                           }
                          ],
                          [["x", "-x", "z"]]
                          ),
            *super().VTOM("corner",
                          corner(visual_shape) + floor(visual_shape),
                          ["wall", "closed", "boundary", "corner", "building", "interior"],
                          [{"y": "filled_space",
                           "-x": "corner_wall_template",
                           "z": "corner_wall_template",
                            "x": "corner_wall_template",
                            "-z": "corner_wall_template",
                           },
                           {"y": "filled_space",
                            "-x": "corner_wall_template",
                            "z": "corner_wall_template",
                            "x": "corner_wall_template",
                            "-z": "empty_space_outside"
                            },
                           {"y": "filled_space",
                            "-x": "corner_wall_template",
                            "z": "corner_wall_template",
                            "-z": "corner_wall_template",
                            "x": "empty_space_outside"
                            },
                           {"y": "filled_space",
                            "-x": "corner_wall_template",
                            "z": "corner_wall_template",
                            "-z": "empty_space_outside",
                            "x": "empty_space_outside"
                            },
                           {"y": "filled_space",
                            "-x": "corner_wall_template",
                            "z": "corner_wall_template",
                            "-z": "corner_wall_template",
                            "x": "floorroof"
                            },
                           {"y": "filled_space",
                            "-x": "corner_wall_template",
                            "z": "corner_wall_template",
                            "-z": "floorroof",
                            "x": "floorroof"
                            },
                           {"y": "filled_space",
                            "-x": "corner_wall_template",
                            "z": "corner_wall_template",
                            "x": "corner_wall_template",
                            "-z": "corner_wall_template","-y": "empty_space_outside"
                            },
                           {"y": "filled_space",
                            "-x": "corner_wall_template",
                            "z": "corner_wall_template",
                            "x": "corner_wall_template",
                            "-z": "empty_space_outside", "-y": "empty_space_outside"
                            },
                           {"y": "filled_space",
                            "-x": "corner_wall_template",
                            "z": "corner_wall_template",
                            "-z": "corner_wall_template",
                            "x": "empty_space_outside", "-y": "empty_space_outside"
                            },
                           {"y": "filled_space",
                            "-x": "corner_wall_template",
                            "z": "corner_wall_template",
                            "-z": "empty_space_outside",
                            "x": "empty_space_outside", "-y": "empty_space_outside"
                            }
                           ],
                          [["z", "-x"]]
                          ),
            *super().VTOM("roof",
                         floor(visual_shape),
                         ["roof", "boundary", "void"],
                         [
                              {
                             "x": "empty_space_outside",
                         "-x": "empty_space_outside",
                         "z": "empty_space_outside",
                         "-z": "empty_space_outside",
                          "y": "empty_space_outside",
                          "-y": "filled_space"
                         },
                              {
                                  "x": "filled_space",
                                  "-x": "empty_space_outside",
                                  "z": "empty_space_outside",
                                  "-z": "empty_space_outside",
                                  "y": "empty_space_outside",
                                  "-y": "filled_space"
                              },
                              {
                                  "x": "filled_space",
                                  "-x": "empty_space_outside",
                                  "z": "filled_space",
                                  "-z": "empty_space_outside",
                                  "y": "empty_space_outside",
                                  "-y": "filled_space"
                              },
                              {
                                  "x": "filled_space",
                                  "-x": "filled_space",
                                  "z": "filled_space",
                                  "-z": "empty_space_outside",
                                  "y": "empty_space_outside",
                                  "-y": "filled_space"
                              },
                              {
                                  "x": "filled_space",
                                  "-x": "filled_space",
                                  "z": "filled_space",
                                  "-z": "filled_space",
                                  "y": "empty_space_outside",
                                  "-y": "filled_space"
                              },
                          ]),
            *super().VTOM("front_wall_inside",
                         front_wall_middle(visual_shape) + floor(visual_shape),
                         ["wall", "closed", "inside", "boundary", "straight", "building", "interior", "straight"],
                         {
                          "y": "filled_space",
                          "z": "front_wall_inside_template",
                          "-z": "front_wall_inside_template",
                              "x": "front_wall_inside_template",
                              "-x": "front_wall_inside_template",
                          },
                         [["x", "-x", "z"], ["x", "-x", "-z"]]
                         ),
            *super().VTOM("front_wall_with_door_opening_inside",
                         front_wall_with_door_opening_middle(visual_shape) +
                         floor(visual_shape),
                         ["wall", "inside", "door", "routing", "building", "interior", "straight"],
                         {"y": "filled_space",
                          "z": "front_wall_inside_template",
                          "-z": "front_wall_inside_template",
                              "x": "front_wall_inside_template",
                              "-x": "front_wall_inside_template",
                          },
                         [["x", "-x", "z", "-z"]]
                         ),
            *super().VTOM("t_split_inside",
                          front_wall_middle(visual_shape) + floor(visual_shape) +
                          np.rot90(front_wall(visual_shape), 1, (0, 2)),
                          ["wall", "closed", "inside", "boundary", "straight", "building", "interior"],
                          {
                              "y": "filled_space",
                              "z": "t_split_inside_template",
                              "-z": "t_split_inside_template",
                              "x": "t_split_inside_template",
                              "-x": "t_split_inside_template",
                          },
                          # TODO doesn't work like this, to do path correctly, path pairs need to be defined (x,z) means
                          # can go with x to z
                          [["x","z"], ["-x", "-z"]]
                          ),
            *super().VTOM("inside",
                         floor(visual_shape),
                         ["wall", "inside", "door", "routing", "building", "interior"],
                         {"y": "filled_space",
                          "-x": "inside_template",
                          "z": "inside_template",
                          "x": "inside_template",
                          "-z": "inside_template",
                          },
                         [["x", "-x", "z", "-z"]]
                         ),

            # super().VTOM("front_fence",
            #              front_fence(visual_shape) + floor(visual_shape),
            #              ["fence", "closed", "boundary", "straight", "exterior"],
            #              {"x": "empty_space_outside", "-x": "empty_space_outside"}),
            # super().VTOM("corner_fence",
            #              corner_fence(visual_shape) + floor(visual_shape),
            #              ["fence", "closed", "boundary", "corner", "exterior"],
            #              {"-x": "empty_space_outside", "-z": "empty_space_outside"}),
            # super().VTOM("flipped_corner_fence",
            #              flipped_corner_fence(visual_shape) + floor(visual_shape),
            #              ["fence", "closed", "boundary", "corner", "exterior"],
            #              {"x": "empty_space_outside", "-z": "empty_space_outside"}),
            # super().VTOM("flipped_corner_fence",
            #              flipped_corner_fence(visual_shape) + floor(visual_shape),
            #              ["fence", "closed", "boundary", "corner", "exterior"],
            #              {"x": "empty_space_outside", "-z": "empty_space_outside"}),


        ]

        flip_and_rotate_tiles = []
        self.realized_textures = super().create_tiles(flip_and_rotate_tiles, rotated_tiles, normal_tiles)
