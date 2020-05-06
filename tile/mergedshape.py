import numpy as np

from solving.simplesolver import SimpleSolver
from solving.util import dimensional_tuple_to_dict, random_color
from tile.shape import ProtoShape
from tile.tile import Tile


class ShapeCollection(ProtoShape):
    def __init__(self, adjacency_type, category):
        super().__init__(adjacency_type, category)
        # self.type = adjacency_type
        # self.category = category
        self.shapes = []
        self.position = None
        # maximum shape in the collection
        self.max_bounding_box = None
        # minimum shape in the collection
        self.min_bounding_box = None
        # bounding box over the entire collection
        self.collection_bounding_box = None

    # def get_range(self):
    #     return self.min_bounding_box, self.max_bounding_box

    def get_identifier(self):
        return f"{self.type}{self.category}min{''.join(map(str,self.min_bounding_box))}" \
               f"max{''.join(map(str,self.max_bounding_box))}"

    def add_shape(self, shape):
        # type and category need to be the same of the shape and container
        assert(shape.type == self.type)
        assert (shape.category == self.category)
        self.collection_bounding_box = shape.bounding_box if not self.collection_bounding_box else \
            tuple(np.maximum(np.add(shape.position, shape.bounding_box), self.collection_bounding_box))
        self.max_bounding_box = shape.bounding_box if not self.max_bounding_box else \
            shape.bounding_box if np.sum(shape.bounding_box) > np.sum(self.max_bounding_box) else self.max_bounding_box
        self.min_bounding_box = shape.bounding_box if not self.min_bounding_box else \
            shape.bounding_box if np.sum(shape.bounding_box) < np.sum(self.min_bounding_box) else self.min_bounding_box
        #self.position = self.position if self.position and np.sum(shape.position) > np.sum(self.position) \
        #    else shape.position
        self.position = tuple(np.minimum(self.position, shape.position)) if self.position else shape.position
        self.shapes.append(shape)

    def show(self, profile, random_color=random_color):
        empty_tile = profile.empty_tile
        cell_size = dimensional_tuple_to_dict(profile.empty_tile.shape)
        block_size = dimensional_tuple_to_dict(self.collection_bounding_box)
        block = SimpleSolver.fill_mocked_block_with_empty_tiles(block_size, cell_size,
                                                                empty_tile)
        cells_dict = {}
        for cell in block.cells:
            cells_dict[cell.id] = cell
        smallest_position = self.position
        for shape in self.shapes:
            color = random_color()
            for position in shape.translated_points():
                tileinfo = shape.get_position(position)
                tile = tileinfo["tile"]
                rotY = tileinfo["rotY"]
                new_tile = Tile(tile.id, tile.shape.astype(dtype=bool).astype(dtype=int) * color,
                                tile.categories, tile.adjacencies)
                cells_dict[tuple(np.subtract(position, smallest_position))].contains = {(tile.id, 0, rotY, 0): new_tile}
        block.successful = True
        return block.show()
