import random
from itertools import product, islice


def fill_block_floor(block_shape , limit=None):
    d = {}
    full_indexes = list(product(range(0, block_shape[0]), range(0, block_shape[2])))
    for i_t in islice(full_indexes, limit) if limit else full_indexes:
        d[(i_t[0], 0, i_t[1])] = True
    return d

def fill_randomely(block_shape):
    d = {}
    full_indexes = list(product(range(0, block_shape[0]), range(0, block_shape[1]), range(0, block_shape[2])))
    for index in full_indexes:
        if random.random() > 0.5:
            d[index[0], index[1], index[2]] = True
    return d


def fill_all(block_shape):
    d = {}
    full_indexes = list(product(range(0, block_shape[0]), range(0, block_shape[1]),range(0, block_shape[2])))
    for i_t in full_indexes:
        d[(i_t[0], i_t[1], i_t[2])] = True
    return d


def fill_diagonally_upwards(block_shape):
    d = {}
    full_indexes = list(product(range(0, block_shape[0]), range(0, block_shape[1]),range(0, block_shape[2])))
    for i_t in full_indexes:
        if i_t[0]  > (i_t[1]) and i_t[2]  > (i_t[1]):
            d[(i_t[0], int(i_t[1]/2), i_t[2])] = True
    return d

def fill_wall(block_shape, limit=None):
    d = {}
    full_indexes = list(product(range(0, block_shape[0]), range(0, block_shape[2])))
    for i_t in islice(full_indexes, limit) if limit else full_indexes:
        d[0, i_t[0], i_t[1]] = True
    return d


def get_indices(x,y,z):
    return list(product(list(range(0,x)), list(range(0,y)), list(range(0,z))))