import math
from functools import reduce
from itertools import product, combinations_with_replacement, combinations

import networkx as nx
import numpy as np
from solving.block import Block
from deepmerge import Merger
import random
import matplotlib.pyplot as plt

from voxels.magicavoxwrapper import visualize_voxel

dimension_order = ["x", "y", "z"]

dimension_order_with_negative = ["x", "-x", "y", "-y", "z", "-z"]
dimension_order_with_negative_2d = ["x", "-x", "z", "-z"]

dimension_index_values = {"x": (0 , 1), "-x": (0 , 0), "y": (1, 1), "-y": (1, 0), "z": (2, 1), "-z": (2, 0)}

dimension_directions = {"x": (1, 0, 0), "-x": (-1, 0, 0), "y": (0, 1, 0),
                        "-y": (0, -1, 0), "z": (0, 0, 1), "-z": (0, 0, -1)}

dimensions_directions_2d = {"x": (1, 0), "-x": (-1, 0), "z": (0, 1), "-z": (0, -1)}

inverted_dimension_directions = {}
for d in dimension_directions:
    inverted_dimension_directions[dimension_directions[d]] = d
inverted_dimension_directions_2d = {}
for d in dimensions_directions_2d:
    inverted_dimension_directions_2d[dimensions_directions_2d[d]] = d

#counterclockwise
# rotational_order = ["x", "z", "-x", "-z"]
# clockwise
rotational_order = ["x", "-z", "-x", "z"]

twod_sequential_dimension_order = ["x", "z"]

sequential_dimension_order = ["x", "y", "z"]
#sequential_dimension_order = ["z", "y", "x"]

x = 0
y = 1
z = 2


def serialize_direction_to_clingo(direction):
    if is_negative_dimension(direction):
        return "minus" + invert_dimension(direction)
    return direction


def get_rotated_dimension(start_dimension, amount_of_orthogonal_rotation):
    if not start_dimension in rotational_order:
        # y and -y remain the same after rotation along y axis
        return start_dimension
    index = (rotational_order.index(start_dimension) + amount_of_orthogonal_rotation) % len(rotational_order)
    return rotational_order[index]


def number_to_dimension_converter(number):
    return dimension_order[number]


def sequential_number_to_dimension_converter(number):
    """
    Used specifically for the conversion in _take_all_direction, because
    of the order and direction that function needs to correctly obtain the
    matrix result.
    """
    return sequential_dimension_order[number]


def horizontal_dimension_swap(d):
    if d == "x":
        return "z"
    if d == "z":
        return "x"
    return d


def number_to_dimension_converter_with_negative(number):
    return dimension_order_with_negative[number]


def dimension_to_number_converter(dimension):
    if is_negative_dimension(dimension):
        dimension = invert_dimension(dimension)
    return [t[0] for t in enumerate(dimension_order) if t[1] == dimension][0]


def is_negative_dimension(dimension):
    return dimension.startswith('-')


def invert_dimension(dimension):
    if is_negative_dimension(dimension):
        return dimension.replace('-', '')
    return '-' + dimension


def invert_if_negative(dimension):
    if is_negative_dimension(dimension):
        return invert_dimension(dimension)
    return dimension


def _take_all_direction(element, direction, show_function, temporary_option):
    """
    consumes a dimension each step and adds all the data within that dimension recursively together
    """
    array = None
    current_element = element
    while current_element is not None:
        proceeding_array = _take_all_direction(current_element, direction - 1, show_function, temporary_option) \
            if direction > 0 else show_function(current_element)
        order = (array, proceeding_array)
        if dimension_order[direction] == "x":
            order = (array, proceeding_array)
            concatenation_direction = 2
        if dimension_order[direction] == "y":
            order = (proceeding_array, array)
            concatenation_direction = 1
        if dimension_order[direction] == "z":
            order = (array, proceeding_array)
            concatenation_direction = 0
        array = np.concatenate(order,
                               axis=concatenation_direction
                               ) if array is not None else proceeding_array
        if dimension_order[direction] in current_element.neighbors:
            current_element = current_element.neighbors[dimension_order[direction]]
        else:
            current_element = None
    return array


