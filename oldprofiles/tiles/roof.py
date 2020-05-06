from functools import reduce

from oldprofiles.tiles.tiles import empty_space

import numpy as np

def roof_template(shape):
    M = empty_space(shape)
    M[:, 0, :] = True
    M[:, 1, :] = True
    M[:, 2, :] = True
    return M


def roof_quarter_end(shape):
    M = empty_space(shape)
    M[:, 0, :] = True
    M[0:shape[0] - 1, 1, :] = True
    M[0:shape[0] - 2, 2, :] = True
    return M


def roof_half_middle(shape):
    M = empty_space(shape)
    M[:, 0, :] = True
    M[:, 1, 0:shape[2] - 1] = True
    M[:, 2, 0:shape[2] - 2] = True
    return M


def roof_middle(shape):
    M = empty_space(shape)
    M[:, 0, :] = True
    M[:, 1, :] = True
    M[:, 2, :] = True
    return M


def roof_one_direction(shape):
    M = empty_space(shape)
    M[:, 0, :] = True
    M[1:, 1, 1: shape[2] - 1] = True
    M[2:, 2, 2:shape[2] - 2] = True
    return M


def roof_full(shape):
    M = empty_space(shape)
    M[:, 0, :] = True
    M[1:shape[0] - 1, 1, 1: shape[2] - 1] = True
    M[2:shape[0] - 2, 2, 2:shape[2] - 2] = True
    return M

