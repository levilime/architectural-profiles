from functools import reduce

from solving.util import dimension_directions, get_rotated_dimension, merge_dicts
import numpy as np
import networkx as nx

from tile.adjacency import adjacency_two_tiles


def convert_to_graph(block, profile):
    # nodes = [cell.contains for cell in block.cells]
    cells_dict = reduce(lambda agg, cell: merge_dicts(agg, {cell.id: cell}), block.cells, {})
    edges = reduce(lambda agg, adj: merge_dicts(agg, {adj: []}), profile.additional_adjacencies, {})
    for cell in block.cells:
        tile = list(cell.contains.values())[0]
        tile_id = tuple(list(cell.contains)[0])
        rotation = tile_id[1:]
        for adjacency in tile.adjacencies:
            for dimension in tile.adjacencies[adjacency]:
                rotated_dimension = get_rotated_dimension(dimension, int(rotation[1]))
                neighbor_index = tuple(np.add(dimension_directions[rotated_dimension], cell.id).tolist())
                if neighbor_index in cells_dict:
                    neighbor = list(cells_dict[neighbor_index].contains)[0]
                    if adjacency_two_tiles(profile, tile_id, neighbor, rotated_dimension, adjacency):
                        edges[adjacency].append((cell.id, neighbor_index))

    graphs = {}
    # make different graphs for every adjacency subtype
    for adjacency_subtype in profile.additional_adjacencies:
        G = nx.Graph()
        # G.add_nodes_from([(*cell.id, list(cell.contains)[0][0]) for cell in block.cells])
        G.add_nodes_from([cell.id for cell in block.cells])
        G.add_edges_from([edge[:2] for edge in edges[adjacency_subtype]])
        graphs[adjacency_subtype] = G
    return graphs