def add_cell_indication(cell_position, voxels_amount, cell_size, value=True):
    m = np.full(voxels_amount, False)
    actual_size = tuple(np.subtract(cell_size, 1))
    corners = [tuple([cell_position[i] * cell_size[i] + (actual_size[i] if max_corner else 0)
                      for i, max_corner in enumerate(index)])
               for index in product(*[[False, True]]*3)]
    for corner in corners:
        # flip y axis
        m[corner[2], m.shape[1] - 1 - corner[1], corner[0]] = value
    return m


def change_voxels_according_to_cells(cell_positions, solution, cell_size, value=3):
    new_solution = np.copy(solution)
    # actual_size = tuple(np.subtract(cell_size, 1))
    max_y = int(solution.shape[1] / cell_size[1])
    for cell_position in cell_positions:
        cell_position = list(tuple(cell_position))
        cell_position[1] = (max_y - 1) - cell_position[1]
        cell_range = [range(cell_position[i] * cell_size[i], (cell_position[i] + 1) * cell_size[i])
                   for i in list(reversed(range(0,3)))]
        new_solution[np.ix_(*cell_range)] = solution[np.ix_(*cell_range)].astype(bool) * value
    return new_solution


def add_all_cell_indications(cell_positions, block_size, cell_size, value=True):
    complete_size = tuple(np.multiply(block_size, cell_size))
    m = np.full(complete_size, False)
    voxels_amount = np.multiply(block_size, cell_size)
    return reduce(lambda agg, cell_position: add_cell_indication(
        cell_position, voxels_amount, cell_size, value) + agg, cell_positions, m)


# TODO added temporary option as a hack, delete later and fix block and cell discrepancy
def get_filled_array_from_starting_block(element, dimension, show_function, temporary_option="cell"):
    """
    returns the data of all cells starting with the element starting cell in an matrix.
    """
    return _take_all_direction(element, dimension - 1, show_function, temporary_option)


def fill_all_cells(grid_shape, creation_function):
    all_possibilities = convert_grid_shape_to_indices(grid_shape)
    cells = []
    for index in all_possibilities:
        cells.append(creation_function(index))
    return cells


def convert_grid_shape_to_indices(grid_shape):
    return product(*map(lambda i: range(0, grid_shape[dimension_order[i]]), range(0, len(grid_shape))))


def fill_specific_cells(grid_shape, fill_indexes, creation_function, void_function):
    all_possibilities = convert_grid_shape_to_indices(grid_shape)
    # excluding_exisiting = filter(lambda possiblity: not possiblity in cell_indexes, all_possibilities)
    indexed_filled_indexes = {}
    for cell_index in fill_indexes:
        indexed_filled_indexes[cell_index] = True
    cells = []
    # create all cells
    for i, possibility in enumerate(all_possibilities):
        if possibility in indexed_filled_indexes:
            # if it is the objective to fill it
            cells.append(creation_function(possibility))
        else:
            # if it is should remain unfilled
            cells.append(void_function(possibility))
    return cells


def create_grid_with_cells_and_void(grid_shape, fill_indexes, creation_function, void_function):
    cells = fill_specific_cells(grid_shape, fill_indexes, creation_function, void_function)
    cells_dict = make_connections_between_grid_cells(grid_shape, cells)
    return cells


def create_grid(grid_shape, creation_function):
    """
    This is used to create a grid of elements where the elements
    have the neighbors property to specify their neighbors
    """
    # cells = fill_all_cells(grid_shape, creation_function)
    # cells_dict = make_connections_between_grid_cells(grid_shape, cells)
    # return cells

    positions = convert_grid_shape_to_indices(grid_shape)
    return create_grid_with_cells_and_void(grid_shape, positions, creation_function, None)


