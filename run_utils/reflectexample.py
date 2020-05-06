import numpy as np

from itertools import product
from run_utils.adjacencyfromexample import all_tiles_at_postions
from solving.blocksolver import create_block_from_result
from solving.metadata import Metadata
from solving.util import get_max_dimensions_indices, deep_merge, dimensional_dict_to_tuple, dimensional_tuple_to_dict
from voxels.magicavoxwrapper import visualize_voxel


def reflects_examples(profile, shapes, cell_size, solver, anti=False, visualize=False):
    """
    this method checks whether a profile can reproduce its examples.
    :param profile:
    :param shapes: for example: import_reflection_shapes(profile_json, tileset_name)
    :param block_size: how much cells fit in a block
    :param cell_size:
    :return:
    """
    # block_size_t = dimensional_dict_to_tuple(block_size)
    cell_size_t = dimensional_dict_to_tuple(cell_size)
    examples = [all_tiles_at_postions(example, cell_size_t, profile.tiles, False)
     for example in shapes]

    results = []
    for example, shape in zip(examples, shapes):
        if visualize:
            visualize_voxel(shape)
        indices = list(example)
        max_indices = get_max_dimensions_indices(indices)
        boundaries = [index + 1 for index in max_indices]
        block_size_t = choose_block_size(boundaries)
        blocks_amount = tuple([max(int(np.ceil((t[0]) / t[1])), 1) for t in zip(boundaries, block_size_t)])
        cells_in_shape = tuple([int(x1/x2) for x1,x2 in zip(reversed(shape.shape), cell_size_t)])
        block_size_example_t = tuple([min(x1, x2) for x1, x2 in zip(block_size_t, cells_in_shape)])

        assignments = {}
        for index in indices:
            tile = example[index]["tile"]
            rotY = example[index]["rotY"]
            block_position = tuple([int(np.floor(t[0] / t[1])) for t in zip(index, block_size_t)])
            relative_index = tuple([t[0] % t[1] for t in zip(index, block_size_t)])
            assignments = deep_merge(assignments, {
                block_position: {relative_index: (tile, *(0, rotY, 0))}
            })
            # if not "void" in tile.categories:
            #     assignments = deep_merge(assignments, {
            #         block_position: {
            #             "filled_assignment": {relative_index: True}
            #         }
            #     })
        indices = list(product(*[range(0, i) for i in blocks_amount]))
        metadata = Metadata.resolve_metadata(profile, dimensional_tuple_to_dict(block_size_example_t), indices)
        metadata.cell_assigns = assignments
        solution_size = dimensional_tuple_to_dict(block_size_example_t)
        result = solver(profile, solution_size, cell_size, indices, metadata)
        # result = habitation_resolver(profile, dimensional_tuple_to_dict(block_size_example_t), cell_size,
        #                             indices, metadata)

        if result.solutions:
            solution = create_block_from_result(result.solutions[0], profile, cell_size) # result

        else:
            results.append(False)
            continue

        if visualize:
            visualize_voxel(solution.show())

        def is_equal(shape, result):
            return np.sum(shape.astype(bool) ^ result.show()[tuple([slice(0, n)
                                                             for n in shape.shape])].astype(bool)) == 0
        results.append(is_equal(shape, solution))

    return len(list(filter(lambda x: x == anti, results))) == 0


def choose_block_size(cells_t):
    return tuple([[x for x in [3,4,5, cell_d] if cell_d % x == 0][0] for cell_d in cells_t])
