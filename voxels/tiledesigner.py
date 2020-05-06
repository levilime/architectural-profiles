import numpy as np
import math
from functools import reduce
import itertools

from voxels.tilecombiner import create_textures, only_corner_wall_textures

x = 0
y = 1
z = 2

class TileDesigner:
    # A cell is a voxel grid of booleans:
    # M = array([[[True, True],
    #         [False, False]],
    #        [[False, False],
    #         [False, False]]])
    # M[x,y,z]
    def __init__(self, shape):
        self.shape = shape