# FIXME this way of converting 1 dimensional index to grid with neighbors had a good run, but
# much more clear to use product for this
def make_connections_between_grid_cells(grid_shape, cells):
    # put the addresses of the neighbor cells in every cell

    # count order, first over x-axis, then y axis and lastly z-axis.
    # So first count the row going to the right at the bottom, then go one up and count this new row above the previous
    # one.
    # And when the last row at the top is reached, take the bottom row left to the bottom row that was counted first.
    # etc...
    cells_dict = reduce(lambda agg, cell: dict(agg, **{str(cell.id): cell}), cells, {})
    for cell in cells:
        index = cell.id
        neighbors = {}
        all_checks = [item for sublist in map(lambda i:
                                              [(i, dimension_order_with_negative[i * 2], 1),
                                               (i, dimension_order_with_negative[i * 2 + 1], -1)],
                                              range(0, len(grid_shape))) for item in sublist]
        for numbered_dimension, named_dimension, direction in all_checks:
            new_index = list(index)
            new_index[numbered_dimension] += direction
            if grid_shape[invert_if_negative(named_dimension)] > index[numbered_dimension] + direction >= 0:
                neighbors[named_dimension] = cells_dict[str(tuple(new_index))]
        cell.add_neighbors(neighbors)
    return cells_dict


# FIXME void_function should not be created here but given as a parameter from simplesolver
def create_grid_with_cells_and_void_closure(cell_indexes):
    """

    :param cell indexes denotes what cells need to be solved, the indices that are not named will not be solved,
     remain empty
    """
    return lambda grid_shape, creation_function: create_grid_with_cells_and_void(
        grid_shape, cell_indexes, creation_function, lambda i: Block(i, True))


def compare_textures(A, B):
    """
    take as reference the dimensions of A, get them by getting the edges keys of A
    (that contain the constraints of an edge)
    :param A: input texture
    :param B: texture to compare with
    :return: satisfiable constraints with as key the direction from A to B
    """
    dims = reduce(lambda agg, dim: agg + [(dim, invert_dimension(dim))], A.edges, [])
    constraints = {}
    # check for every dimension what constraints still hold relating to B
    for dim in dims:
        constraints[dim[0]] = check_constraint(A.edges[dim[0]], B.edges[dim[1]])
    return constraints


def check_constraint(sequence_a, sequence_b):
    """
    Check whether these two sequences are equal
    :param sequence_a:
    :param sequence_b:
    :return: True if the sequences are equal otherwise False
    """
    for i, a in enumerate(sequence_a):
        if not compare_elements(sequence_b[i], a):
            return False
    return True


def compare_elements(a, b):
    """
    Check whether these two 1 dimensional sequences are equal
    :param a:
    :param b:
    :return: True if the sequences are equal otherwise False
    """
    for i, x in enumerate(a):
        if not b[i] == x:
            return False
    return True


def dimensional_dict_to_tuple(d):
    return tuple([d[key] for key in dimension_order])


def dimensional_tuple_to_dict(t):
    return reduce(lambda agg, e: dict(agg, **{e[1]: t[e[0]]}), enumerate(dimension_order), {})


def objects_with_id_field_to_dict(objs):
    return reduce(lambda agg, obj: merge_dicts(agg, {obj.id: obj}), objs, {})


def incorporated(key, obj):
    return reduce(lambda agg, index: deep_merge(agg, {index:
                                                   {key: obj[
                                                       index]}}), obj, {})


def explode_tuple_in_3d_indexing(t):
    return t if len(t) == 3 \
        else (t[0], 0, t[1])


def explode_tuple_in_3d_shape(t):
    return t if len(t) == 3 \
        else (t[0], 1, t[1])


def merge_dicts(dict1, dict2):
    d = dict1.copy()
    d.update(dict2)
    return d


