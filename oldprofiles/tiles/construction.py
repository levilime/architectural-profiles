from functools import reduce

from oldprofiles.tiles.tiles import empty_space

import numpy as np


def construction_pillar(shape):
    M = empty_space(shape)
    M[2, :, 2] = True
    return M


def quarter_construction_pillars(shape):
    return construction_pillar(shape)


def half_construction_pillars(shape):
    return construction_pillar(shape) + np.rot90(construction_pillar(shape), 1, (0, 2))


def all_construction_pillars(shape):
    return reduce(lambda M, rotation: M + np.rot90(construction_pillar(shape),
                                            rotation, (0, 2)), range(0,4), empty_space(shape))
