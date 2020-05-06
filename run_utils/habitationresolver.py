import json

from run_utils.profileimporter import import_profile, materialize_profile
from clingo.clingosolver import solve_with_clingo_additional_constraints_closure
from solving.simplesolver import SimpleSolver
from solving.util import create_grid_with_cells_and_void_closure, convert_grid_shape_to_indices, \
    dimensional_dict_to_tuple, dict_to_group

import numpy as np

amount_voxels_per_dimension = 5

USE_EXACT_BLOCK_SOLVER = True

def habitation_resolver_reference_profile(habitation_profile,
                                          box_size,
                                          cell_size,
                                          placement,
                                          metadata,
                                          materialization):
    print("choose profile: " + habitation_profile)
    cell_size_to_tuple = dimensional_dict_to_tuple(cell_size)
    with open(f"profiles/{habitation_profile}.json", 'r') as f:
        profile_json = json.load(f)

    profile = import_profile(profile_json, '5x4x5x', cell_size_to_tuple)
    # TODO enable materializing profile again
    materialized_profile = materialize_profile(profile, '5x4x5x')
    return habitation_resolver(materialized_profile,
                       box_size, cell_size, placement, metadata)


def habitation_resolver(habitation_profile,
                        box_size,
                        cell_size,
                        placement,
                        metadata,
                        retries=0,
                        use_exact=USE_EXACT_BLOCK_SOLVER):
    """
    Interface for resolving an collection of box indices.
    :param habitation_profile:
    :param box_size:
    :param placement:
    :return:
    """
    if len(placement) < 1:
        return np.empty((0,0,0), dtype=int)

    solve_with_clingo = solve_with_clingo_additional_constraints_closure(habitation_profile.rules)

    def only_solve_if_no_void_block(solver):
        def f(block_objectives, metadata=metadata):
            if len([i for i in block_objectives if block_objectives[i].void]) > 0:
                for i in block_objectives:
                    block_objectives[i].successful = True
                return block_objectives
            else:
                return solver(block_objectives, metadata)
        return f

    solve_with_clingo_no_void = only_solve_if_no_void_block(solve_with_clingo)

    solving_algo = solve_with_clingo_no_void

    textures = list(habitation_profile.tiles.values())
    # to denote the bounding box of the solution in
    min_values = list(map(lambda i: np.min(list(map(lambda x: x[i], placement))), range(0, 3)))
    max_values = list(map(lambda i: np.max(list(map(lambda x: x[i], placement))), range(0, 3)))

    difference_values = np.subtract(max_values, min_values)

    relative_placement = [tuple(np.subtract(place_index, min_values)) for place_index in placement]

    create_grid = create_grid_with_cells_and_void_closure(relative_placement)

    solver = SimpleSolver({"x": difference_values[0] + 1, "y": difference_values[1] + 1, "z": difference_values[2] + 1},
                          create_grid, metadata, retries)

    if len(metadata.equal_blocks):
        solved = solver.solve_multiple(solving_algo, box_size,
                              cell_size,
                              habitation_profile,
                              habitation_profile.empty_tile,
                              dict_to_group(metadata.equal_blocks))
    else:
        solved = solver.solve(solving_algo, box_size,
                   cell_size,
                   habitation_profile,
                   habitation_profile.empty_tile,
                   relative_placement + [index for index in
                                convert_grid_shape_to_indices({"x": difference_values[0] + 1,
                                                               "y": difference_values[1] + 1,
                                                               "z": difference_values[2] + 1}) if index not in relative_placement],
                   True)

    # result = solved.show()
    return solved
