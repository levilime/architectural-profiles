from functools import reduce
from itertools import product

import numpy as np
from solving.util import transform_meta_assignment_placement_with_position, dimensional_dict_to_tuple, \
    is_negative_dimension, dimensional_tuple_to_dict, invert_dimension, invert_if_negative, \
    objects_with_id_field_to_dict, dimension_order, merge_dicts


def create_tiles_and_categories(tiles):
    lines = []
    lines.append("%tile(ID).\n%category(ID, CATEGORY).")
    for tile in list(tiles.values()):
        # define tile
        lines.append("tile(" + str(tile.id) + ").")
        # define categories
        for category in tile.categories:
            lines.append("category(" + ",".join([str(tile.id)] + [category]) + ").")
    return "\n".join(lines) + "\n"


def create_adjacencies(adjacencies, type):
    lines = []
    lines.append("%adjacencies for Type: " + type + ".")
    lines.append("%adjacency(Type, ID1, ID2, D, Rx, Ry, Rz).")
    for tile_id in adjacencies:
        for dimension in adjacencies[tile_id]:
            for adjacent_tile_tuple in adjacencies[tile_id][dimension]:
                lines.append("adjacency(" + ",".join([type, str(tile_id),  str(adjacent_tile_tuple[0]),
                                                      convert_dimension_to_minus_notation(dimension)]) + ","
                             + ",".join(list(map(str, adjacent_tile_tuple))[1:]) + ").")
    return "\n".join(lines) + "\n"


# def create_entrance_directions(tiles):
#     lines = []
#     for k in tiles:
#         tile = tiles[k]
#         for t in tile.entrance_adjacencies:
#             lines.extend([f"entrancedirection({k}, {t}, {convert_dimension_to_minus_notation(d)})."
#                           for d in tile.entrance_adjacencies[t]])
#     return "\n".join(lines) + "\n"


def create_connectivities_with_range(connectivities):
    # Type, CategoryFrom, CategoryThrough, CategoryTo, Direction, MinD, MaxD
    lines = []
    lines.append("% connectivities")
    if len(connectivities) == 0:
        return "% no connectivities \n"
    max_int = int(np.max([connectivity.length[1] for connectivity in connectivities]))
    lines.append(f"connectivityrangenums(0..{max_int}).")
    for connectivity in connectivities:
        lines.append(f"requireddistance({connectivity.type},{connectivity.from_c[0]},"
                     f"{connectivity.through_c[0]}, {connectivity.to_c[0]}, {connectivity.length[0]}, "
                     f"{connectivity.length[1]}).")
        lines.append(f"relevantthroughcategory({connectivity.through_c[0]}).")
        lines.append(f"connectivitytype({connectivity.type}).")
    return "\n".join(lines) + "\n"


def ground_possibilities_closure_func(ll):
    only_unique_list = list(set(ll))
    d = reduce(lambda agg, e: dict(agg, **{str(e[1]): e[0]}), enumerate(only_unique_list), {})
    return lambda e: d[str(e)]


def add_meta_dimensions(block_size, neighbor_assignments):
    constraints = ""
    for relative_position in neighbor_assignments:
        start = transform_meta_assignment_placement_with_position(block_size, (0,0,0), relative_position)
        end = transform_meta_assignment_placement_with_position(block_size,
                                                                [i - 1 for i in dimensional_dict_to_tuple(block_size)], relative_position)
        constraints += "cell(" + ",".join([str(t[0]) + ".." + str(t[1]) for t in zip(start, end)]) +").\n"
    return constraints


def add_dimensions_to_file(current_blocks, block_size, boundary_expansion={}, null_cells=[]):
    lines = []
    # if len(null_cells):
    #     lines.append("% null cells exist or current_blocks, boundary expansion is ignored with null cells.")
    #     null_cells_set = set(null_cells)
    #     for index in product(*[range(0, block_size[k]) for k in dimension_order]):
    #         if index not in null_cells_set:
    #             lines.append(f"cell" + str(index) + ".")
    #             lines.append(f"currentblock" + ",".join(map(str, [0] + list(index))) + ".")

    if len(current_blocks):
        def add_boundary_expansion(d, current_relative_block_index):
            return (boundary_expansion[current_relative_block_index][d] if d in boundary_expansion[current_relative_block_index] else 0) \
                    * (-1 if is_negative_dimension(d) else 1)

        for i, block in enumerate(current_blocks):
            block_to_d = dimensional_tuple_to_dict(block)
            ranges = [(block_to_d[d] * block_size[d] + add_boundary_expansion(invert_dimension(d), block),
                       add_boundary_expansion(d, block) + (block_to_d[d] + 1) * block_size[d] - 1) for d in
                                   block_size]
            printed_ranges = tuple(["..".join([str(low), str(high)]) for low, high in ranges])
            lines.append("cell(" + ",".join(printed_ranges) + "). \n"
                         "currentblock(" + ",".join([str(i)] + list(printed_ranges)) + ").")
    return "\n".join(lines) + "\n"

