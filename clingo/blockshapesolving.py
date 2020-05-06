from clingo.blocksolving import clingo_boundary_method_contraints
from clingo.call import call_clingo_for_multiple, call_gringo_clasp_combination
from clingo.constants import TEMPLATE_CLINGO_FILE_BOUNDARIES, CLINGO_FILE
from clingo.createtemplate import create_clingo_file
from clingo.shapeutil import add_placeable_shape, add_ground, add_air_shape, \
    add_specific_shape_adjacency, add_purposeful_shape_connection, add_close_on_types, add_required_shape_ids, \
    add_pulled_by_gravity_shape_reference, add_shape_occurences, \
    add_shape_connected, add_shape_annotations, add_shape_annotations_from_metadata
from clingo.util import *


def run_with_clingo_boundary_shape_method(block_objectives,
                                          metadata,
                                          surroundings,
                                          shape_granter,
                                          optimization=True,
                                          models=0,
                                          restart_on_model=False):
    expanded_boundaries = {}
    for i in block_objectives:
        expanded_boundaries[i] = block_objectives[i].expanded_boundaries

    def prepare_constraints(shape_granter):
        shapes = shape_granter()
        placeable_shapes, identifer_shapes = \
            tuple(zip(*[(add_placeable_shape(i, shape), (i, shape.name)) for i, shape in enumerate(shapes)]))
        shape_identifier_d = reduce(
            lambda agg, t: merge_dicts(agg, {t[1]: [t[0]] if t[1] not in agg else agg[t[1]] + [t[0]]}),
            identifer_shapes,
            {})
        constraint_list = [
            *clingo_boundary_method_contraints(block_objectives,
                                              metadata,
                                              surroundings,
                                              [],
                                              False),
            add_lines(placeable_shapes),
            add_lines(add_pulled_by_gravity_shape_reference(shapes)),
            add_lines(add_shape_occurences(shapes)),
            add_lines(add_shape_annotations(surroundings)),
            add_lines(add_shape_annotations_from_metadata(metadata.shape_annotations)),
            add_lines([add_specific_shape_adjacency(shape_adjacency, shape_identifier_d)
                       for shape_adjacency in metadata.profile.shape_adjacencies]),
            add_lines([add_purposeful_shape_connection(p) for p in metadata.profile.purposeful_shape_connections]),
            add_ground(),
            add_close_on_types(metadata),
            add_air_shape(),
            add_required_shape_ids(metadata.required_shapes),
            add_shape_connected(metadata.profile)
        ]
        constraints_for_clingo = reduce(lambda agg, c: agg + "\n" + c, constraint_list, "") + "\n"
        create_clingo_file(constraints_for_clingo, TEMPLATE_CLINGO_FILE_BOUNDARIES)
        return shapes

    if restart_on_model:
        shapes = prepare_constraints(shape_granter)
        for solution in call_gringo_clasp_combination(CLINGO_FILE, optimization, models):
            solving_statement(metadata.block_size, shapes)
            shapes = prepare_constraints(shape_granter)
            yield solution
    else:
        shapes = prepare_constraints(shape_granter)
        solving_statement(metadata.block_size, shapes)
        yield call_clingo_for_multiple(CLINGO_FILE, optimization, models)

def solving_statement(block_size, shapes):
    print(f"solving size {block_size} for shapes: {[(shape.name, shape.bounding_box) for shape in shapes]}")
