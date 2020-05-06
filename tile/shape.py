import networkx as nx
import numpy as np
from functools import reduce

from solving.simplesolver import SimpleSolver
from solving.util import translated_dimension_directions, dimensional_tuple_to_dict, inverted_dimension_directions, breadth_first_search_for_graph, show_graph
from tile.adjacency import adjacency_two_tiles
from tile.shapespecification import ShapeMetadata
from voxels.magicavoxwrapper import visualize_voxel

ANY_INDICATOR = "many"

class ContainerShape:

    def __init__(self, category):
        self.category = category

    def has_type(self, t):
        raise NotImplementedError("Implement def has_type in sub class")

    def has_category(self, c):
        raise NotImplementedError("Implement def has_category in sub class")

    def equals(self, other_shape):
        return self.category == other_shape.category


class ProtoShape(ContainerShape):

    def __init__(self, type, category):
        self.type = type
        super().__init__(category)

    def equals(self, other_shape):
        return self.type == other_shape.type and self.category == other_shape.category


class HeadShape:

    def __init__(self):
        self.shapes = set()

    def add_shape(self, shape):
        self.shapes.add(shape)

    # def get_all_shapes(self):
    #     """
    #     :return:
    #     """
    #     # for now loops forever if hierarchical shape is connected with its own hierarchy
    #     # TODO make it not loop forever when that happens
    #     shapes = set()
    #     for shape in self.shapes:
    #         shapes.union(shape.get_all_shapes())
    #     return shapes

    def get_all_free_shapes(self, cells_d):
        return set([free_shape for shape in self.shapes for free_shape in
                    shape.get_all_free_shapes(cells_d,
                    self.get_all_cell_positions_assigned_by_shapes())])

    def get_all_cell_positions_assigned_by_shapes(self):
        shapes = self.get_all_shapes()
        return reduce(lambda agg, shape: agg.union(shape.translated_points()), shapes, set())

    def remove_shape(self, other_shape):
        """
        Removes other_shape from all shapes under this shape
        :return: the shapes that the other_shape was removed
        """
        self.shapes.discard(other_shape)
        for shape in self.shapes:
            shape.remove_shape(other_shape)

    def show_shape_graph(self):
        all_shapes = self.get_all_shapes()
        edges = [(shape, other_shape) for shape in all_shapes for other_shape in shape.shape_edges]
        G = nx.DiGraph()
        G.add_nodes_from(all_shapes)
        G.add_edges_from(edges)
        show_graph(G)

    def get_all_shapes(self):
        found_shapes = reduce(
            lambda current_found_shapes, shape:
            current_found_shapes.union(shape.get_connected_shapes()),
            self.shapes, set())
        return found_shapes

    def __str__(self):
        return "headshape"

class Nameable:

    def __init__(self, name):
        self.name = name