def convert_tuple_to_placement_constraint(t):
    return {"x": t[0], "y": t[1], "z": t[2], "texture": t[3]}

def create_placement_constraints(placement_constraints):
    constraints = ""
    for pc in placement_constraints:
        constraints += ":- assign(" + ",".join([str(pc["x"]), str(pc["y"]), str(pc["z"]), str(pc["texture"])]) \
                       + ")." + "\n"
    return constraints


def convert_dimension_to_minus_notation(direction):
    return ("minus" if is_negative_dimension(direction) else "") + invert_if_negative(direction)


def create_neighbor_adjacency_information(indexed_indices, neighbor_adjacencies):
    constraints = ""
    for count, index in indexed_indices:
        for na in neighbor_adjacencies[index]:
            constraints += "adjacentblockneighbor(" + str(count) + "," + convert_dimension_to_minus_notation(
                na) + ").\n"
    return constraints


def convert_dimension_to_clingo_coordinate_system(direction):
    if not invert_if_negative(direction) == "y" :
        return invert_dimension(direction)
    return direction


def create_all_connected(profile):
    lines = []
    lines.append("% all connected constraints, tiles with these categories need to be connected through the adjacency type"
                 "\n% over the entire block")
    added_types = set()
    for all_connected in profile.all_connected:
        level = all_connected.level if all_connected.level > 1 else ""
        lines.append(f"all{level}connected({all_connected.type}, {all_connected.category}).")
        added_types.add(all_connected.category)
    lines.extend(add_relevant_connectivity_types(added_types))
    return "\n".join(lines) + "\n"


def create_simple_connected(profile):
    lines = []
    lines.append("% simple connected")
    added_types = set()
    for all_connected in profile.all_connected:
        lines.append(f"simpleallconnected({all_connected.type}, {all_connected.category}).")
        added_types.add(all_connected.category)
    lines.extend(add_relevant_connectivity_types(added_types))
    return "\n".join(lines) + "\n"


def hard_override(profile):
    if profile.hard_override:
        return "hardoverride.\n"
    else:
        return "softoverride.\n"


def create_constraints_block_at_ending_side(cut_off):
    lines = []
    # add dimensions that need to properly be cut off at the block boundary
    added_types = set()
    lines.extend(add_relevant_connectivity_types(added_types))
    for cutoff in cut_off.cutoffs:
        for type_adjacency in cutoff.types:
            for category in cutoff.categories:
                lines.append(f"cutoff({type_adjacency}, {category}).")
                added_types.add(type_adjacency)
    lines.extend(add_relevant_connectivity_types(added_types))
    return "\n".join(lines) + "\n"


def add_relevant_connectivity_types(types):
    return [f"connectivitytype({type_c})." for type_c in types]


def create_density(profile):
    lines = []
    lines.append(f"% Density weights for categories.")
    for category in profile.density:
        weight = profile.density[category]
        lines.append(f"densityweight({category}, {weight}).")
    return "\n".join(lines) + "\n"


def create_positional_assignments(assignments, category):
    constraints = ""
    for assignment in assignments:
        joined_assignment = ",".join(list(map(str, assignment["position"])))
        # constraints += "override(" + joined_assignment + ").override" + category + "(" + joined_assignment + ").\n"
        constraints += "override(" + joined_assignment + ", " + category + ").\n" #  override" + category + "(" + joined_assignment + ").\n"
    return constraints


def create_metapositions(indexed_indices, metapositions):
    constraints = "% set metaposition if this block is the final edge of the solution in a certain direction\n"
    for count, index in indexed_indices:
        for metaposition in metapositions[index]:
            constraints += "metaposition(" + str(count) + "," + convert_dimension_to_minus_notation(metaposition) + ").\n"
    return constraints


def create_additional_constraints(additional_constraints):
    return additional_constraints.to_string()


