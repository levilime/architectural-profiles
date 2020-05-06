import numpy as np
from functools import reduce
import itertools


def all_rotations_on_y(M):
    return map(lambda i: np.rot90(np.copy(M), i, (0, 2)), range(0, 4))


def all_rotated_possibilities(wall_fronts):
    rotated_walls = map(lambda wall_front: list(all_rotations_on_y(wall_front)), wall_fronts)
    all_wall_combinations = itertools.product(*rotated_walls)
    wall_collection = []
    for wall_combination in all_wall_combinations:
        walls = [wall_combination[0],
                 wall_combination[0] + wall_combination[1],
                 wall_combination[0] + wall_combination[2],
                 wall_combination[0] + wall_combination[1] + wall_combination[2],
                 wall_combination[0] + wall_combination[1] + wall_combination[2] + wall_combination[3]]
        wall_collection += [reduce(lambda agg, wall: [*agg, *all_rotations_on_y(wall)], walls, [])]
    return wall_collection


def remove_duplicates(volumes, shape):
    return reduce(lambda agg, v1:
                  [*agg, v1] if len([v2 for v2 in agg
                                     if volume_equals(v2, v1, shape)]) < 1
                  else agg, volumes, [])


def volume_equals(A, B, shape):
    return np.alltrue(A ^ B ^ np.full(shape, True))


def create_textures(single, walls, finishes, shape):
    # single = [self.empty_space(), self.floor(), self.ceiling()]
    # walls = [self.front_wall(),
    #          self.front_wall_with_door_opening(),
    #          self.front_fence(),
    #          self.front_wall_with_window()]
    # finish = [self.fence_finish_front_left(), self.wall_finish_front_left(),
    #           self.ceiling_finish_front_left(),
    #           self.ceiling_finish_front_left() + self.fence_finish_front_left()]

    all_walls = all_rotated_possibilities(walls)
    # all_finishes = all_rotated_possibilities(finishes)

    flatten_dict_in_list = lambda ll: reduce(lambda agg, d: agg + [d.values()], ll, [])

    all_walls_flattened = flatten_dict_in_list(all_walls)
    # all_finishes_flattened = flatten_dict_in_list(all_finishes)

    combined_with_floor_ceiling = map(lambda v_t: v_t[0] + v_t[1],
                                      itertools.product(*[single, all_walls_flattened]))
    combined_with_floor_ceiling = remove_duplicates(combined_with_floor_ceiling, shape)
    # combined_with_finish = map(lambda v_t: v_t[0] + v_t[1], itertools.product(
    #     *[combined_with_floor_ceiling, all_finishes_flattened]))
    # return list(remove_duplicates(combined_with_finish))
    return list(remove_duplicates(combined_with_floor_ceiling))


def only_corner_wall_textures(walls, env):
    all_combinations = itertools.product(walls, walls)
    return reduce(
        lambda agg, wall_combination: agg + create_corner(wall_combination[0] + env, wall_combination[1] + env),
        all_combinations, [])


def twin_straight_wall_textures(walls, env):
    all_combinations = itertools.product(walls, walls)
    return reduce(
        lambda agg, wall_combination: agg + create_corner(wall_combination[0] + env, wall_combination[1] + env),
        all_combinations, [])


def create_corner(input_wall1, input_wall2):
    wall = input_wall1
    corner = wall + np.rot90(np.copy(input_wall2), 1, (0, 2))
    return list(all_rotations_on_y(corner))

def create_corners(walls):
    for possibility in possibility_map(2, walls):
        return create_corner(possibility[0], possibility[1])


def possibility_map(slots, elements):
    return itertools.product(*map(lambda i: elements, range(0, slots)))

def create_all_wall_possibilities(walls, env):
    elements = []
    for slot_combination in [combination for amount in range(1,5) for combination in itertools.combinations([0,1,2,3], amount)]:
        for wall_combination in possibility_map(len(slot_combination), walls):
            element = reduce(lambda agg, wall_slot_pair:
                agg + np.rot90(np.copy(wall_combination[wall_slot_pair[0]]), wall_slot_pair[1], (0, 2)),
                             enumerate(slot_combination), env)
            elements.append(element)
    return elements

def cut_tile_on_all_positive_sides(tile):
    B = np.full(list(map(lambda x: x - 1, tile.shape)), False, dtype=tile.dtype)
    B[0:B.shape[0], 0:B.shape[1], 0:B.shape[2]] = tile[0:B.shape[0], 0:B.shape[1], 0:B.shape[2]]
    return B
