from functools import reduce

from clingo.call import call_clingo_for_multiple, call_clingo
from clingo.createtemplate import create_clingo_file
from clingo.shapeutil import create_shape_specification, add_required_shape, activate_shape_generator_mode, \
    add_entrance_amount, add_vertical_entrance_allowance
from clingo.util import *
from clingo.constants import TEMPLATE_CLINGO_FILE_BOUNDARIES, CLINGO_FILE
from solving.util import dimensional_dict_to_tuple, dimension_order_with_negative
from tile.shapespecification import ShapeSpecification


def get_shapes_from_generation(metadata, shape_specification: ShapeSpecification, model_amount=0):
    block_indices = [(0,0,0)]
    indexed_indices = list(enumerate(block_indices))
    # TODO make loop to go over all possible sizes between min and max
    block_size = metadata.block_size
    # expanded_boundaries = metadata.get_expanded_boundaries()
    profile = metadata.profile
    meta_positions = metadata.metapositions
    constraint_list = [
       add_dimensions_to_file(block_indices, block_size, {(0,0,0): {}}),
       create_tiles_and_categories(profile.tiles),
       create_tile_directions(profile.tiles),
       create_tile_entrances(profile.tiles),
       create_adjacencies(profile.adjacencies, "strict"),
       reduce(lambda agg, adjacency_sub_type: agg + "\n" +
                                              create_adjacencies(profile.additional_adjacencies[adjacency_sub_type],
                                                                 adjacency_sub_type),
              profile.additional_adjacencies, ""),
       create_simple_connected(profile),
       hard_override(profile),
       create_metapositions(indexed_indices, {(0,0,0): set(dimension_order_with_negative)}),
       create_constraints_block_at_ending_side(profile.cut_off),
       create_shape_specification(shape_specification),
        add_lines(add_entrance_amount(shape_specification)),
        add_lines(add_vertical_entrance_allowance(shape_specification)),
       add_required_shape(shape_specification),
       activate_shape_generator_mode(),
     ]
    constraints_for_clingo = reduce(lambda agg, c: agg + "\n" + c, constraint_list, "") + "\n"
    create_clingo_file(constraints_for_clingo, TEMPLATE_CLINGO_FILE_BOUNDARIES)
    return call_clingo_for_multiple(CLINGO_FILE, False, model_amount)
