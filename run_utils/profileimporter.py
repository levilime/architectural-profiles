from functools import reduce

import numpy as np
import json

from run_utils.adjacencyfromexample import adjacencies_from_example
from profiles.profile import Profile
from solving.blocksolver import create_block_from_voxels
from solving.util import dimension_order_with_negative, deep_merge, merge_dicts
from tile.adjacency import Adjacencies, adjacencies_tile_ordered, get_entrance_adjacencies, Adjacency
from tile.allconnected import AllConnected
from tile.blobtoside import BlobsToSide
from tile.connectivity import Connectivities
from tile.connectivityblob import ConnectivityBlob, ConnectivityBlobs
from tile.connectivitythrough import ConnectivityThroughs
from tile.cutoff import CutOffs
from tile.purposefulshapeconnection import PurposefulShapeConnection
from tile.shapeadjacency import ShapeAdjacency
from tile.shapeadjacencyspecification import ShapeAdjacencySpecification
from tile.shapespecification import ShapeSpecification, create_specifications_from_json, order_shapes
from tile.tile import Tile
from voxels.magicavoxwrapper import import_voxel
import os.path
from voxels.magicavoxwrapper import visualize_voxel

SHAPE_DIRECTORY = 'tileshapes'
EMPTY_TILE = "void"

# SUBSET_ADJACENCIES = ["routing", "construction", "directconstruction"]
STRICT_ADJACENCY = "strict_adjacency"


def import_example_as_block(file_location, cell_size, profile, tile_exemption_allowed=True):
    return create_block_from_voxels(import_voxel(file_location), cell_size, profile, tile_exemption_allowed)


def import_shape(tileset_name, id):
    return import_voxel(os.path.join(SHAPE_DIRECTORY, tileset_name, id + '.vox'))


def import_example(tileset_name, name):
    return import_voxel(os.path.join(SHAPE_DIRECTORY, tileset_name, "examples", name + '.vox'))


def import_profile_from_file(profile_location, tileset_name, tile_size, get_tile_shape=None, get_examples=None):
    with open(profile_location, 'r') as f:
        profile_json = json.load(f)
    return import_profile(profile_json, tileset_name, tile_size, get_tile_shape, get_examples)

def create_all_possible_adjacencies(tiles):
    all_tile_signatures = ((k, 0, y, 0) for k in tiles for y in range(0,4))
    all_adjacencies = reduce(lambda agg, k: merge_dicts(agg, {k:Adjacency(tiles[k[0]], rotY=k[2])}),  all_tile_signatures, {})
    all_directions = ((k, d) for k in tiles for d in dimension_order_with_negative)
    d = reduce(lambda agg, t: deep_merge(agg, {t[0]: {t[1]: all_adjacencies}}),  all_directions, {})
    return d


def get_tiles(profile_json, tileset_name):
    serialized_tiles = profile_json.get("tiles", [])
    serialized_adjacencies = profile_json.get("adjacency", {})
    tile_dict = {}

    adjacencies_ordered_by_tile = adjacencies_tile_ordered(serialized_adjacencies)
    entrance_adjacencies = get_entrance_adjacencies(serialized_adjacencies)

    for serialized_tile in serialized_tiles:
        id = serialized_tile["id"]
        tile = Tile(id,
                    import_shape(tileset_name, id),
                    serialized_tile["categories"],
                    adjacencies_ordered_by_tile[id] if id in adjacencies_ordered_by_tile else {},
                    entrance_adjacencies[id] if id in entrance_adjacencies else {}
                    )
        tile_dict[id] = tile
    return tile_dict


