import numpy as np
import math

from oldprofiles.tiles.tiles import empty_space, put_in_middle

x = 0
y = 1


def front_wall_template(shape):
    M = front_wall(shape)
    M += floor(shape)
    M += ceiling(shape)
    return M


def front_wall(shape):
    M = empty_space(shape)
    M[:, :, 0] = True
    return M


def front_wall_with_window(shape):
    M = front_wall(shape)
    M[int(M.shape[x] / 2), int(M.shape[y] / 2), :] = False
    return M


def front_wall_with_door(shape):
    M = front_wall(shape)
    M[int(M.shape[0] / 2), 1: 3, :] = False
    return M


def corner(shape):
    return front_wall(shape) + np.rot90(front_wall(shape), 1, (0,2))

def flipped_corner(shape):
    return np.flip(corner(shape), 0)


def front_fence(shape):
    M = front_wall(shape)
    M[:, 0: int(math.floor(shape[y]/2))] = False
    return M


def corner_fence(shape):
    return corner_fence(shape) + np.rot90(corner_fence(shape), 1, (0, 2))


def flipped_corner_fence(shape):
    return np.flip(corner_fence(shape), 0)


def floor(shape):
    M = empty_space(shape)
    M[:, 0, :] = True
    return M


def ceiling(shape):
    M = empty_space(shape)
    M[:, -1, :] = True
    return M

def stairs(shape):
    return hardcoded_stairs(shape)

def hardcoded_stairs(shape):
    M = empty_space(shape)
    M[:, 0, 0] = True
    M[:, 0, 1] = True
    M[:, 0:2, 2] = True
    M[:, 0:3, 3] = True
    M[:, 0:4, 4] = True
    return M


def stairs_above_connector(shape):
    M = empty_space(shape)
    M[:, 0, -1] = True
    return M

def front_wall_middle(shape):
    return put_in_middle(shape, front_wall_f)


def front_wall_f(M, r):
    new_M = np.copy(M)
    new_M[:, :, r] = True
    return new_M


def front_wall_with_door_opening_middle(shape):
    return put_in_middle(shape, front_wall_with_door_opening_f)

def front_wall_with_door_opening_f(M, r):
    new_M = front_wall_f(M, r)
    new_M[int(M.shape[0]/2) , 1: 3, :] = False
    return new_M
