from functools import reduce

from solving.util import dimension_directions, deep_merge, invert_dimension
from tile.adjacency import add_addjacencies
from voxels.magicavoxwrapper import import_voxel
import math
from itertools import product
import numpy as np
from voxels.magicavoxwrapper import visualize_voxel

def adjacencies_from_example(tiles, shape, example, tile_exemption_allowed_mode=True):
    M = example
    # go over all tiles
    tiles_at_position = all_tiles_at_postions(M, shape, tiles, tile_exemption_allowed_mode)
    # extract the adjacencies
    new_adjacencies = {}
    for position in tiles_at_position:
        current_tile_comparison = tiles_at_position[position]
        tile = current_tile_comparison["tile"]
        for direction in dimension_directions:
            position_surrounding_tile = tuple(np.add(position, dimension_directions[direction]))
            if position_surrounding_tile in tiles_at_position:
                surrounding_tile_comparison = tiles_at_position[position_surrounding_tile]
                added_adjacencies = add_addjacencies(
                    tile, surrounding_tile_comparison["tile"], current_tile_comparison["rotY"], direction,
                    surrounding_tile_comparison["rotY"], invert_dimension(direction)
                )
                new_adjacencies = deep_merge(new_adjacencies, added_adjacencies)
    return new_adjacencies


def all_tiles_at_postions(M, shape, tiles, tile_exemption_allowed_mode):
    amount_tiles = [math.floor(M.shape[t[0]]/shape[t[0]]) for t in enumerate(M.shape)]
    tiles_at_position = {}

    # extract the tiles in the example
    for index in product(*[range(0, i) for i in amount_tiles]):
        current_tile = M[tuple([slice(int(c * shape[i]), int((1 + c) * shape[i]))
                 for i, c in enumerate(index)])]
        found_tile = find_tile_according_to_shape(current_tile, tiles)

        if not found_tile and not tile_exemption_allowed_mode:
            M_error = M.copy()
            M_error[tuple([slice(int(c * shape[i]), int((1 + c) * shape[i]))
                 for i, c in enumerate(index)])] = 22
            visualize_voxel(M_error)
            visualize_voxel(current_tile)
            raise Exception("the tile was not found in the dictionary")
        elif not found_tile:
            continue
        # flip y direction, because shape counts from top to bottom
        # also flip x and z
        changed_index = (index[2], (amount_tiles[1] - 1) - index[1], index[0])
        tiles_at_position[changed_index] = found_tile
    return tiles_at_position


def find_tile_according_to_shape(tile_shape, tiles, include_color=True, rotY=True, rotX = False, rotZ = False):
    """
    :param tile_shape: 
    :param tiles: 
    :param rotY: only supported
    :param rotX: currently not supported
    :param rotZ: currently not supported
    :return: 
    """
    used_type = int if include_color else bool
    tile_comparison_list = []
    for tile_key in tiles:
        tile = tiles[tile_key]
        tile_comparison_list += [{"tile": tile, "shape": np.rot90(tile.shape, i, (0,2)).astype(used_type), "rotY": i}
                                 for i in range(0,4)]
    comparable_tile_shape = tile_shape.astype(used_type)
    for tile_comparison in tile_comparison_list:
        if np.array_equal(tile_comparison["shape"], comparable_tile_shape):
            return tile_comparison