# TODO change name in BBShape, and add PathShape(that uses length and width as its descriptor)
class Shape(ProtoShape, HeadShape, Nameable):

    # TODO instead of putting type and category directly, use shape specification inside shape
    def __init__(self, tiles_at_position, typ, category, initial_position=(0, 0, 0), name=None, shape_metadata=ShapeMetadata()):
        """
        :param tiles_at_position: {tuple(position): {rotY:integer, tile: Tile}}
        :param typ:
        :param category:
        """
        ProtoShape.__init__(self, typ, category)
        HeadShape.__init__(self)
        Nameable.__init__(self, name)
        self.tiles_at_position = tiles_at_position if tiles_at_position else [initial_position]
        self.bounding_box = tuple(np.add(np.subtract(reduce(np.maximum, self.tiles_at_position),
                                                     reduce(np.minimum, self.tiles_at_position)), 1).tolist())
        self.position = initial_position
        self.shape_metadata = shape_metadata
        # denote the shapes for which there exists an outward edge
        self.shape_edges = set()

        # self.type = typ
        # self.category = category
        # children shapes
        # self.shape_graph = ShapeGraph()
        # self.shape_graph.add_shape(self)

    def __str__(self):
        return f"{self.type}, {self.category}, {str(self.bounding_box)}"

    def add_edge_to_other_shape(self, other_shape):
        self.shape_edges.add(other_shape)

    def remove_shape(self, other_shape):
        affected = set()
        self.shapes.discard(other_shape)
        affected = {self} if self.remove_edge_to_shape(other_shape) else affected
        for shape in self.shapes:
            affected = affected.union(shape.remove_shape(other_shape))
        return affected

    def has_type(self, t):
        return self.type == t

    def has_category(self, c):
        return self.category == c

    def remove_edge_to_shape(self, other_shape):
        """
        Remove other shape from the edges outward of this shape
        :param other_shape:
        :return: True if an edge was removed else False
        """
        prev_len = len(self.shape_edges)
        self.shape_edges.discard(other_shape)
        return prev_len == len(self.shape_edges)

    def get_bounding_box(self):
        return tuple(np.add(np.subtract(reduce(np.maximum, self.tiles_at_position),
                                               reduce(np.minimum, self.tiles_at_position)), 1).tolist())

    # def add_shape(self, shape):
    #     self.shapes.append(shape)
    #     # other_bb_size = shape.get_bounding_box()
    #     # pos_diff = np.subtract(self.position, shape.position)
    #     # translated_bb = np.add(other_bb_size, pos_diff)
    #     # self.bounding_box = tuple(np.maximum(translated_bb, self.bounding_box))

    def check_if_position_is_adjacent(self, position, translated_points=None):
        surroundings = translated_dimension_directions(position)
        translated_points = self.translated_points() if not translated_points else translated_points
        adjacency_directions = []
        for d in surroundings:
            if surroundings[d] in translated_points:
                adjacency_directions.append(d)
        return adjacency_directions

    def translated_points(self):
        """
        gives all positions in absolute form
        :return:
        """
        return self.specific_translated_points(self.tiles_at_position)

    def specific_translated_points(self, points):
        """
        translates specific positions from relative to absolute
        :param points:
        :return:
        """
        return set([tuple(np.add(p, self.position)) for p in points])

    def get_position(self, position):
        return self.tiles_at_position.get(tuple(np.subtract(position, self.position)))

    def get_tile_signature_at_position(self, position):
        """
        tile at position
        :param position: absolute position
        :return: (tile_id, rotX, rotY, rotZ)
        """
        return (self.get_position(position)["tile"].id, 0, self.get_position(position)["rotY"], 0)

    def get_tile_at_position(self, position):
        return self.get_position(position)["tile"]

    def get_outside_entrance_positions(self):
        """
        :return: [{entrance_position: position, adjacent_position: position}]
        """
        entrances = self.get_entrances()
        free_positions = []
        for entrance_position in entrances:
            tile_id, rotx, roty, rotz = self.get_tile_signature_at_position(entrance_position)
            tile = self.get_tile_at_position(entrance_position)
            for entrance_adjacency in tile.get_entrance_adjacencies(self.type, roty):
                relative_position = entrance_adjacency
                absolute_position = tuple(np.add(relative_position, entrance_position))
                if not absolute_position in self.tiles_at_position:
                    adjacent_entrance_position = absolute_position
                    free_positions.append(dict(entrance_position=entrance_position,
                                               entrance_position_tile=tile,
                                               type=self.type,
                                               adjacent_position=adjacent_entrance_position,
                                               direction=inverted_dimension_directions[tuple(
                                               np.subtract(entrance_position, adjacent_entrance_position))]))
        return free_positions

    def get_free_positions(self, cells_d, assigned_to_shape_positions):
        """
        a position is free if it has the position to be
        an entrance to a cell that is not yet assigned to a shape (or out of bounds).
        :param cells_d:
        :return:
        """
        return filter(lambda p:
                      p["adjacent_position"] in cells_d and not p["adjacent_position"] in assigned_to_shape_positions,
                      self.get_outside_entrance_positions())

    def is_connectable(self, cells_d, assigned_to_shape_positions):
        return len(list(self.get_free_positions(cells_d, assigned_to_shape_positions))) > 0

    def get_all_adjacencies_between_shapes(self, shape):
        adjacencies = {}
        translated_points = self.translated_points()
        for position in shape.translated_points():
            result = self.check_if_position_is_adjacent(position, translated_points)
            if result:
                adjacencies[position] = result
        return adjacencies

    def to_block(self, profile):
        empty_tile = profile.empty_tile
        cell_size = dimensional_tuple_to_dict(profile.empty_tile.shape)
        block_size = dimensional_tuple_to_dict(self.bounding_box)
        block = SimpleSolver.fill_mocked_block_with_empty_tiles(block_size, cell_size,
                                                                empty_tile)
        cells_dict = {}
        for cell in block.cells:
            cells_dict[cell.id] = cell
        for position in self.tiles_at_position:
            tileinfo = self.tiles_at_position[position]
            tile = tileinfo["tile"]
            rotY = tileinfo["rotY"]
            cells_dict[position].contains = {(tile.id, 0, rotY, 0): tile}
        block.successful = True
        return block

    def show(self, profile, adjacency_type=None):
        block = self.to_block(profile)
        if adjacency_type:
            # visualize_voxel(block.show_adjacency(adjacency_type))
            return block.show_adjacency(adjacency_type)
        else:
            # visualize_voxel(block.show())
            return block.show()

    def children_are_complete(self, profile):
        for child in self.shapes:
            if not child.is_complete(profile):
                return False
        return True

    def _get_all_adjacencies_of_position(self, position):
        """
        all adjacencies of a position
        given in relative positions
        :param position: relative position
        :return:
        """
        ll = []
        at_position = self.tiles_at_position[position]
        tile_id, rotX, rotY, rotZ = at_position["tile"].id, 0, at_position["rotY"], 0
        # all adjacent tiles that follow the adjacency subset of the tile
        for position_change in at_position["tile"].get_adjacencies(self.type, rotY):
            # get direction according to position change
            direction = inverted_dimension_directions[position_change]
            other_position = tuple(np.add(position_change, position))
            # yield other_position, direction
            ll.append((other_position, direction))
        return ll

    def get_entrances(self):
        """
        get all entrances to outside the shape,
        this is given in absolute positions
        :return:
        """
        ll = set()
        for position in self.tiles_at_position:
            # take the tile at the position
            at_position = self.tiles_at_position[position]
            tile_id, rotX, rotY, rotZ = at_position["tile"].id, 0, at_position["rotY"], 0
            for other_position, direction in self._get_all_adjacencies_of_position(position):
                if not other_position in self.tiles_at_position and \
                        at_position["tile"].is_entrance(self.type, rotY, direction):
                    ll.add(position)
        return self.specific_translated_points(ll)

    def is_complete(self, profile):
        """
        when a shape is complete it has no tiles that have a direction that go outside the shape, except if that direction
        is an entrance.
        :return:
        """
        # for every position in the shape
        for position in self.tiles_at_position:
            # take the tile at the position
            at_position = self.tiles_at_position[position]
            tile_id, rotX, rotY, rotZ = at_position["tile"].id, 0, at_position["rotY"], 0
            # all adjacent tiles that follow the adjacency subset of the tile
            for other_position, direction in self._get_all_adjacencies_of_position(position):
                # if other position is in the shape, then check whether the adjacencies match up
                if not other_position in self.tiles_at_position and \
                        not at_position["tile"].is_entrance(self.type, rotY, direction):
                    print(f"{position} has {tile_id} and rot {rotY} and does not on {direction} have an entrance")
                    return False

                # FIXME probably also need to check with children positions, parent tiles don't have to adhere to child tiles,
                # FIXME therefore adjacency from parent to/from child tile can be ignored
                if other_position in self.tiles_at_position:
                    at_other_position = self.tiles_at_position[other_position]
                    tile_id_other, rotX_other, rotY_other, rotZ_other = \
                        at_other_position["tile"].id, 0, at_other_position["rotY"], 0
                    complete = adjacency_two_tiles(profile, (tile_id, rotX, rotY, rotZ),
                                        (tile_id_other, rotX_other, rotY_other, rotZ_other),
                                                   direction, adjacency_subset=self.type) or \
                               at_position["tile"].is_entrance(self.type, rotY, direction)
                    if not complete:
                        print(f"{position} has {tile_id, rotY} and does not match on {direction} with {tile_id_other, rotY_other}")
                        return False
                # if the other position is not in the shape, then check if it is an entrance, that may go out of the shape
                print(f"{position} has {tile_id} completes on {direction}")
        return True and self.children_are_complete(profile)

    def get_shapes(self):
        return self.get_all_shapes()

    def get_all_free_shapes(self, cells_d, assigned_cell_positions=None):
        """
        A shape is free if it has an entrance that is not directly connected to an other shape.
        :param cells_d:
        :return:
        """
        if not assigned_cell_positions:
            assigned_cell_positions = self.get_all_cell_positions_assigned_by_shapes()
        return list(filter(lambda shape: shape.is_connectable(cells_d, assigned_cell_positions),
                           self.get_connected_shapes()))

    def get_connected_shapes(self):
        def direction_f(shape):
            return shape.shape_edges

        # def match_condition_c(found_shapes):
        #     return lambda shape: shape not in found_shapes

        found_shapes = set(breadth_first_search_for_graph(
                    self,
                    lambda x: True,
                    direction_f))
        return found_shapes

class CombinedShape(Shape):

    def __init__(self, tiles_at_position, initial_position=(0, 0, 0), name=None):
        # many is used to indicate that the shape does not have on type/category
        # FIXME make a more robust, integral solution
        super().__init__(tiles_at_position, ANY_INDICATOR, ANY_INDICATOR, initial_position, name)
