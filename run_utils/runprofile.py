import json
from functools import reduce

from oldprofiles.util import fill_diagonally_upwards, fill_all, fill_block_floor, get_indices, fill_randomely
from run_utils.profileimporter import import_profile, materialize_profile, import_reflection_shapes, import_anti_reflection_shapes
from run_utils.habitationresolver import habitation_resolver
from run_utils.reflectexample import reflects_examples
from solving.metadata import Metadata
from solving.util import dimensional_dict_to_tuple, dimension_order, deep_merge
from voxels.magicavoxwrapper import visualize_voxel


def run_profile_from_json(profile_json, grid_size, block_size, cell_size, test=True, metadata={}, models=0):
    profile = get_profile_from_json(profile_json, cell_size)
    # TODO test is at a weird position. should be in run_profile. This is done because examples are not yet registered in the profile class
    return run_profile(profile,
                       grid_size,
                       block_size,
                       cell_size,
                       import_reflection_shapes(profile_json, '5x4x5x') if test else [],
                       import_anti_reflection_shapes(profile_json, '5x4x5x') if test else [], metadata, None, models)


def get_profile_from_file(profile_location, cell_size):
    with open(profile_location, 'r') as f:
        profile_json = json.load(f)
    return get_profile_from_json(profile_json, cell_size)


def get_profile_from_json(profile_json, cell_size):
    cell_size_t = dimensional_dict_to_tuple(cell_size)
    profile = import_profile(profile_json, '5x4x5x', cell_size_t)
    return profile


def run_profile(profile, grid_size, block_size, cell_size,
                reflection_tests=[],
                anti_reflection_tests=[],
                input_metadata={},
                placement=None, models=0):
    if reflection_tests:
        assert(reflects_examples(profile, reflection_tests,
                                  cell_size, habitation_resolver, False, True))
    if anti_reflection_tests:
        assert(reflects_examples(profile, anti_reflection_tests,
                                 block_size, cell_size, True, True))

    block_equals = input_metadata["block_equals"] if "block_equals" in input_metadata else []
    null_blocks = input_metadata["null_blocks"] if "null_blocks" in input_metadata else []
    cell_equals = input_metadata["cell_equals"] if "cell_equals" in input_metadata else []
    null_cells = input_metadata["null_cells"] if "null_cells" in input_metadata else []

    grid_shape_as_tuple = tuple(map(lambda key: grid_size[key], dimension_order))
    # FIXME put materialized profile back on
    # materialized_profile = materialize_profile(profile, '5x4x5x')
    materialized_profile = profile
    placement = placement if placement else get_indices(*grid_shape_as_tuple)
    metadata = Metadata.resolve_metadata(materialized_profile, block_size, placement, block_equals, null_blocks,
                                         cell_equals, null_cells)
    metadata.models = models
    return habitation_resolver(materialized_profile, block_size, cell_size, placement, metadata, 15)


def get_metadata(profile, block_size, placement, metadata):
    materialized_profile = profile
    metadata = Metadata.resolve_metadata(materialized_profile, block_size, placement, metadata.equal_blocks)
    return metadata


def run_profile_from_file(profile_location, grid_size, block_size, cell_size, test=True, indexed_roadmap={}, models=0):
    with open(profile_location, 'r') as f:
        profile_json = json.load(f)
    return run_profile_from_json(profile_json, grid_size, block_size, cell_size, test, indexed_roadmap, models)