def group_to_dict(groups):
    return reduce(lambda agg, indices: merge_dicts(agg,
                                            reduce(lambda agg_2, index: merge_dicts(agg_2, {index: indices}), indices, {})),
           groups, {})


def deep_merge(dict1, dict2):
    my_merger = Merger(
        # pass in a list of tuple, with the
        # strategies you are looking to apply
        # to each type.
        [
            (list, ["append"]),
            (dict, ["merge"])
        ],
        # next, choose the fallback strategies,
        # applied to all other types:
        ["override"],
        # finally, choose the strategies in
        # the case where the types conflict:
        ["override"]
    )
    return my_merger.merge(dict1, dict2)


def deep_merge_override_list(dict1, dict2):
    my_merger = Merger(
        # pass in a list of tuple, with the
        # strategies you are looking to apply
        # to each type.
        [
            (list, ["override"]),
            (dict, ["merge"])
        ],
        # next, choose the fallback strategies,
        # applied to all other types:
        ["override"],
        # finally, choose the strategies in
        # the case where the types conflict:
        ["override"]
    )
    return my_merger.merge(dict1, dict2)


# def deep_merge(dict1, dict2):
#     if not isinstance(dict1, dict) and isinstance(dict2, dict):
#         return dict2
#     if isinstance(dict1, dict) and not isinstance(dict2, dict):
#         return dict1
#     if not isinstance(dict1, dict) and not isinstance(dict2, dict):
#         return dict1
#     new_dict = {}
#     unique_keys1 = [k for k in dict1 if k not in dict2]
#     unique_keys2 = [k for k in dict2 if k not in dict1]
#     shared_keys = [k for k in dict1 if k in dict2]
#     for k in unique_keys1:
#         new_dict = merge_dicts(new_dict, {k: dict1[k]})
#     for k in unique_keys2:
#         new_dict = merge_dicts(new_dict, {k: dict2[k]})
#     for k in shared_keys:
#         new_dict = merge_dicts(new_dict, {k: deep_merge(dict1[k], dict2[k])})
#     return new_dict


def transform_meta_assignment_placement_with_direction(block_size, index, d):
    # the direction the deplacement is in relative to the
    # current block. Add to the relevant dimension the block size
    return tuple([((-1 if is_negative_dimension(d) else 1) *
                   block_size[invert_if_negative(d)] if invert_if_negative(d) == dimension_order[i] else 0)
                  + e
                  for i, e in enumerate(index)])


def transform_meta_assignment_placement_with_position(block_size, index, position):
    # the direction the deplacement is in relative to the
    # current block. Add to the relevant dimension the block size
    return tuple(np.add(np.multiply(dimensional_dict_to_tuple(block_size), position), index))


def get_directly_surrounding_indices(dimensions):
    return get_adjacent_indices([0] * dimensions)


def get_max_dimensions_indices(ll):
    if len(ll) < 1:
        return ()
    boundaries = []
    for i in range(0, len(ll[0])):
        boundaries.append(np.max([t[i] for t in ll]))
    return tuple(boundaries)


def index_within_bounds(M, index):
    return len(list(filter(lambda t: t[1] >= M.shape[t[0]] or t[1] < 0, enumerate(index)))) <= 0


def breadth_first_search(start_position, traversal_condition, match_condition, directions):
    to_visit = {tuple(start_position)}
    visited = set()
    match = []
    while len(to_visit):
        current_position = to_visit.pop()
        visited.add(current_position)

        if traversal_condition(current_position):
            for direction in directions:
                new_position = tuple(map(lambda t: t[0] + t[1], zip(current_position, direction)))
                if new_position not in visited and new_position not in to_visit:
                    to_visit.add(new_position)
        if match_condition(current_position):
            match.append(current_position)
    return match


def unnest_list(ll):
    return [y for x in ll for y in x]


