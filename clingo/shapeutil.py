from solving.metadata import Metadata
from tile.purposefulshapeconnection import PurposefulShapeConnection
from tile.shape import Shape
from tile.shapeadjacency import ShapeAdjacency
from tile.shapeadjacencyspecification import ShapeAdjacencySpecification
from tile.shapespecification import ShapeSpecification


def create_shape_specification(ss:  ShapeSpecification):
    lines = []
    identifier = ss.name
    lines.append(f"shape({identifier}).")
    lines.extend([f"shapecategory({identifier}, {c})." for c in ss.category])
    lines.extend([f"shapetype({identifier}, {t})." for t in ss.type])
    return "\n".join(lines) + "\n"


def add_required_shape(ss: ShapeSpecification):
    lines = []
    lines.append(f"requiredshape(({ss.name}, (0,0,0))).")
    return "\n".join(lines) + "\n"


def add_required_shape_ids(ids: [str]):
    lines = []
    for name in ids:
        lines.append(f"requiredshapeid({name}).")
    return "\n".join(lines) + "\n"


def activate_shape_generator_mode():
    lines = []
    lines.append("shapegeneratormode.")
    return "\n".join(lines) + "\n"


def add_placeable_shape(identifier, shape: Shape):
    lines = []
    lines.append(f"shape({identifier}).")
    lines.append(f"shapecontainer({shape.name}, {identifier}).")
    lines.append(f"shapetype({identifier}, {shape.type}).")
    lines.append(f"shapecategory({identifier}, {shape.category}).")
    lines.extend([f"shapeposition({identifier}, "
                  f"{p}, "
                  f"{shape.tiles_at_position[p]['tile'].id},"
                  f"{shape.tiles_at_position[p]['rotY']})."
                  for p in shape.tiles_at_position])
    lines.append(f"shapedimensions({identifier}, ({','.join(map(str, shape.bounding_box))})).")
    return "\n".join(lines) + "\n"


def add_many_shape_adjacency(shape_adjacency: ShapeAdjacencySpecification):
    lines = []
    lines.append(f"manyshapeadjacencies("
                 f"{shape_adjacency.type},"
                 f"{shape_adjacency.shape_a.category[0]}, "
                 f"{shape_adjacency.shape_b.category[0]}).")
    return "\n".join(lines) + "\n"


def add_close_on_types(metadata: Metadata):
    return "\n".join([f"closedontype({t})." for t in metadata.closed_on_types]) + "\n"


def add_pulled_by_gravity_shape_reference(shapes):
    return [f"shapepulledbygravity({shape.name})." for shape in shapes if shape.shape_metadata.pulled_by_gravity]


def add_shape_occurences(shapes):
    return [f"shapeoccurence({shape.name}, " \
            f"({','.join(map(str, (max(n-1, 0) for n in shape.shape_metadata.occurence.grid)))}), " \
                f"({shape.shape_metadata.occurence.amount[0]}, {shape.shape_metadata.occurence.amount[1]}))."
            for shape in shapes if shape.shape_metadata.occurence]

def add_shape_annotations(surroundings):
    lines = []
    for current_block_index in surroundings:
        for local_neighbor_index in surroundings[current_block_index]:
            lines.extend([cell.shape_placement_annotation
                          for cell in surroundings[current_block_index][local_neighbor_index].cells
                          if hasattr(cell, "shape_placement_annotation")]
                         )
    return lines

def add_shape_annotations_from_metadata(shape_annotations):
    lines = []
    for k in shape_annotations:
        lines.append(shape_annotations[k])
    return lines

# def create_full_neighborhood_block_constraints(neighbor_assignments, block_size):
#     constraints = "% Assignments of already solved adjacent blocks that this block needs to unify with.\n"
#     block_size_d = dimensional_dict_to_tuple(block_size)
#     for current_block_index in neighbor_assignments:
#         for local_neighbor_index in neighbor_assignments[current_block_index]:
#             position = np.add(np.multiply(block_size_d, current_block_index),
#                               np.multiply(block_size_d, local_neighbor_index))
#             cells_dict = objects_with_id_field_to_dict(
#                 neighbor_assignments[current_block_index][local_neighbor_index].cells
#             )
#             for cell_index in cells_dict:
#                 cell_position = np.add(position, cell_index)
#                 i = cell_position
#                 tile = list(cells_dict[cell_index].contains)[0][0]
#                 rotation = list(cells_dict[cell_index].contains)[0][1:]
#                 constraints += create_assign(i, tile, rotation) + "\n"
#                 constraints += "cell(" + ",".join(map(str, tuple(i))) + ").\n"
    # for d in neighbor_assignments:
    #     constraints += "% at edge " + str(d) + "\n"
    #     for neighbor_assignment in neighbor_assignments[d]:
    #         i = neighbor_assignment["index"]
    #         tile = neighbor_assignment["tile"]
    #         rotation = neighbor_assignment["rotation"]
    #         constraints += create_assign(i, str(tile.id), rotation) + "\n"

def add_shape_connected(profile):
    lines = []
    lines.append("% shape connected")
    for all_connected in profile.all_connected:
        lines.append(f"shapeconnectedrequirement({all_connected.type}).")
    return "\n".join(lines) + "\n"

def add_entrance_amount(shape):
    return [f"shapeentrance({shape.name}, " \
            f"{min(shape.shape_metadata.entrance_amount)}," \
            f"{max(shape.shape_metadata.entrance_amount)})."] if shape.shape_metadata.entrance_amount else []

def add_vertical_entrance_allowance(shape):
    return [f"shapeentranceatheightlevel({shape.name}, " \
            f"{level})."
            for level in shape.shape_metadata.entrance_vertical_levels if shape.shape_metadata.entrance_vertical_levels]

def add_specific_shape_adjacency(shape_adjacency: ShapeAdjacencySpecification, d):
    lines = []
    for i in (d[shape_adjacency.shape_a.name] if shape_adjacency.shape_a.name in d else [shape_adjacency.shape_a.name]):
        for j in \
                (d[shape_adjacency.shape_b.name] if shape_adjacency.shape_b.name in d else [shape_adjacency.shape_b.name]):
            lines.append(f"shapeadjacency("
                         f"{i}, "
                         f"{j},"
                         f"{shape_adjacency.type}).")
    return "\n".join(lines) + "\n"


def add_purposeful_shape_connection(p: PurposefulShapeConnection):
    lines = []
    lines.append(f"purposefulshapeconnection("
                 f"{p.name}, "
                 f"{p.type},"
                 f"{p.amount}).")
    return "\n".join(lines) + "\n"


def add_ground():
    lines = []
    lines.append(f"shapetype(ground, construction)."
                 f"shapecategory(ground, ground).")
    return "\n".join(lines) + "\n"

def add_air_shape():
    return "\n".join(["shape(void).",
    "shapetype(void, construction).",
    "shapecategory(void, void).",
    "shapeposition(void, (0, 0, 0), void,0).",
    "shapedimensions(void, (1,1,1))."]) + "\n"
