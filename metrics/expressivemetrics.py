import random
from functools import reduce
from itertools import product, combinations

from scipy.ndimage import convolve

import numpy as np
import networkx as nx

TILE_ROTATIONS = 4

from solving.blocksignature import BlockSignature
from solving.blocksolver import block_from_cells
from solving.util import breadth_first_search, breadth_first_search_for_graph, merge_dicts, create_tile_enum


def density_metric(block, empty_ids):
    total_tiles = len(block.cells)
    dense_tiles = reduce(lambda agg, cell: agg + 1 if list(cell.contains.values())[0].id in empty_ids else agg,
                         block.cells, 0)
    return (total_tiles - dense_tiles)/total_tiles


def variety_metric(block, profile, empty_ids=frozenset()):
    shapes_in_cells = block.get_shapes_in_block()
    shapes = [block_from_cells(shape_in_cells, profile, block.cell_size) for shape_in_cells in shapes_in_cells]
    signatures = [BlockSignature(BlockSignature.block_to_positioned_tiles(block)) for block in shapes]
    unique_signatures = reduce(lambda agg, s: agg if s in agg else agg + [s], signatures, [])
    unique_signatures_count = reduce(lambda agg, t: merge_dicts(agg, {t[0]: 0}), enumerate(unique_signatures), {})
    for s in signatures:
        index = unique_signatures.index(s)
        unique_signatures_count[index] += 1
    ignored_signatures = set([i for i, s in enumerate(unique_signatures)
                          if any((s.has_tile_id(empty_id) for empty_id in empty_ids))])
    ignored_tiles_amount = np.sum([unique_signatures_count[i] * len(unique_signatures[i].positioned_tiles)
                            for i in ignored_signatures])
    remaining_signatures_indices = set(unique_signatures_count).difference(ignored_signatures)
    components = [unique_signatures[i].amount_of_positions()/unique_signatures_count[i]
                  for i in remaining_signatures_indices]
    total_tiles = len(block.cells)
    return np.sum(components) / (total_tiles - ignored_tiles_amount)

# def self_similarity(block, profile):
#     signature = BlockSignature(BlockSignature.block_to_positioned_tiles(block))
#     M = signature.to_matrix_representation(profile)
#

def repetition_metric(block, profile, empty_ids=frozenset()):
    signature = BlockSignature(BlockSignature.block_to_positioned_tiles(block))
    M = signature.to_matrix_representation(profile)
    all_tiles = list(profile.tiles.values())
    relevant_tiles = (t for t in all_tiles if t.id not in empty_ids)
    not_relevant_tiles = (t for t in all_tiles if t.id in empty_ids)
    tile_enum = create_tile_enum(profile)
    all_tiles_rotations = list(product(all_tiles, range(0, TILE_ROTATIONS)))
    tiles = list(product(relevant_tiles, range(0, TILE_ROTATIONS)))
    ignored_tiles = list(product(not_relevant_tiles, range(0, TILE_ROTATIONS)))
    
    def get_tile_placements(tile, rotation):
        return (M == (tile_enum[tile.id] * TILE_ROTATIONS + rotation)).astype(bool).astype(float)

    tile_occurences = reduce(lambda agg, t: merge_dicts(agg, {t: np.sum(get_tile_placements(*t))}), all_tiles_rotations
                             , {})
    tile_repetitions = {}
    #agg_M = np.full(np.array(M.shape), 0.0)
    for t in tiles:
        if tile_occurences[t] <= 0:
            continue
        M_t = get_tile_placements(*t)
        # agg_M += repetition_M * (1/tile_occurences[t])
        # def operator(ll):
        #    all_above_0 = list(filter(lambda x: not not x, ll))
        #    return np.average(all_above_0) if all_above_0 else 0.0
        tile_repetitions[t] = operate_on_repetition_matrix(get_repetition_matrix(M_t), np.max)
    # return a repetition number, which is the repetition of every tile and the weight given by the amount occurences.
    return np.sum([tile_repetitions[k] * tile_occurences[k] for k in tile_repetitions]) / \
           (np.sum((tile_occurences[k] for k in tile_repetitions))) # agg_M * (len(tiles) ** -1) * M.size ** -1
    # [tile_repetitions[k] for k in tile_repetitions]


def operate_on_repetition_matrix(M, operator):
    return operator(M.flatten()[1:])


def get_repetition_matrix(M):
    repetition_M = np.full(np.array(M.shape), 0.0)
    #max_M = np.full(np.array(M.shape), 0.0)
    for step in product(*(range(0, x) for x in M.shape)):
        step_kernel_size = np.array(step) + 1
        max_occurence_kernel_size = np.array([np.max(step) * 2 + 1] * len(M.shape))
        occurence_kernel = np.full(step_kernel_size, 0.0)
        # occurence_kernel[tuple([int(np.floor(x/2)) for x in occurence_kernel.shape])] = 0.5
        middle_max_occurence_kernel = tuple([int(np.floor(x / 2)) for x in max_occurence_kernel_size])
        occurence_kernel[(0, 0, 0)] = 0.5
        occurence_kernel[step] = 0.5
        max_occurence_kernel = np.full(max_occurence_kernel_size, 0)
        max_occurence_kernel[tuple(np.array(middle_max_occurence_kernel) + np.array(step))] = 1
        occ_M = np.floor(convolve(M, occurence_kernel, mode="constant"))
        max_occ_M = (convolve(M, max_occurence_kernel,
                              mode="constant", cval=- step_kernel_size.size) >= 1).astype(float)
        repetition_M[step] = (max(np.sum(occ_M) - 1, 0)) / (np.sum(max_occ_M) - 1) if np.sum(max_occ_M) - 1 > 0 else 0.0
        # max_M[step] = np.sum(max_occ_M)
    relevant_M = repetition_M # repetition_M[np.ix_(*[range(0, int(np.ceil(s/2))) for s in repetition_M.shape])]
    return relevant_M

