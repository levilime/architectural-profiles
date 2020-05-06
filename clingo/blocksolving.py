from clingo.call import call_clingo, call_clingo_for_multiple
from clingo.constants import TEMPLATE_CLINGO_FILE_BOUNDARIES, CLINGO_FILE
from clingo.createtemplate import create_clingo_file
from clingo.util import *
from constraints.declarativeconstraint import DeclarativeConstraints
from run_utils.runconfig import MANY_RUN
from solving.metadata import Metadata


def clingo_boundary_method_contraints(block_objectives,
                                    metadata: Metadata,
                                    surroundings,
                                    additional_constraints=DeclarativeConstraints(),
                                    multiple=MANY_RUN):
    block_indices = list(block_objectives)
    indexed_indices = list(enumerate(block_indices))
    block_size = metadata.block_size
    block_size_t = dimensional_dict_to_tuple(block_size)
    # expanded_boundaries = metadata.get_expanded_boundaries()
    null_cells = metadata.null_cells
    profile = metadata.profile
    meta_positions = metadata.metapositions
    block_equals = metadata.equal_blocks[list(block_objectives)[0]] if list(block_objectives)[
                                                                           0] in metadata.equal_blocks \
        else set()
    neighbor_directions = metadata.neighbor_adjacencies

    expanded_boundaries = {}
    for i in block_objectives:
        expanded_boundaries[i] = block_objectives[i].expanded_boundaries

    constraint_list = [
        add_dimensions_to_file(block_indices, block_size, expanded_boundaries, null_cells),
        # add_meta_dimensions(block_size, surroundings),
        create_tiles_and_categories(profile.tiles),
        create_tile_entrances(profile.tiles),
        create_tile_directions(profile.tiles),
        create_adjacencies(profile.adjacencies, "strict"),
        reduce(lambda agg, adjacency_sub_type: agg + "\n" +
                                               create_adjacencies(profile.additional_adjacencies[adjacency_sub_type],
                                                                  adjacency_sub_type),
               profile.additional_adjacencies, ""),
        # create_all_connected(profile),
        hard_override(profile),
        create_neighbor_adjacency_information(indexed_indices, neighbor_directions),
        # create_positional_assignments(filled_assigns, "filled"),# create_positional_assignments(filled_assigns, "filled"),
            lines_to_string([create_assign(tuple(np.add(np.multiply(block_size_t, block_index), i)), "void", (0,0,0))
             for block_index in metadata.null_cells
             for i in metadata.null_cells[block_index]]),
        create_metapositions(indexed_indices, meta_positions),
        create_constraints_block_at_ending_side(profile.cut_off),
        create_blobs_to_side(profile.blobs_to_side),
        create_connectivity_blobs(profile.connectivity_blobs),
        create_connectivity_through(profile.connected_through),
        create_assignments_multiple(metadata.cell_assigns, dimensional_dict_to_tuple(block_size))
        if metadata.cell_assigns else "",
        create_full_neighborhood_block_constraints(surroundings, block_size),
        create_density(profile),
        create_block_equals(block_size, block_equals),
        lines_to_string([create_cell_equals_with_block_position(metadata.equal_cells[i], i, block_size_t)
                         for i in block_indices if i in metadata.equal_cells])
    ]
    return constraint_list


def run_with_clingo_boundary_method(block_objectives,
                                    metadata,
                                    surroundings,
                                    additional_constraints=DeclarativeConstraints(),
                                    models=0):
    constraint_list = clingo_boundary_method_contraints(block_objectives,
                                    metadata,
                                    surroundings,
                                    additional_constraints,
                                    not not models) \
                      + [activate_tile_solving_mode()] + [create_simple_connected(metadata.profile)]
    constraints_for_clingo = reduce(lambda agg, c: agg + "\n" + c, constraint_list, "") + "\n"
    create_clingo_file(constraints_for_clingo, TEMPLATE_CLINGO_FILE_BOUNDARIES)
    return call_clingo(CLINGO_FILE, True) if not models else call_clingo_for_multiple(CLINGO_FILE,
                                                                                      False,
                                                                                      models)