# FIXME tileset_name should be an optional parameter
def import_profile(profile_json, tileset_name, tile_size, get_tile_shape=None, get_examples=None, omega_adjacency_mode=False):
    if not get_tile_shape:
        get_tile_shape = lambda id: import_shape(tileset_name, id)
    if not get_examples:
        get_examples = lambda profile_json: import_examples(profile_json, tileset_name)
    serialized_adjacencies = profile_json.get("adjacency", {})
    serialized_connectivities = profile_json.get("connectivity", {})
    serialized_all_connected = profile_json.get("allconnected", {})

    tile_dict = get_tiles(profile_json, tileset_name)

    adjacencies_from_file = Adjacencies(list(map(lambda k: tile_dict[k], tile_dict)), dimension_order_with_negative,
                              serialized_adjacencies, profile_json["empty_tile"])
    adjacencies_from_examples = {}
    tiles_for_example = reduce(lambda agg, id: merge_dicts(agg, {id: tile_dict[id]}), tile_dict, {})
    for example_voxels in get_examples(profile_json):
        adjacencies_from_examples = deep_merge(adjacencies_from_examples, adjacencies_from_example
        (tiles_for_example, tile_size, example_voxels, False))
    strict_adjacencies = deep_merge(adjacencies_from_file.strict_adjacencies, adjacencies_from_examples)

    if omega_adjacency_mode:
        strict_adjacencies = create_all_possible_adjacencies(tile_dict)

    additional_adjacencies = {}
    subset_adjacencies_types = filter(lambda type: type != STRICT_ADJACENCY, serialized_adjacencies)
    for type in subset_adjacencies_types:
        subset_adjacencies = Adjacencies.consume_subset_adjacencies(serialized_adjacencies[type],
                                                                    strict_adjacencies)
        additional_adjacencies[type] = subset_adjacencies
    connectivities = Connectivities(serialized_connectivities).get_all_routes()
    all_connected = AllConnected(serialized_all_connected)
    # info =  {"tiles": tile_dict, "adjacencies": adjacencies, "connectivities": connectivities}

    hard_override = "hard_override" in profile_json and not not profile_json["hard_override"]
    # cut off categories
    cut_off = CutOffs(profile_json.get("cutoff", []))
    connectivityblobs = ConnectivityBlobs(profile_json.get("blobs", []))
    density = profile_json.get("density", {})
    blobstoside = profile_json.get("blobstoside", [])
    connected_through = profile_json.get("through", [])
    empty_tile_id = profile_json["empty_tile"]

    profile = Profile(tile_dict,
                   strict_adjacencies,
                   connectivities,
                   all_connected.all_connected,
                   connectivityblobs,
                   blobstoside,
                   connected_through,
                   tile_dict[empty_tile_id],
                   additional_adjacencies,
                   hard_override,
                   cut_off,
                   density)

    all_adjacencies = []
    # for example_voxels in get_examples(profile_json):
    #     shapes = shapes_from_example(tiles_for_example, tile_size,
    #                                  example_voxels, [("routing", "interior"), ("routing", "exterior"),
    #                                                   ("construction", "built")
    #                                                   ])
    #
    #     complete_shapes = [shape for shape in shapes if shape.is_complete(profile)]
    #     adjacencies = adjacencies_in_shapes(profile, complete_shapes, ["routing", "construction"])
    #     # show
    #     # shapes = [shape for pair in merge_shape_adjacencies(adjacencies) for shape in pair]
    #     # for shapecollection in shapes:
    #     #     visualize_voxel(shapecollection.show(profile))
    #     # end show
    #     all_adjacencies = all_adjacencies + adjacencies
    # profile.shapes = reduce(lambda ll, pair: ll + [pair.shape_a, pair.shape_b], profile.shape_adjacencies, [])
    # profile.shape_adjacencies = merge_shape_adjacencies(all_adjacencies)

    profile.shapes = []

    # shapes = reduce(lambda agg, e: merge_dicts(agg, {e["id"]:
    #                             ShapeSpecification(e["id"], e["type"], e["category"], e["form"])}),
    #                 profile_json.get("shapes", []), {})
    shapes = create_specifications_from_json(profile_json)
    profile.shape_specifications = order_shapes(list(shapes.values()))
    shapes["ground"] = ShapeSpecification("ground", ["construction"], ["ground"], None)
    profile.shape_adjacencies = [ShapeAdjacencySpecification(e["type"], shapes[e["lhs"]], shapes[e["rhs"]]) for e in
                                 profile_json.get("shapeadjacencies", [])]
    profile.purposeful_shape_connections = [PurposefulShapeConnection(e["shape"], e["type"], e["amount"]) for e in
                                            profile_json.get("purposefulshapeconnection", [])]
    profile.active_shapes = profile_json.get("activeShapes", None)
    return profile


def import_examples(profile_json, tileset_name):
    return [import_example(tileset_name, example)
            for example in profile_json["adjacency"]["strict_adjacency"]["examples"]]


def import_examples_custom_location(typ, profile_json, location):
    return [import_example_custom_location(location, example)
            for example in profile_json["adjacency"]["strict_adjacency"][typ]]


def import_example_custom_location(location, name):
    return import_voxel(os.path.join(location, name + '.vox'))


def import_reflection_shapes(profile_json, tileset_name):
    return [import_example(tileset_name, example)
            for example in profile_json["adjacency"]["strict_adjacency"]["reflections"]]

def import_anti_reflection_shapes(profile_json, tileset_name):
    return [import_example(tileset_name, example)
            for example in profile_json["adjacency"]["strict_adjacency"]["antireflections"]]


def materialize_profile(profile, tileset_name):
    mat_tile_dict = materialize_tiles(tileset_name, profile.tiles)
    return profile.copy_profile_other_tiles(mat_tile_dict, mat_tile_dict[EMPTY_TILE])


def materialize_tiles(tileset_name, tile_dict):
    materialized_dict = {}
    for id in tile_dict:
        materialized_dict[id] = Tile(
            id,
            import_shape(tileset_name, id + "mat"),
            tile_dict[id].categories
        )
    return materialized_dict


