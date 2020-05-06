from functools import reduce

from clingo.aspresult import SHAPE_PLACEMENT_ANNOTATION
from clingo.blocksolving import run_with_clingo_boundary_method
from constraints.declarativeconstraint import DeclarativeConstraints
from solving.blocksolver import BlockSolver, block_from_result, block_from_result_shape_annotation
import math

from solving.metadata import Metadata
from solving.util import merge_dicts


def solve_with_clingo(block_objectives: {str: BlockSolver}, metadata: Metadata={}, constraints=DeclarativeConstraints()) \
        -> {str: BlockSolver}:
    return solve_with_clingo_general(block_objectives,
                                     metadata,
                                     constraints=constraints,
                                     f=run_with_clingo_boundary_method)


def solve_with_clingo_general(block_objectives: {str: BlockSolver},
                              metadata: Metadata={},
                              constraints=DeclarativeConstraints(),
                              f=run_with_clingo_boundary_method) \
        -> {str: BlockSolver}:
    """
    Tile solving, clingo wrapper.

    :param self: the block
    :param metadata:
    Metadata contains per block information on information on the objective. Currently the following metadata is
    supported:
    {
    "neighbors": on what sides the block has an neighbor,
    "expanded_boundaries": on what side need the boundaries be expanded and by how much. Given as a dictionary
    with key the dimension and value a number. This denotes how much
    the block should be grown from the block size. {"-x":1, "y":1} would mean, add a slice to -x side and a slice to y.
    "exact_boundary_match: whether boundary matches of tiles of other block neigbors need to be exact or soft(maximized)."
    "profiles": overrides what profile is used in a block, overrides the global profile that is given.
    "rules": overrides what profile rules are used in a block, overrides global profile and profile override if given.
    "tiles": overrides what profile tiles are used in a block, overrides global profile and profile override if given.
    "meta_positions": the (semantic) position of the block in the entire solution
    }
    :param constraints: the rules of the profile. Can be overridden by profile in metadata or rules in metadata
    """
    if len(block_objectives) == 0:
        return block_objectives

    surroundings_to_parent = reduce(lambda agg, i: merge_dicts(agg,
                                                     {i: block_objectives[i].solved_neighbors}), block_objectives, {})
    result = f(block_objectives,
                 metadata,
                 surroundings_to_parent,
                 constraints, models=metadata.models if metadata else 1)

    # clingo returns: {x: y: z: rx: ry: rz: solution_id: }
    for block_objective_index in block_objectives:
        block_objective = block_objectives[block_objective_index]
        for solution in result.solutions:
            block_from_result(solution, block_objective, block_objective_index)
            metadata.shape_annotations = merge_dicts(metadata.shape_annotations, get_shape_annotations(solution))
            # block_from_result_shape_annotation(solution, block_objective, block_objective_index)
    return result

def solve_with_clingo_additional_constraints_closure(constraints):
    return lambda self, metadata={}: solve_with_clingo(self, metadata, constraints)


def flatten_index(x, y, z, block_size):
    return x + y * block_size["x"] + \
           z * block_size["x"] * block_size["y"]


def nested_index(i, block_size):
    return i % block_size["x"], math.floor(i / block_size["x"]) % block_size["y"], \
           math.floor(i / (block_size["x"] * block_size["y"])) % block_size["z"]

def get_shape_annotations(solution):
    clingo_computed_cells = solution.values
    computed_cells = [(cell["x"], cell["y"], cell["z"], cell[SHAPE_PLACEMENT_ANNOTATION])
                      for cell in clingo_computed_cells if SHAPE_PLACEMENT_ANNOTATION in cell]
    # here the cells are assigned their tile. Exploits impurity to set the tile in the cell object of the block
    shape_annotations_d = {}
    for entry in computed_cells:
        # get all entry parts, meaning the not the last element in the list, that will be the address
        shape_annotations_d = merge_dicts(shape_annotations_d, {entry[:3]: entry[3]})
    return shape_annotations_d