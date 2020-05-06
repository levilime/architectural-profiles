from functools import reduce

from adjacencyfromexample import all_tiles_at_postions
from solving.util import dimension_directions, deep_merge, invert_dimension, merge_dicts, \
    breadth_first_search_for_graph, breadth_first_search, minimum_vector_of_list
from tile.adjacency import add_addjacencies, adjacency_two_tiles
from tile.mergedshape import ShapeCollection
from tile.shape import Shape
from itertools import product, permutations, combinations
import numpy as np

from tile.shapeadjacency import ShapeAdjacency
from voxels.magicavoxwrapper import visualize_voxel

def shapes_from_example(tiles, shape, example, relevant_type_category_pairs, tile_exemption_allowed_mode=True):
    M = example
    # go over all tiles
    tiles_at_position = all_tiles_at_postions(M, shape, tiles, tile_exemption_allowed_mode)
    # extract the adjacencies
    shapes = []
    for type_category_pair in relevant_type_category_pairs:
        type = type_category_pair[0]
        category = type_category_pair[1]
        positions_with_relevant_tiles = reduce(lambda agg, i: merge_dicts(agg, {i: tiles_at_position[i]}) if
            category in tiles_at_position[i]["tile"].categories else agg, tiles_at_position, {})
        unseen = set(list(positions_with_relevant_tiles))
        while len(unseen) > 0:
            current_position = unseen.pop()

            def match_condition(position):
                return True

            def direction_f(position):
                rotation_y = tiles_at_position[position]["rotY"]
                tile = tiles_at_position[position]["tile"]
                # get new positions by adding the current position with the changes in direction of the rotated tile
                new_positions = [tuple(np.add(position, change_position)) for change_position in
                        tile.get_adjacencies(type, rotation_y)]
                # filter out positions that are out of bound or already seen
                return filter(lambda new_position: new_position in tiles_at_position and
                              new_position in unseen and category in tiles_at_position[new_position]["tile"].categories,
                              new_positions)
            new_shape_positions = breadth_first_search_for_graph(tuple(current_position), match_condition, direction_f)
            unseen = unseen.difference(new_shape_positions)
            minimum_position = tuple(reduce(np.minimum, new_shape_positions))

            skewed_positions = reduce(lambda agg, p:
                                      merge_dicts(agg,
                                        {tuple(np.subtract(p, minimum_position).tolist()): tiles_at_position[p]}),
                                                  new_shape_positions, {})
            shapes.append(Shape(
                reduce(lambda agg, p: merge_dicts(agg, {p: skewed_positions[p]}),
                       skewed_positions, {}), type, category, minimum_position))
    return shapes


def adjacencies_in_shapes(profile, shapes, relevant_types):
    adjacent_shapes = {}
    shape_combinations = filter(lambda pair: pair[0].type == pair[1].type, combinations(shapes, 2))
    for shape_a, shape_b in shape_combinations:
        if not shapes_are_adjacent([shape_a, shape_b]):
            continue
        # FIXME temporary rule to not have adjacent shapes with the same category, but that
        # two adjacent shapes have the same category and type should not occur in the first place!
        if shape_a.category == shape_b.category:
            continue
        adjacencies = shape_b.get_all_adjacencies_between_shapes(shape_a)

        def is_adjacent(type, adjacencies):
            for position in adjacencies:
                for direction in adjacencies[position]:
                    tile_a = shape_a.get_tile_signature_at_position(position)
                    tile_b = shape_b.get_tile_signature_at_position(tuple(np.add(dimension_directions[direction], position)))
                    if adjacency_two_tiles(profile, tile_a, tile_b, direction, type):
                        return True
            return False

        for typ in relevant_types:
            if is_adjacent(typ, adjacencies):
                if typ in adjacent_shapes:
                    adjacent_shapes[typ].append((shape_a, shape_b))
                else:
                    adjacent_shapes[typ] = [(shape_a, shape_b)]
    return reduce(lambda agg, k: agg + adjacent_shapes[k], adjacent_shapes, [])


def merge_shape_adjacencies(adjacent_shapes):
    container = {}
    def add_to_container(shape_a, shape_b):
        # TODO also implement hierarchichal shape adjacencies
        assert(shape_a.type == shape_b.type)
        identifier = (shape_a.type, *[f(shape_a.category, shape_b.category) for f in [min, max]])
        first_shape = shape_a if shape_a.category == identifier[1] else shape_b
        second_shape = shape_b if shape_b.category == identifier[2] else shape_a
        if not identifier in container:
            container[identifier] = ShapeAdjacency(ShapeCollection(first_shape.type, first_shape.category),
                                                   ShapeCollection(second_shape.type, second_shape.category))
        container[identifier].shape_a.add_shape(first_shape)
        container[identifier].shape_b.add_shape(second_shape)

    for adjacency_pair in adjacent_shapes:
        add_to_container(*adjacency_pair)
    return list(container.values())

def flatten_shape_containers(shape_containers):
    pass

def shape_adjacencies_to_shape_containers(adjacent_shapes):
    container = {}
    def add_to_container(shape):
        identifier = (shape.type, shape.category)
        if not identifier in container:
            container[identifier] = ShapeCollection(*identifier)
        container[identifier].add_shape(shape)

    for adjacency_pair in adjacent_shapes:
        [add_to_container(adjacency) for adjacency in adjacency_pair]
    return list(container.values())


def shapes_are_adjacent(shapes):
    pairs = combinations(shapes, 2)
    for shape_1, shape_2 in pairs:
        if shape_inside_shape(shape_1, shape_2):
            return True
    return False


def position_inside_shape(position, shape):
    return all([p1 >= p2 for p1, p2 in zip(position, shape.position)]) and \
           all([p1 <= p2 for p1, p2 in zip(position, np.add(shape.position, shape.bounding_box))])


def shape_inside_shape(shape_a, shape_b):
    positions = shape_a.translated_points()
    return any(map(lambda position: position_inside_shape(position, shape_b), positions))