def create_neighbor_match_constraints(constrained_cells, block_size):
    match_constraints = "% match with the cells of adjacent blocks. \n"

    def constraint_match(cell_index, neighbor_id, direction):
        return "boundarymatchobjective(" + ",".join([direction] +
                                                   [str(i) for i in list(cell_index)] + [neighbor_id]) +").\n"

    for cell_index in constrained_cells:
        for direction in constrained_cells[cell_index]:
            for texture in constrained_cells[cell_index][direction]:
                match_constraints += constraint_match(cell_index, str(texture.id),
                                                      convert_dimension_to_minus_notation(direction))
    return match_constraints


def create_full_neighborhood_block_constraints(neighbor_assignments, block_size):
    constraints = "% Assignments of already solved adjacent blocks that this block needs to unify with.\n"
    block_size_d = dimensional_dict_to_tuple(block_size)
    for current_block_index in neighbor_assignments:
        for local_neighbor_index in neighbor_assignments[current_block_index]:
            position = np.add(np.multiply(block_size_d, current_block_index),
                              np.multiply(block_size_d, local_neighbor_index))
            cells_dict = objects_with_id_field_to_dict(
                neighbor_assignments[current_block_index][local_neighbor_index].cells
            )
            for cell_index in cells_dict:
                cell_position = np.add(position, cell_index)
                i = cell_position
                tile = list(cells_dict[cell_index].contains)[0][0]
                rotation = list(cells_dict[cell_index].contains)[0][1:]
                constraints += create_assign(i, tile, rotation) + "\n"
                constraints += "cell(" + ",".join(map(str, tuple(i))) + ").\n"
    # for d in neighbor_assignments:
    #     constraints += "% at edge " + str(d) + "\n"
    #     for neighbor_assignment in neighbor_assignments[d]:
    #         i = neighbor_assignment["index"]
    #         tile = neighbor_assignment["tile"]
    #         rotation = neighbor_assignment["rotation"]
    #         constraints += create_assign(i, str(tile.id), rotation) + "\n"
    return constraints


def create_assign(index, tile_id, rotation):
    return "assign(" + ",".join(map(str, [*index, tile_id, *rotation])) \
                               + ")."


def create_assignments_multiple(assigns_d, block_size):
    lines = []
    for block_index in assigns_d:
        start_placement = np.multiply(block_index, block_size)
        lines.append(create_assignments(assigns_d[block_index], start_placement))
    return "\n".join(lines) + "\n"

def lines_to_string(lines):
    return "\n".join(lines) + "\n"

def create_assignments(assigns, start=(0,0,0)):
    constraints = []
    constraints.append("% hardcoded assignments, used for reflection of example testing.")
    for index in assigns:
        assign = assigns[index]
        tile_id = assign[0].id
        rotation = assign[1:]
        placement = np.add(start, index)
        constraints.append(create_assign(placement, tile_id, rotation))
    return "\n".join(constraints) + "\n"


def create_boundary_match_logic(exact_boundary_match):
    hard = "% hard constraint boundary match\n" + \
           ":- boundarymatchobjective(EdgeD, X,Y,Z, EdgeID), not 1 {boundarymatch(X,Y,Z)}.\n"
    soft = "% weak constraint boundary match\n" + \
           "#maximize { Y@2: texturematchonboundary(Y) }.\n"
    return hard if exact_boundary_match else soft


def create_blobs_to_side(blobs_to_side):
    lines = ["\n% certain blobs are forced to be connected to an edge of the solution."]
    unique_types = set()
    unique_categories = set()
    for connectivity in blobs_to_side:
        unique_types.add(connectivity["type"])
        unique_categories.add(connectivity["category"])
    lines += [f"connectivitytype({unique_type})."
              for unique_type in unique_types]
    lines += [f"relevantthroughcategory({unique_category})."
              for unique_category in unique_categories]

    return "\n".join(lines + ["blobtoside(" +",".join([b["type"], b["category"], convert_dimension_to_minus_notation(b["side"])])+ ")."
                              for b in blobs_to_side])


