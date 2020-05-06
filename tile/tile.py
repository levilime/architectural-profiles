import json
import math

import numpy as np

from solving.util import dimension_directions, merge_dicts, get_rotated_dimension
from voxels.magicavoxwrapper import visualize_voxel


class Tile:

    def __init__(self, id, shape, categories, adjacencies, entrance_adjacencies={}):
        if not isinstance(id, str):
            raise TypeError(f"Tile id must be a string, id: {str(id)} is not.")
        self.id = id
        self.shape = shape
        self.categories = categories
        self.adjacencies = adjacencies
        self.entrance_adjacencies = entrance_adjacencies

    def available_types(self):
        return self.adjacencies.keys()

    def equal(self, tile):
        return tile.id == self.id

    def show(self):
        return self.shape

    def show_with_rotation(self, rotations):
        return np.rot90(self.show(), int(rotations[1]), (0,2))

    def show_adjacency(self, type, color=1.0):
        shape = np.full(self.shape.shape, False, dtype=bool)
        if type not in self.adjacencies:
            return shape
        directions = self.adjacencies[type]
        adjusted_dimensions_directions = {"x": (0,0,1), "-x": (0,0,-1), "z": (1,0,0), "-z": (-1,0,0), "y": (0,-1,0),
                                          "-y": (0,1,0)}

        # adjusted_dimensions_directions = merge_dicts(dimension_directions, {})
        # temp = adjusted_dimensions_directions["-y"]
        # adjusted_dimensions_directions["-y"] = adjusted_dimensions_directions["y"]
        # adjusted_dimensions_directions["y"] = temp
        #
        # temp = adjusted_dimensions_directions["-z"]
        # adjusted_dimensions_directions["-z"] = adjusted_dimensions_directions["-x"]
        # adjusted_dimensions_directions["-x"] = temp

        for direction in directions:
            t = adjusted_dimensions_directions[direction]
            d = [i for i,x in enumerate(t) if not x == 0][0]
            get_the_middle_of_the_shape = lambda i: range(math.floor((shape.shape[i] -
                                                                      (1 if shape.shape[i] % 2 == 0 else 0))/2),
                           math.ceil(shape.shape[i]/2))
            get_bottom_to_middle = lambda i: range(0, math.ceil(shape.shape[i]/2))
            get_middle_to_top = lambda i: range(math.floor(shape.shape[i]/2), shape.shape[i])
            r = np.ix_(*[get_the_middle_of_the_shape(i) if not d == i else
                     (get_bottom_to_middle(i) if t[d] < 0 else
                      get_middle_to_top(i))
                     for i in range(0, 3)])
            shape[r] = 1 * color

        # shape = np.rot90(shape, -1, (0,2))
        return shape

    def get_adjacencies(self, type, rotY, adjacencies=None):
        return set([dimension_directions[d] for d in self.get_adjacencies_with_directions(type, rotY, adjacencies)])

    def get_adjacencies_with_directions(self, type, rotY, adjacencies=None, entrance=True):
        if not adjacencies:
            adjacencies = self.adjacencies
        if type not in adjacencies:
            # raise an explicit exception
            # raise Exception(type + " is not an adjacency type for tile: " + self.id)
            return set()
            # return set()
        directions = adjacencies[type]
        if not entrance:
           directions = set(directions).difference(set(self.entrance_adjacencies[type]))
        # dimension_directions
        rotated_directions = [get_rotated_dimension(d, rotY) for d in directions]
        return rotated_directions

    def get_entrance_adjacencies(self, type, rotY):
        return self.get_adjacencies(type, rotY, self.entrance_adjacencies)

    def get_adjacencies_ommit_entrance(self, type, rotY):
        return self.get_adjacencies(type, rotY).difference(self.get_entrance_adjacencies(type, rotY))

    def is_entrance(self, type, rotY, direction):
        return get_rotated_dimension(direction, -rotY) in self.entrance_adjacencies[type] \
            if type in self.entrance_adjacencies else False

    def show_adjacency_with_rotation(self, type, rotations):
        return np.rot90(self.show_adjacency(type), int(rotations[1]), (0,2))

    def serialize(self):
        return {"id": self.id, "categories": list(self.categories)}

    def one_of_categories_in_tile(self, categories):
        for category in categories:
            if category in self.categories:
                return True
        return False
