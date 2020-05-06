import numpy as np

from oldprofiles.tiles.mountainvillage import front_wall, front_wall_with_window, front_wall_with_door


def small_nook(shape):
    return front_wall(shape) + np.rot90(front_wall(shape), 1, (0,2)) + np.rot90(front_wall(shape), - 1, (0,2))


def small_room(shape):
    return front_wall(shape) + np.rot90(front_wall(shape), 1, (0,2)) + np.rot90(front_wall(shape), 2, (0,2)) \
           + np.rot90(front_wall(shape), 3, (0,2))


def small_nook_with_door(shape):
    return front_wall_with_door(shape) + np.rot90(front_wall(shape), 1, (0, 2)) + np.rot90(front_wall(shape), - 1, (0, 2))

def small_nook_with_side_door(shape):
    return front_wall_with_window(shape) + np.rot90(front_wall_with_door(shape), 1, (0, 2)) + np.rot90(front_wall(shape), - 1, (0, 2))


def small_nook_with_window(shape):
    return front_wall_with_window(shape) + np.rot90(front_wall(shape), 1, (0, 2)) + np.rot90(front_wall(shape), - 1, (0, 2))


def small_room_with_door(shape):
    return front_wall_with_door(shape) + np.rot90(front_wall(shape), 1, (0,2)) + np.rot90(front_wall(shape), 2, (0,2)) \
           + np.rot90(front_wall(shape), 3, (0,2))
