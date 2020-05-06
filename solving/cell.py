from functools import reduce
from itertools import product

from PIL import Image
import numpy as np

from solving.util import merge_dicts, dimensional_dict_to_tuple, breadth_first_search_for_graph, is_in_range, \
    inverted_dimension_directions

# cell currently has knowledge on what tile rotations are available.
# FIXME this should not be hardcoded in in the cell
rotations = {"x": 1, "y": 4, "z": 1}
rotations_tuple = dimensional_dict_to_tuple(rotations)


class Cell:
    """
    Cell has neighbor cells and contains textures. They reside within a block.
    They are used in blocksolver to solve the block (of cells).
    """
    def __init__(self, textures, id, cell_size):
        # for r in rotations:

        self.contains = reduce(lambda a, t:
                               merge_dicts(a,
                               reduce(lambda agg, elem: merge_dicts(agg, {(elem.id, *t): elem}), textures, {})
        ), product(*[range(0, i) for i in rotations_tuple]), {})
        self.cell_size = cell_size
        self.id = id
        self.neighbors = {}

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def add_neighbors(self, neighbors):
        self.neighbors = neighbors

    def set_tile(self, tile, rotY):
        self.contains = {(tile.id, 0, rotY, 0): tile}

    def show_possibilities(self):
        amount_possibilities = len(self.contains)
        img_array = reduce(lambda agg, texture: np.asarray(texture.transformed_image()) + agg,
                           self.contains.values(),
                           np.zeros((self.cell_size["x"], self.cell_size["y"], 3))) / amount_possibilities
        return Image.fromarray(np.uint8(img_array))

    def get_remaining_contains(self):
        return [self.contains[key] for key in self.contains]

    def is_assigned(self):
        return len(self.contains) == 1

    def get_tile_in_contains(self):
        if len(self.contains) > 1 or len(self.contains) == 0:
            raise ValueError("cell: " + str(self.id) + " has not 1 contains, amount of contains: " +
                             str(len(self.contains)) + ".")
        return {"tile": self.contains[list(self.contains)[0]], "rotY": list(self.contains)[0][2]}

    def copy(self):
        # FIXME copy has now been disabled, because a stack overflow occured sometimes. Necessary to really look at how
        # this should work.
        return self
        # return self._copy({})

    def _copy(self, trace):
        new_cell = Cell({}, self.id, self.cell_size)
        new_cell.contains = self.contains
        trace[self.id] = new_cell
        new_cell.add_neighbors(
            reduce(lambda agg, direction: dict(agg, **{direction: self.neighbors[direction]._copy(trace)
            if self.neighbors[direction].id not in trace else trace[self.neighbors[direction].id]}),
                   [direction for direction in self.neighbors], {}))
        return new_cell

    def possible_adjacency_positions(self, type, entrance=True):
        return reduce(lambda agg, t: agg.union(self.contains[t].get_adjacencies(type, t[2]) if entrance else
                                               self.contains[t].get_adjacencies_ommit_entrance(type, t[2])),
                      self.contains, set())

    def possible_adjacency_directions(self, type, entrance=True):
        return set([inverted_dimension_directions[p] for p in self.possible_adjacency_positions(type, entrance)])
