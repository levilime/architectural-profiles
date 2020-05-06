import json
import os
import pickle
import time
from functools import reduce
from itertools import product

from clingo.blockshapesolving import run_with_clingo_boundary_shape_method
from clingo.blocksolving import dimensional_tuple_to_dict
from clingo.clingosolver import solve_with_clingo, solve_with_clingo_general
from clingo.shapegeneration import get_shapes_from_generation
from constraints.declarativeconstraint import DeclarativeConstraints
from habitationresolver import habitation_resolver
from profileimporter import import_profile, import_reflection_shapes
from runprofile import get_metadata
from solving.blocksignature import BlockSignature, remove_duplicate_blocks
from solving.blocksolver import create_block_from_result, BlockSolver
from solving.metadata import Metadata
from solving.simplesolver import SimpleSolver
from solving.util import color_connected_parts, dimensional_dict_to_tuple, merge_dicts, dimension_order_with_negative, \
    convert_grid_shape_to_indices
from tile.shape import Shape, HeadShape, CombinedShape
from tile.shapespecification import ShapeSpecification, NonAtomicShapeSpecification
from voxels.magicavoxwrapper import visualize_voxel

input_size = {"x": 6, "y": 5, "z": 6}
cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_t = dimensional_dict_to_tuple(cell_size)

# MODELS_FOR_SHAPE_AMOUNT decides the number of models to find to fill in a certain shape size.
MODELS_FOR_SHAPE_AMOUNT = 1
MODELS_PER_SOLVE_STEP = 5
DUPLICATE_UNTIL_QUIT = 5
RESTART_ON_MODELS = True
CLOSED_TYPES_WHEN_SOLVING = [] #["routing", "construction"]

def generate_multiple_atomic(profile, shape_specification, size, show=False):
    def gen():
        for i in range(0, MODELS_FOR_SHAPE_AMOUNT):
            found_shapes = solve_atomic_shape(profile,
                                              shape_specification,
                                              cell_size,
                                              size,
                                              show)
            for shape in found_shapes:
                yield shape.to_block(profile)
    return (create_shape_from_specification_and_block(shape_specification, block, profile)
            for block in remove_duplicate_blocks(gen(), absolute_duplicate_occurrence_limit=DUPLICATE_UNTIL_QUIT))


def generate_shapes_in_profile(profile, cell_size, show=False):
    shape_collections = {}
    for shape_specification in profile.shape_specifications:
        possible_sizes = product(*[range(mi, ma + 1) for mi, ma in
                                   zip(shape_specification.form["min"],
                                       shape_specification.form["max"])])
        shapes = {}
        for size in possible_sizes:
            print(f"now calculating shapes of size: {size}")
            if type(shape_specification) == ShapeSpecification:
                # shapes_of_size = solve_atomic_shape(profile,
                #                                     shape_specification,
                #                                     cell_size,
                #                                     size,
                #                                     show)
                shapes_of_size = list(generate_multiple_atomic(profile, shape_specification, size, show))
            elif type(shape_specification) == NonAtomicShapeSpecification:
                shapes_of_size = solve_non_atomic_shape(profile,
                                                        shape_specification,
                                                        cell_size,
                                                        size,
                                                        shape_collections,
                                                        show)
            else:
                raise Exception("unsupported shape specification was given")
            if shapes_of_size:
                # raise Exception(f"no shapes exist for size: {size}")
                if not size in shapes:
                    shapes[size] = []
                shapes[size] += shapes_of_size
            shape_collections[shape_specification] = shapes
    flattened_shape_collection = [shape
                                  for shape_specification in shape_collections
                                  for size in shape_collections[shape_specification]
                                  for shape in shape_collections[shape_specification][size]]
    return flattened_shape_collection


def solve_non_atomic_shape(profile, non_atomic_shape_specification, cell_size, size, shape_collections, show=False):
    relevant_shapes = [shape
                          for shape_specification in shape_collections if shape_specification.name in
                          non_atomic_shape_specification.shapes
                          for size in shape_collections[shape_specification]
                          for shape in shape_collections[shape_specification][size]]
    metadata = Metadata(profile, dimensional_tuple_to_dict(size), {(0, 0, 0): dimension_order_with_negative}, *[[]] * 5,
                        closed_on_types=non_atomic_shape_specification.closed_types,
                        required_shapes=set([shape.name for shape in relevant_shapes]))
    created_blocks = generate_solutions(profile, relevant_shapes,
                                MODELS_FOR_SHAPE_AMOUNT,
                                False,
                                input_size=dimensional_tuple_to_dict(size),
                                metadata=metadata)
    if show:
        created_blocks = list(created_blocks)
        for block in created_blocks:
            visualize_voxel(block.show())
    signatures_with_duplicates = [BlockSignature(BlockSignature.block_to_positioned_tiles(block))
                                  for block in created_blocks]
    signatures = reduce(lambda agg, signature: agg if signature in agg else agg + [signature],
                        signatures_with_duplicates,
                        [])


    signatures_other_notation = [s.convert_to_dict_notation(profile.tiles) for s in signatures]
    # TODO instead of putting type and category directly, use shape specification inside shape
    shapes = [CombinedShape(signature_other_notation, name=non_atomic_shape_specification.name)
              for signature_other_notation in signatures_other_notation]
    # TODO remove duplication here and in solve atomic shape
    return shapes


