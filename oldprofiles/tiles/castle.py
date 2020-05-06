from oldprofiles.tiles.tiles import front_wall_side, floor, empty_space, straight_path, ceiling
import numpy as np

def double_wall_vertical_open(shape):
    A = front_wall_side(shape)
    return A + np.rot90(A, 2, (0,2))

def double_wall_closed_under(shape):
    return double_wall_vertical_open(shape) + floor(shape)

def double_wall_closed_above(shape):
    M = double_wall_vertical_open(shape)
    M[:, M.shape[1] - 1, :] = False
    # for i in range(0, M.shape[0]):
    #     if i % 2 > 0:
    #         M[i, M.shape[1] - 1, 0] = True
    #         M[i, M.shape[1] - 1, -1] = True
    M[:, int((M.shape[1] - 1)/2), :] = True
    return M


def double_wall_corner_vertical(shape):
    M = empty_space(shape)
    M = M + np.rot90(front_wall_side(shape), 3, (0,2)) + np.rot90(front_wall_side(shape), 2, (0,2))
    M[M.shape[0] - 1, :, 0] = True
    return M

def double_wall_corner_above(shape):
    M = double_wall_corner_vertical(shape)
    M[:, M.shape[1] - 1, :] = False
    M[:, int((M.shape[1] - 1)/2), :] = True
    # railing = empty_space(shape)
    # for i in range(0, M.shape[0]):
    #     if i % 2 == 0:
    #         M[i, M.shape[1] - 1, 0] = True
    #M + railing + np.rot90(railing, 1, (0,2))
    return M

def double_wall_corner_under(shape):
    return double_wall_corner_vertical(shape) + floor(shape)

def double_wall_gate(shape):
    M = np.rot90(double_wall_vertical_open(shape), 1, (0,2))
    M += ceiling(shape)
    M[:,:,0] = False
    M[:, :, -1] = False
    M += straight_path(shape)
    # M = M ^ front_wall_side(shape)
    return M