def breadth_first_search_for_graph(start_position, match_condition, direction_f, exit_condition=lambda match: False):
    to_visit = {start_position}
    visited = set()
    match = []
    while len(to_visit):
        current_position = to_visit.pop()
        visited.add(current_position)
        for new_position in direction_f(current_position):
            if new_position not in visited and new_position not in to_visit:
                to_visit.add(new_position)
        if match_condition(current_position):
            match.append(current_position)
        if exit_condition(current_position):
            return match
    return match


def random_color():
    return random.randint(1,200)


def color_connected_parts(matrix, color_func=random_color):
    M = np.array(matrix, dtype=bool)
    M_result = np.full(M.shape, 0)
    it = np.nditer(M, flags=['multi_index'])
    directions = [dimension_directions[k] for k in dimension_directions]
    while not it.finished:
        entry = it.multi_index
        if M_result[entry] == 0:
            pick_color = color_func()
            entries = breadth_first_search(entry, *[
                # check if index exists in array and check if cell is not colored
                                                    lambda index: len([True for x,y in zip(index, M.shape) if x >= y or x < 0]) < 1
                                                                 and M[index]] * 2,
                                           directions)
            for new_entry in entries:
                M_result[(new_entry)] = pick_color
        it.iternext()
    return M_result


def divide_into_parts(space, part_size):
    blocks = []
    parts = tuple([math.floor(s/p) for s,p in zip(space.shape, part_size)])
    for dims in product(*[range(0, d) for d in parts]):
        blocks.append(space[np.ix_(*[range(dims[i] * part_size[i],
                                           (dims[i] + 1) * part_size[i]) for i in range(0, len(space.shape))])])
    return blocks


def get_submatrix_centred_at_position(space, position, size):
    return space[np.ix_(*[range(
        max(0, position[i] - math.floor(size[i]/2)),
                          min(space.shape[i] - 1, position[i] + math.floor(size[i]/2) + 1))
        for i in range(0, len(space.shape))])], \
        [math.floor(s/2) + min(position[i] - math.floor(s/2), 0) for i, s in enumerate(size)]


def remove_matrix_duplicates(blocks):
    unique_blocks = []
    for block in blocks:
        if len([b for b in unique_blocks if np.sum(b - block) == 0]) == 0:
            unique_blocks.append(block)
    return unique_blocks


def numpy_lists_are_equal(l1, l2):
    return len(list(filter(lambda m: np.sum(m) > 0,
                [t[0] - t[1] for t in zip(l1, l2)]))) == 0


def get_block_solved_surrounding(block_position, blocks, level) -> dict:
    """
    :param current_position: position in the grid
    :param level: denotes how big the boundary should be:
    0 = only adjacent blocks
    1 = all directly surrounding blocks
    2, ... = blocks that are that amount of steps or less from the core block
    :return: dict with keys the relative index and as value the corresponding surrounding block
    """
    only_adjacent = False
    if level == 0:
        only_adjacent = True
        level = 1
    surroundings = {}
    for index in product(*[range(*[cp + change for change in [-1 * level, 1 * level + 1]]) for cp in block_position]):
        relative_index = np.subtract(index, block_position)
        if only_adjacent and np.sum(np.abs(relative_index)) > 1:
            # take only the directly adjacent blocks
            continue
        if index in blocks:
            current_block = blocks[index]
            if current_block.solution is not None:
                # if the solution is already created (and successful)
                surroundings[tuple(relative_index)] = blocks[index].solution
    return surroundings


def get_adjacent_indices(position):
    relative_positions = \
        [[int(math.pow(-1,  (i % 2))) if math.floor(i / 2) == x else 0
          for x in range(len(position))] for i in range(len(position) * 2)]
    return add_positions_together(position, relative_positions)


def get_adjacent_cell_positions(cell, type, entrance=True):
    return [tuple(np.add(cell.id, position)) for position in cell.possible_adjacency_positions(type, entrance)]


def add_positions_together(position, positions):
    return [np.add(position, other_position)
            for other_position in positions]