def solve_atomic_shape(profile, shape_specification, cell_size, size, show=False):
    metadata = Metadata(profile, dimensional_tuple_to_dict(size), *[[]] * 6)
    result = get_shapes_from_generation(metadata, shape_specification, MODELS_PER_SOLVE_STEP)
    created_blocks = (create_block_from_result(solution, profile, cell_size) for solution in result.solutions)
    signatures_with_duplicates = [BlockSignature(BlockSignature.block_to_positioned_tiles(block))
                                  for block in created_blocks]
    signatures = reduce(lambda agg, signature: agg if signature in agg else agg + [signature],
                        signatures_with_duplicates,
                        [])
    signatures_other_notation = [s.convert_to_dict_notation(profile.tiles) for s in signatures]
    # TODO instead of putting type and category directly, use shape specification inside shape
    shapes = [Shape(signature_other_notation,
                          shape_specification.type[0],
                          shape_specification.category[0], name=shape_specification.name,
                    shape_metadata=shape_specification.shape_metadata)
                    for signature_other_notation in signatures_other_notation]
    for solution in result.solutions:
        created_block = create_block_from_result(solution, profile, cell_size)
        if show:
            visualize_voxel(created_block.show())
    return shapes


def create_shape_from_specification_and_block(shape_specification, block, profile):
    return Shape(BlockSignature(BlockSignature.block_to_positioned_tiles(block)).convert_to_dict_notation(profile.tiles),
                shape_specification.type[0],
                shape_specification.category[0], name=shape_specification.name,
                shape_metadata=shape_specification.shape_metadata)


def solve_input_with_shapes(input_size, profile, shapes, cell_size, metadata=None, models=1,
                            restart_on_models=RESTART_ON_MODELS, return_on_failure=True):
    if not metadata:
        metadata = Metadata(profile, input_size, {(0, 0, 0): dimension_order_with_negative}, *[[]] * 5,
                            closed_on_types=CLOSED_TYPES_WHEN_SOLVING)
    block = BlockSolver(input_size, cell_size, profile)
    result = run_with_clingo_boundary_shape_method({(0, 0, 0): block}, metadata, [], shapes, False, models,
                                                   restart_on_model=restart_on_models)
    if restart_on_models:
        for solution in result:
            yield solution
            if return_on_failure and not solution.solutions:
                print("generation failed and returns")
                break

    else:
        r = list(result)
        yield r[0]


def generate_solutions(profile, shapes, amount, restart_on_models, input_size,
                       duplicate_finish_count=False,
                       metadata=None):
    # print("solving for shapes:" + str([(shape.name, shape.get_bounding_box()) for shape in shapes]))
    print("solution size: " + str(input_size))
    results = solve_input_with_shapes(input_size, profile, shapes, cell_size, metadata, amount, restart_on_models)
    unique_blocks = remove_duplicate_blocks((create_block_from_result(solution, profile, cell_size)
                                             for result in results for solution in result.solutions),
                                            sorted=True, exit_on_subsequent_duplicate_count=duplicate_finish_count)
    return unique_blocks


def generate_solutions_in_blocks(profile, shapes, amount, restart_on_models, grid_size, block_size, metadata=None):

    solver = SimpleSolver(grid_size)
    indices = [block.id for block in solver.blocks]
    metadata = Metadata.resolve_metadata(profile, block_size, indices)

    def full_solver():
        def solver(block_objectives,
                   metadata,
                   surroundings_to_parent,
                   constraints,
                   models=1):
            result = list(run_with_clingo_boundary_shape_method(block_objectives,
                                                         metadata,
                                                         surroundings_to_parent,
                                                         shapes,
                                                         False, 1))[0]
            return result

        return lambda block_objectives: \
            solve_with_clingo_general(block_objectives, metadata, f=solver)

    solving_algo = full_solver()
    solved = solver.solve(solving_algo, block_size,
                          cell_size,
                          profile,
                          profile.empty_tile)
    # flatten blocks in one block
    # FIXME it is (ofcourse) really slow to first convert to voxel and then create a block from that
    return [solved.flatten_into_block()]