def create_connectivity_blobs(connectivity_blobs):
    """
    connectivities blobs
    :param connectivityblobs:
    :return:
    """

    connectivity_blobs = connectivity_blobs.blobs
    lines = []
    lines.append("% connectivity blobs")
    if len(connectivity_blobs) == 0:
        return "% no connectivity blobs \n"

    unique_types = set()
    unique_categories = set()
    for connectivity in connectivity_blobs:
        unique_types.add(connectivity.type)
        unique_categories.add(connectivity.category)
    lines += [f"connectivitytype({unique_type})."
              for unique_type in unique_types]
    lines += [f"relevantthroughcategory({unique_category})."
              for unique_category in unique_categories]
    max_int = int(np.max([np.max([connectivity.length[k] for k in list(filter(lambda x: x.startswith("max"), connectivity.length))])
                          for connectivity in connectivity_blobs]))
    lines.append(f"connectivityrangenums(0..{max_int}).")
    for connectivity in connectivity_blobs:
        type_c = connectivity.type
        category_c = connectivity.category
        if "minD" in connectivity.length and "maxD" in connectivity.length:
            minD = connectivity.length["minD"]
            maxD = connectivity.length["maxD"]
            lines.append(f"requireddistance({type_c}, {category_c}, {minD},{maxD}).")
        check_list = [b + a for a,b in product(["x", "y", "z"], ["minD", "maxD"])]
        if len([x for x in connectivity.length if x in check_list]) == 6:
            numbers = ", ".join([str(connectivity.length[k]) for k in check_list])
            lines.append(f"requireddistance({type_c}, {category_c}, {numbers}).")
    return "\n".join(lines) + "\n"


def create_cell_equals_with_block_position(cell_equals, block_index, block_size_t):
    lines = []
    lines.append("% enforce that two cells must be the same")
    block_translation = np.multiply(block_index, block_size_t)
    for index in cell_equals:
        for other_index in cell_equals[index]:
            index = tuple(np.add(block_translation, index))
            other_index = tuple(np.add(block_translation, other_index))
            lines.append(f"equalvalue(" + ",".join([str(x) for x in list(index) + list(other_index)]) + ").")
    return "\n".join(lines) + "\n"

def create_cell_equals(cell_equals):
    lines = []
    lines.append("% enforce that two cells must be the same")
    for index in cell_equals:
        for other_index in cell_equals[index]:
            lines.append(f"equalvalue(" + ",".join([str(x) for x in list(index) + list(other_index)]) + ").")
    return "\n".join(lines) + "\n"


def create_block_equals(block_size, equal_blocks):
    lines = ""
    block_pairs = reduce(lambda agg, ll: (agg[0] + [(agg[1], ll)], ll)
                         if agg[1] else ([], ll), equal_blocks, ([], None))[0]

    def create_cells_from_index(index):
        from itertools import product
        return list(product(*[range(block_size[d] * i, block_size[d] * i + block_size[d])
                for d, i in zip(dimension_order, index)]))
    for block_pair in block_pairs:
        collection = reduce(lambda agg, c: merge_dicts(agg, {c[0]: [c[1]]}),
                            zip(*map(create_cells_from_index, block_pair)), {})
        lines += create_cell_equals(collection) + "\n"
    return lines


def activate_tile_solving_mode():
    lines = []
    lines.append("tilesolvingmode.")
    return "\n".join(lines) + "\n"


def create_connectivity_through(connected_through):
    lines = []
    lines.append("% if blob A and blob C exist then there must be blob B connecting them")
    added_types = set()
    for through in connected_through:
        a = through.get("category_a")
        b = through.get("category_b")
        c = through.get("category_c")
        through_type = through.get("type")
        lines.append(f"blobtraversal({through_type}, {a}, {b}, {c}).")
        added_types.add(a)
        added_types.add(b)
        added_types.add(c)
    lines.extend(add_relevant_connectivity_types(added_types))
    return "\n".join(lines) + "\n"


def create_shape_definitions(shapes):
    lines = []
    lines.append("%shape definitions")
    for shape in shapes:
        lines.append(f"shape({shape.get_identifier()}, {shape.type}, {shape.category}, "
                     f"{','.join(map(str,shape.min_bounding_box))}, {','.join(map(str,shape.max_bounding_box))}).")
    return "\n".join(lines) + "\n"


def create_shape_adjacencies(shape_adjacencies):
    lines = []
    lines.append("%shape adjacencies")
    for shape_a, shape_b in shape_adjacencies:
        lines.append(f"shapeadjacency({shape_a.get_identifier()}, {shape_b.get_identifier()}).")
    return "\n".join(lines) + "\n"


def create_tile_entrances(tiles):
    return _create_tile_directions(tiles, lambda tile: tile.entrance_adjacencies, "tileentrance")


def create_tile_directions(tiles):
    return _create_tile_directions(tiles, lambda tile: tile.adjacencies, "tiledirection")


def _create_tile_directions(tiles, f, name):
    lines = []
    lines.append("%tile entrances")
    for tile in tiles.values():
        adjacencies = f(tile)
        for typ in adjacencies:
            for direction in adjacencies[typ]:
                lines.append(f"{name}({tile.id}, {typ}, {convert_dimension_to_minus_notation(direction)}).")
    return "\n".join(lines) + "\n"

def add_lines(lines):
    return "\n".join(lines) + "\n"
