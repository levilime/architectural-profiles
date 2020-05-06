import numpy as np
import math

x = 0
y = 1
z = 2


def empty_space(shape):
    return np.full(shape, False)


def filled_space(shape):
    return np.full(shape, True)


def filled_space_half(shape):
    M = empty_space(shape)
    A = np.full((shape[0], 1, shape[2]), False)
    A[:, 0, :] = ceiling_for_wall_between_inside_outside(shape)[:, shape[1] - 1, :]
    M[:, :, :] = A
    return M


def filled_space_quarter(shape):
    M = empty_space(shape)
    A = np.full((shape[0], 1, shape[2]), False)
    A[:, 0, :] = ceiling_inside_corner(shape)[:, shape[1] - 1, :]
    M[:, :, :] = A
    return M


def roof(shape):
    return empty_space(shape) + floor(shape)


def foundation(shape):
    return empty_space(shape) + ceiling(shape)


def floor(shape):
    M = empty_space(shape)
    M[:, 0, :] = True
    return M


def ceiling(shape):
    M = empty_space(shape)
    M[:, -1, :] = True
    return M


def floor_for_wall_between_inside_outside(shape):
    M = empty_space(shape)
    M[:, 0, 0:int(math.floor(M.shape[2] / 2)) + even_switch(M.shape[2])] = True
    return M


def floor_inside_corner(shape):
    M = empty_space(shape)
    M[0:int(math.floor(M.shape[0] / 2)) + even_switch(M.shape[0]), 0, 0:int(math.floor(M.shape[2] / 2)) + even_switch(M.shape[2])] = True
    return M


def ceiling_for_wall_between_inside_outside(shape):
    M = empty_space(shape)
    M[:, M.shape[1] - 1, 0:int(math.floor(M.shape[2] / 2))+ even_switch(M.shape[2])] = True
    return M


def ceiling_inside_corner(shape):
    M = empty_space(shape)
    M[0:int(math.floor(M.shape[0] / 2)) + even_switch(M.shape[0]), M.shape[1] - 1, 0:int(math.floor(M.shape[2] / 2))
                                                                                     + even_switch(M.shape[2])] = True
    return M


def floors_inside_corner(shape):
    return floor_inside_corner(shape) + ceiling_inside_corner(shape)


def corner(shape):
    M = empty_space(shape)
    M[0: int(math.floor(M.shape[0]/2)) + even_switch(M.shape[0]),
    :,
    0: int(math.floor(M.shape[2]/2)) + even_switch(M.shape[2])] = True

    M[0: int(math.floor(M.shape[0]/2)) + even_switch(M.shape[0]) - 1,
    :,
    0: int(math.floor(M.shape[2]/2)) + even_switch(M.shape[2]) - 1] = False
    return M


def front_wall(shape):
    return put_in_middle(shape, front_wall_f)


def front_wall_f(M, r):
    new_M = np.copy(M)
    new_M[:, :, r] = True
    return new_M


def front_wall_side(shape):
    return front_wall_f(empty_space(shape), range(0,1))


def front_wall_with_door_opening(shape):
    return put_in_middle(shape, front_wall_with_door_opening_f)


def front_wall_with_door_opening_f(M, r):
    new_M = front_wall_f(M, r)
    new_M[int(M.shape[0]/2) , 1: 3, :] = False
    return new_M


def front_wall_with_window(shape):
    return put_in_middle(shape, front_wall_with_window_f)


def front_wall_with_window_f(M, r):
    new_M = front_wall_f(M, r)
    new_M[int(M.shape[x]/2), int(M.shape[y]/2), :] = False
    return new_M


def put_in_middle(shape, wall_function):
    M = np.full(shape, False)
    new_M = wall_function(M, range(int(shape[2] / 2) - 1 + + even_switch(M.shape[0]), int(shape[2] / 2) + even_switch(M.shape[2])))
    return new_M


def straight_path(shape):
    M = empty_space(shape)
    M[math.floor(M.shape[0]/2), 0, :] = True
    return M


def x_path(shape):
    M = empty_space(shape)
    return straight_path(shape) + np.rot90(straight_path(shape), 1, (0, 2))


def corner_path(shape):
    M = empty_space(shape)
    M[:, 0, :] = corner(shape)[:, 0, :]
    return M


def t_path(shape):
    return corner_path(shape) + straight_path(shape)


def stairs(shape):
    return hardcoded_stairs(shape)


def stairs_under(shape):
    M = empty_space(shape)
    M[math.floor(M.shape[0] / 2), M.shape[1] - 1, 0] = True
    M[math.floor(M.shape[0] / 2), M.shape[1] - 1, 1] = True
    return M


def stairs_above_connector(shape):
    M = empty_space(shape)
    # M[math.floor(M.shape[0] / 2), 0, 0] = True
    M[math.floor(M.shape[0] / 2), 0, -1] = True
    return M


def hardcoded_stairs(shape):
    M = empty_space(shape)
    M[math.floor(M.shape[0] / 2), 0, 0] = True
    M[math.floor(M.shape[0] / 2), 0, 1] = True
    M[math.floor(M.shape[0] / 2), 1, 2] = True
    M[math.floor(M.shape[0] / 2), 2, 3] = True
    M[math.floor(M.shape[0] / 2), 3, 4] = True
    return M


def even_switch(number):
    return 0 if number % 2 == 0 else 1


def move_to_top(M, slice):
    M[:, M.shape[1] - 1, :] = slice
    return M
