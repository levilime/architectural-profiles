import json
import math
import os
import pickle
import random
import time
from functools import reduce
from itertools import combinations, chain, product, combinations_with_replacement

import batch
from habitationresolver import habitation_resolver
from profileimporter import import_profile, import_reflection_shapes, import_anti_reflection_shapes
from reflectexample import reflects_examples
from shapegenerator import generate_shapes_in_profile, solve_input_with_shapes, generate_solutions, \
    generate_solutions_in_blocks
from solving.blocksignature import remove_duplicate_blocks
from solving.blocksolver import create_block_from_result
from solving.util import dimensional_dict_to_tuple, merge_dicts, deep_merge, create_shape_solve_combinations
from voxels.magicavoxwrapper import visualize_voxel, export

from datetime import date

cell_size = {"x": 5, "y": 4, "z": 5}
cell_size_t = dimensional_dict_to_tuple(cell_size)
block_size = {"x": 16, "y": 4, "z": 16}
input_size = block_size

AMOUNT_OF_RUNS = 100
DUPLICATE_FINISH_COUNT = 3
RANDOM_ORDER = False

date = date.today().strftime("%d%m%Y")

SHOW_GENERATED_SHAPES = False
MAX_SHAPES_PER_CONTAINER = 1
MAX_BLOCKS_IN_STORAGE = 1000

with open("../profiles/base/shapebasestairsstreetconstruction.json", 'r') as f:
    profile_json = json.load(f)

with open("../profiles/base/shapebaseroomonly.json", 'r') as f:
    only_room_profile_json = json.load(f)

with open("../profiles/util/noadjacencytest.json", 'r') as f:
    test_json = json.load(f)

reflection_tests = import_reflection_shapes(test_json, '5x4x5x')
anti_reflection_tests = import_anti_reflection_shapes(test_json, '5x4x5x')


def get_shapes_of_profile(profile, reset=True, show=False):
    if os.path.exists("amazingshapes.p") and not reset:
        with open("amazingshapes.p", "rb") as f:
            shapes = pickle.load(f)
    else:
        shapes = generate_shapes_in_profile(profile, cell_size, show)
        with open("amazingshapes.p", "wb") as f:
            pickle.dump(shapes, f)
    return shapes


profile = import_profile(profile_json, '5x4x5x', cell_size_t)

def solve(directory, profile, shapes, amount, restart_on_models, max_shapes_in_solver=None,duplicate_finish_count=0,
          block_mode=dict(), input_size=input_size):
    time_start = time.clock()
    # filter shapes according to active shapes
    relevant_shapes = [shape for shape in shapes
                       if not profile.active_shapes or shape.name in profile.active_shapes]

    all_relevant_shape_combinations = list(create_shape_solve_combinations(relevant_shapes, max_shapes_in_solver,
                                                                      MAX_SHAPES_PER_CONTAINER))
    def random_shape_granter():
        return random.choice(all_relevant_shape_combinations)

    # TODO instead make a generator that takes any size of shapes and outputs random ones given the constraint amount

    blocks = []
    if block_mode:
        grid_size = reduce(lambda agg, k: merge_dicts(agg, {k: math.floor(input_size[k]/block_mode[k])}),
                           block_mode,
                           {})
        chosen_shapes = random_shape_granter()
        unique_blocks = generate_solutions_in_blocks(profile,
                                                     lambda: chosen_shapes,
                                                     amount,
                                                     restart_on_models,
                                                     grid_size,
                                                     block_mode)
    else:
        unique_blocks = generate_solutions(profile,
                                           random_shape_granter,
                                           amount,
                                           restart_on_models,
                                           input_size,
                                           duplicate_finish_count)
    blocks = chain(blocks, unique_blocks)
    # blocks += list(unique_blocks)
    time_elapsed = (time.clock() - time_start)
    print(time_elapsed)

    # for i, result in enumerate(unique_blocks):
    #     visualize_voxel(result.show())

    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(directory + "/shapes"):
        os.makedirs(directory + "/shapes")
    for i, shape in enumerate(shapes):
        export(shape.show(profile), f"{directory}/shapes/{str(i)}{shape.name}.vox")
    for i, result in enumerate(remove_duplicate_blocks(blocks)):
        print(f"exporting shape run {i}")
        export(result.show(), f"{directory}/result{str(i)}.vox")
        # visualize_voxel(result.show())
    # # result = create_block_from_result(solution.solutions[0], profile, cell_size)


def create_from_profile(profile_json, extension_json_locations, directory, amount, reset=True,
                        restart_on_models=False, duplicate_finish_count=0,
                        block_mode=frozenset(), input_size=input_size):
    print(extension_json_locations)
    profile = merge_profile(profile_json, extension_json_locations)
    shapes = get_shapes_of_profile(profile, reset, SHOW_GENERATED_SHAPES)
    solve(directory, profile, shapes, amount, restart_on_models=restart_on_models,
          duplicate_finish_count=duplicate_finish_count, block_mode=block_mode, input_size=input_size)


# (profile, solution_size, cell_size, indices, metadata)
def solve_input_with_shapes_general_interface(shapes):
    def f(profile, solution_size, cell_size, indices, metadata):
        return solve_input_with_shapes(solution_size, profile, shapes, cell_size, metadata, 1)
    return f


def merge_profile(profile_json, extension_json_locations):
    extension_json = {}
    for e in extension_json_locations:
        with open(e, 'r') as f:
            extension_json = deep_merge(extension_json, json.load(f))
    profile = import_profile(merge_dicts(profile_json, extension_json), '5x4x5x', cell_size_t)
    return profile


#profile = merge_profile(profile_json, "profiles/nostreetadjacencies.json")
#shapes = get_shapes_of_profile(profile, True, False)
# assert(reflects_examples(profile, reflection_tests,
#       cell_size, solve_input_with_shapes_general_interface(shapes), False, True))
# assert(reflects_examples(profile, anti_reflection_tests,
#       cell_size, solve_input_with_shapes_general_interface(shapes), True, True))

# create_from_profile(profile_json, "profiles/nostreetadjacencies.json", "nostreetadjacencies", 10, False)


# create_from_profile(profile_json, "profiles/flathouses.json", "flathousestest", 1, False)
# create_from_profile(profile_json, "profiles/buildingsfarapart.json", "buildingsfaraparttest", 1000, True)
# create_from_profile(profile_json, "profiles/1storyhouses.json", "1storyhousesbignew", 1000)
# create_from_profile(profile_json, "profiles/highrise.json", "highrisebignew", 1000)
# create_from_profile(profile_json, "profiles/stackedrooms.json", "stackedroomsbignew", 1000)
# create_from_profile(profile_json, "profiles/roomsformingbuildings.json", "roomsformingbuildingsbignew", 1000)


# for e in random.sample(batch, len(batch.batch_list)) if RANDOM_ORDER else batch.batch_list:
#     create_from_profile(only_room_profile_json,
#                         e[0],
#                         e[1], AMOUNT_OF_RUNS, restart_on_models=True, reset=True,
#                         duplicate_finish_count=DUPLICATE_FINISH_COUNT)






#import os
#os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")