def is_in_range(position, box_position, box_size):
    """
    whether the given position, is within the bounding box defined by a
    start position box_position, and a bounding box size box_size

    :param position:
    :param box_position:
    :param box_size:
    :return:
    """
    start_of_box = box_position
    end_of_box = tuple(np.add(box_position, box_size))
    return len([i for i, least, most in zip(position, start_of_box, end_of_box) if
                least <= i < most]) == len(position)


def dict_to_group(data):
    seen = set()
    objectives = []
    for i in data:
        if seen.issuperset(set(data[i])):
            continue
        seen = seen.union(data[i])
        objectives.append(data[i])
    return objectives


def translated_dimension_directions(position):
    """

    :param position:
    :return: {direction: absolute position}
    """
    return reduce(lambda agg, d: merge_dicts(agg, {d: tuple(np.add(dimension_directions[d], position))}),
           dimension_directions, {})


def min_of_list(ll):
    return reduce(lambda p,c: np.minimum(p,c), ll)


def max_of_list(ll):
    return reduce(lambda p,c: np.maximum(p,c), ll)


def list_to_d(ll, *keys):
    return reduce(lambda agg, e: merge_dicts(agg, {tuple(map(lambda k: e[k], keys)): e}), ll, {})

def minimum_vector_of_list(elements):
    def minimum_between_two_vectors(a, b):
        smallest = None
        v = a
        for i,n in enumerate(a):
            if not smallest:
                smallest = n
            if smallest < n:
                smallest = n
                v = a
            if smallest < b[i]:
                smallest = b[i]
                v = b
        return v
    return reduce(minimum_between_two_vectors, elements)


# TODO this utility with many additional dependencies belongs somewhere else
def show_graph(graph, graph_title="graph"):
    plt.plot()
    plt.title(graph_title)
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()


def get_positions_including_adjacency_padding(placed_positions: set, cells_d, shape, entrance=False):
    """
    get the positions that can be traversed to from the current placed positions
    :return:
    """
    return reduce(lambda positions, position:
                  positions.union([position] + get_adjacency_padding(cells_d[position], shape.type, entrance))
                  , placed_positions, set())


def get_adjacency_padding(cell, t, entrance=False):
    if not cell.is_assigned():
        return []
    else:
        info = cell.get_tile_in_contains()
        tile, rotY = info["tile"], info["rotY"]
        return [tuple(np.add(cell.id, p)) for p in (tile.get_adjacencies_ommit_entrance(t, rotY) if not entrance else
        tile.get_adjacencies(t, rotY))]


def get_neighbor_adjacencies_from_metapositions(metapositions):
    return reduce(lambda agg, objective: merge_dicts(agg,
                                              {objective: set(dimension_order_with_negative).difference(
                                                  metapositions[objective])}),
           metapositions,
           {})


def create_tile_enum(profile):
    return reduce(lambda agg, t: merge_dicts(agg, {t[1]: t[0]}), enumerate(sorted(profile.tiles)), {})


def create_shape_solve_combinations(relevant_shapes, max_shapes_in_solver, max_shape_container_size):
    relevant_shape_combinations_grouped = reduce(lambda agg, shape:
                                                 merge_dicts(agg, {shape.name: (agg[shape.name]
                                                                                if shape.name in agg else []) + [shape]}
                                                             ), relevant_shapes, {})
    relevant_shape_combinations_ll = relevant_shape_combinations_grouped.values()

    splitted_by_max_shape_combinations = [[e for ll in nested_combination for e in ll]
                                          for nested_combination in product(*map(
        lambda ll: combinations(ll, min(len(ll), max_shape_container_size)),
        relevant_shape_combinations_ll))]

    all_relevant_shape_combinations = (
        combination
        for max_combination in splitted_by_max_shape_combinations
        for combination in combinations(max_combination,
                     min(max_shapes_in_solver, len(max_combination))
                     if max_shapes_in_solver
                     else len(max_combination)))
    return all_relevant_shape_combinations