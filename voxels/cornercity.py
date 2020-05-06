import numpy as np
import math
from functools import reduce
import itertools

from constraints.volumetexture import VolumeTexture
from voxels.simplecity import SimpleCity
from voxels.tilecombiner import create_textures, only_corner_wall_textures, all_rotations_on_y, \
    create_all_wall_possibilities, remove_duplicates

x = 0
y = 1
z = 2

BORDER = 1

class CornerCity:
    # A cell is a voxel grid of booleans:
    # M = array([[[True, True],
    #         [False, False]],
    #        [[False, False],
    #         [False, False]]])
    # M[x,y,z]
    def __init__(self, shape):
        self.shape = shape
        self.realized_textures = self.create_textures(shape)


    def create_textures(self, shape):
        self.shape = shape
        floor_and_roof = self.floor() + self.ceiling()
        boundary_inside_outside = self.floors_for_wall_between_inside_outside()
        textures_to_flip_and_rotate = [

        ]
        textures_to_rotate = [
                    # VolumeTexture("front_wall_inside",
                    #               self.front_wall() + floor_and_roof,
                    #               self.front_wall() + floor_and_roof,
                    #               ["wall", "closed", "inside"]),
                    VolumeTexture("front_wall_with_door_opening_inside",
                                  self.front_wall_with_door_opening() + floor_and_roof,
                                  self.front_wall_with_door_opening() + floor_and_roof,
                                  ["wall", "routing", "vertical", "door", "inside"]),
                    # VolumeTexture("front_wall_with_window_inside",
                    #               self.front_wall_with_window() + floor_and_roof,
                    #               self.front_wall_with_window() + floor_and_roof,
                    #               ["wall", "window", "inside"]),
                    # VolumeTexture("corner_inside",
                    #               self.corner() + floor_and_roof,
                    #               self.corner() + floor_and_roof,
                    #               ["corner", "closed", "inside", "corner"]),
                    VolumeTexture("front_wall_boundary",
                                  self.front_wall() + boundary_inside_outside,
                                  self.front_wall() + boundary_inside_outside,
                                  ["wall", "closed",  "boundary"]),
                    # VolumeTexture("front_wall_with_door_entry",
                    #               self.front_wall() + self.floor_for_wall_between_inside_outside(),
                    #               self.front_wall() + self.floor_for_wall_between_inside_outside(),
                    #               ["wall", "routing", "boundary"]),
                    VolumeTexture("front_wall_with_window_boundary",
                                  self.front_wall_with_window() + boundary_inside_outside,
                                  self.front_wall_with_window() + boundary_inside_outside,
                                  ["wall", "window", "boundary"]),
                    VolumeTexture("corner_boundary",
                                  self.floors_inside_corner() + self.corner(),
                                  self.floors_inside_corner() + self.corner(),
                                  ["wall", "closed", "boundary", "corner"]),
                    # VolumeTexture("t_wall_boundary",
                    #               self.corner() + boundary_inside_outside + self.front_wall(),
                    #               self.corner() + boundary_inside_outside + self.front_wall(),
                    #               ["wall", "closed", "boundary"]),
                    # VolumeTexture("t_wall_inside",
                    #               self.corner() + floor_and_roof + self.front_wall(),
                    #               self.corner() + floor_and_roof + self.front_wall(),
                    #               ["wall", "closed", "inside"]),
                    # VolumeTexture("stairs",
                    #               self.stairs(),
                    #               self.stairs(),
                    #               ["routing", "vertical", "inside"]),
                    VolumeTexture("elevator",
                                  self.elevator(),
                                  self.elevator(),
                                  ["routing", "vertical", "inside"]),
                    VolumeTexture("elevator_ceiling",
                          self.elevator_ceiling(),
                          self.elevator_ceiling(),
                          ["routing", "vertical", "boundary"]),
                    VolumeTexture("elevator_floor",
                          self.elevator_floor(),
                          self.elevator_floor(),
                          ["routing", "vertical", "boundary"]),
                    VolumeTexture("roof_half",
                                  self.empty_space() + self.floor_for_wall_between_inside_outside(),
                                  self.empty_space() + self.floor_for_wall_between_inside_outside(),
                                  ["empty", "boundary", "void", "roof"]),
                    VolumeTexture("roof_fourth",
                                  self.empty_space() + self.floor_inside_corner(),
                                  self.empty_space() + self.floor_inside_corner(),
                                  ["empty", "boundary", "void", "roof"]),
                    VolumeTexture("foundation_half",
                                  self.empty_space() + self.ceiling_for_wall_between_inside_outside(),
                                  self.empty_space() + self.ceiling_for_wall_between_inside_outside(),
                                  ["empty", "boundary", "void", "foundation"]),
                    VolumeTexture("foundation_fourth",
                                  self.empty_space() + self.ceiling_inside_corner(),
                                  self.empty_space() + self.ceiling_inside_corner(),
                                  ["empty", "boundary", "void", "foundation"]),
        ]
        other_textures = [
            # VolumeTexture("stairwell",
            #               self.stairwell(),
            #               self.stairwell(),
            #               ["empty", "inside"]),
            VolumeTexture("empty_space_outside",
                          self.empty_space(),
                          self.empty_space(),
                          ["empty", "outside", "void"]),
            VolumeTexture("roof",
                          self.empty_space() + self.floor(),
                          self.empty_space() + self.floor(),
                          ["empty", "outside", "void"]),
            VolumeTexture("foundation",
                          self.empty_space() + self.ceiling(),
                          self.empty_space() + self.ceiling(),
                          ["empty", "outside", "void"]),
            # VolumeTexture("x_wall",
            #               self.corner() + list(all_rotations_on_y(self.corner()))[2] + floor_and_roof,
            #               self.corner() + list(all_rotations_on_y(self.corner()))[2] + floor_and_roof,
            #               ["wall", "closed", "inside"]
            #               ),
            VolumeTexture("empty_space_inside",
                          self.empty_space() + floor_and_roof,
                          self.empty_space() + floor_and_roof,
                          ["empty", "routing", "inside"])
        ]
        rotated_textures = reduce(lambda agg, t: agg +
                                list(map(
                                    lambda rotated_texture:
                                    VolumeTexture(str(t.id) + str(rotated_texture[0]),
                                                  rotated_texture[1],
                                                  rotated_texture[1],
                                                  t.categories,
                                                  rotated_texture[0],
                                                  str(t.id)),
                                    enumerate(list(all_rotations_on_y(t.match_volume))))

        ), textures_to_rotate, [])
        return rotated_textures + other_textures

    def empty_space(self):
        return np.full(self.shape, False)

    def roof(self):
        return self.empty_space() + self.floor()

    def foundation(self):
        return self.empty_space() + self.ceiling()

    def floor(self):
        M = self.empty_space()
        M[:, 0, :] = True
        return M

    def ceiling(self):
        M = self.empty_space()
        M[:, -1, :] = True
        return M

    def front_wall(self):
        return self.put_in_middle(CornerCity.front_wall_f)

    def front_wall_with_window(self):
        return self.put_in_middle(CornerCity.front_wall_with_window_f)

    def front_wall_with_door_opening(self):
        return self.put_in_middle(CornerCity.front_wall_with_door_opening_f)

    @staticmethod
    def front_wall_with_window_f(M, r):
        new_M = CornerCity.front_wall_f(M, r)
        x_size = math.ceil(new_M.shape[x]/3)
        y_size = math.floor(new_M.shape[y]/3)
        new_M[x_size:new_M.shape[x] - x_size, math.floor(new_M.shape[y]/3):new_M.shape[y] - y_size, :] = False
        return new_M

    @staticmethod
    def front_wall_with_door_opening_f(M, r):
        new_M = CornerCity.front_wall_f(M, r)
        x_size = math.ceil(new_M.shape[x]/3)
        y_size = math.floor(new_M.shape[y]/3)
        new_M[x_size:M.shape[x] - x_size, 1: new_M.shape[y] - y_size, :] = False
        return new_M

    @staticmethod
    def front_wall_f(M, r):
        new_M = np.copy(M)
        new_M[:, :, r] = True
        return new_M

    def put_in_middle(self, wall_function):
        M = np.full(self.shape, False)
        if self.shape[2] % 2 == 0:
            new_M = wall_function(M, range(int(self.shape[2]/2) - 1, int(self.shape[2]/2) + 1))
        else:
            new_M = wall_function(M, range(int(self.shape[2] / 2)))
        return new_M

    def corner(self):
        M = self.empty_space()
        M[0: int(math.floor(M.shape[0]/2) + 1 if M.shape[0] % 2 == 0 else 0),
        :,
        0: int(math.floor(M.shape[2]/2)) + 1 if M.shape[2] % 2 == 0 else 0] = True

        M[0: int(math.floor(M.shape[0]/2)) - 1 if M.shape[0] % 2 == 0 else 0,
        :,
        0: int(math.floor(M.shape[2]/2)) - 1 if M.shape[2] % 2 == 0 else 0] = False
        return M

    def corner_floor_inside(self):
        M = self.corner()
        M[0:int(math.floor(M.shape[0]/2)), -1, 0:int(math.floor(M.shape[2]/2))] = True
        M[0:int(math.floor(M.shape[0] / 2)), 0, 0:int(math.floor(M.shape[2] / 2))] = True
        return M

    def floor_inside_corner(self):
        M = self.empty_space()
        M[0:int(math.floor(M.shape[0] / 2)) + 1, 0, 0:int(math.floor(M.shape[2] / 2)) + 1] = True
        return M

    def floors_inside_corner(self):
        M = self.empty_space()
        M += self.floor_inside_corner()
        M += self.ceiling_inside_corner()
        return M

    def floors_for_wall_between_inside_outside(self):
        M = self.empty_space() + \
            self.floor_for_wall_between_inside_outside() + \
            self.ceiling_for_wall_between_inside_outside()
        return M

    def floor_for_wall_between_inside_outside(self):
        M = self.empty_space()
        M[:, 0, 0:int(math.floor(M.shape[2] / 2)) + 1] = True
        return M

    def ceiling_for_wall_between_inside_outside(self):
        M = self.empty_space()
        M[:, -1, 0:int(math.floor(M.shape[2]/2)) + 1] = True
        return M

    def ceiling_inside_corner(self):
        M = self.empty_space()
        M[0:int(math.floor(M.shape[0]/2)) + 1, -1, 0:int(math.floor(M.shape[2]/2)) + 1] = True
        return M

    def stairwell(self):
        border = BORDER
        M = self.empty_space()
        M += self.floor() + self.ceiling()
        M[border:-border, 0, border:-border] = False
        return M

    def elevator(self):
        border = BORDER
        M = self.empty_space()
        M += self.floor() + self.ceiling()
        M[border:-border, 0, border:-border ] = False
        M[border:-border, -1, border:-border ] = False
        M[border: -border, :, border: -border] = True
        M[border + 1: -border - 1, :, border + 1: -border - 1] = False
        M[border + 1: -border - 1, :, border] = False
        return M

    def elevator_ceiling(self):
        M = self.elevator()
        M += self.ceiling()
        return M

    def elevator_floor(self):
        M = self.elevator()
        M += self.floor()
        return M


    def stairs(self):
        M = self.empty_space()
        M += self.floor()
        border = BORDER
        floor_height = 1
        # border above
        M += self.ceiling()
        M[border:-border, -1, border:-border] = False
        step_height = int(math.ceil(self.shape[y] / (self.shape[x] - border * 2)))
        stair_length = self.shape[x] - border * 2
        for i in range(0, stair_length):
            M[i, 0: min(i * step_height + floor_height, self.shape[y] - 1), border:self.shape[z]-1] = True
        return M