def intricacy_metric(block, destination_ids):
    destination_positions = [cell.id for cell in block.cells
                             if any((cell.get_tile_in_contains().id == d for d in destination_ids))]


def density_metrics(blocks, empty_tiles):
    values = []
    for block in blocks:
        values.append(density_metric(block, empty_tiles))
    return values

def efficiency_metrics(graphs, dimensions=3):
    values = []
    for graph in graphs:
        values.append(efficiency_metric(graph, dimensions))
    return values

def efficiency_metric(graph, dimensions=3):
    """
    take p most outside points and the most inside point.
    em = 1/|p|\sum(direct_path/ shortest_path)
    :param graph:
    :return:
    """
    nodes = list(graph.nodes)
    def compare_f(checks):
        comparator = lambda x, y: len(list(filter(lambda t: t[1] < t[2] if checks[t[0]] else t[1] > t[2],
                                                  zip(range(0, len(checks)), x,y)))) > 0
        # comparator() = lambda x, y: x < y if less else lambda x, y: x > y
        f = lambda y: lambda x: y if not x else (f(x) if comparator(x, y) else f(y))
        return f
    compare_functions = [compare_f(c) for c in product(*[[True, False]] * 3)]
    for node in nodes:
        compare_functions = [c(node) for c in compare_functions]
    boundary_points = [c(None) for c in compare_functions]
    values = []
    for t in combinations(boundary_points, 2):
        if nx.has_path(graph, *t):
            shortest_path = nx.shortest_path_length(graph, *t)
            if shortest_path > 0:
                values.append((int(np.sum(np.abs(np.subtract(*t)))), nx.shortest_path_length(graph, *t)))
    return reduce(lambda agg, t: agg + t[0]/t[1], values, 0)/len(values) if len(values) > 0 else 0

def blob_proportion_metric(graph, block, categories, dimensions=3, random_element_in_list=random.choice):
    # nodes = list(graph.nodes)
    # cells_d = block.get_cells_dict()
    #
    # def get_traversal_condition(category):
    #     def traversal_condition(position):
    #         return position in cells_d and category in cells_d[position].get_tile_in_contains()
    #     return traversal_condition
    #
    # def get_edges_f(g, category):
    #     def get_edges(node):
    #         return filter(lambda x: cells_d[node].get_tile_in_contains().one_of_categories_in_tile([category]),
    #                       g.edges(node))
    #     return get_edges
    #
    # relevant_positions = set()
    # for position in nodes:
    #     tile = cells_d[position].get_tile_in_contains()
    #     for category in categories:
    #         if category in tile.categories:
    #             relevant_positions = relevant_positions.union((position, category))
    #
    # unseen = set(relevant_positions)
    # groups = {}
    #
    # while not len(unseen) == 0:
    #     current = random_element_in_list(unseen)
    #     relevant_categories = set(categories).intersection(cells_d[current[0]].get_tile_in_contains().categories)
    #     for category in relevant_categories:
    #         group = breadth_first_search_for_graph(
    #             current[0], *[get_traversal_condition(category)] * 2, get_edges_f(graph, category))
    #         for position in group:
    #             unseen.remove((position, category))
    #         if category in groups:
    #             groups[category].append(group)
    #         else:
    #             groups[category] = [group]
    pass

def get_intricacy(graph, dimensions=3):
    def compare_f(checks):
        comparator = lambda x, y: len(list(filter(lambda t: t[1] < t[2] if checks[t[0]] else t[1] > t[2],
                                                  zip(range(0, len(checks)), x,y)))) > 0
        # comparator() = lambda x, y: x < y if less else lambda x, y: x > y
        f = lambda y: lambda x: y if not x else (f(x) if comparator(x, y) else f(y))
        return f
    compare_functions = [compare_f(c) for c in product(*[[True, False]] * 3)]
    for node in nodes:
        compare_functions = [c(node) for c in compare_functions]
    boundary_points = [c(None) for c in compare_functions]
    values = []
    for t in combinations(boundary_points, 2):
        if nx.has_path(graph, *t):
            shortest_path = nx.shortest_path_length(graph, *t)
            if shortest_path > 0:
                values.append((int(np.sum(np.abs(np.subtract(*t)))), nx.shortest_path_length(graph, *t)))
    return reduce(lambda agg, t: agg + t[0]/t[1], values, 0)/len(values) if len(values) > 0 else 0
