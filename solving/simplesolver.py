from itertools import product

from profiles.profile import Profile
from solving.heuristicalblockssolver import solve_picking_randomely
from solving.logging.solvinglogger import SolvingLogger
from .block import Block
from .blocksolver import BlockSolver, create_block_from_voxels
from functools import reduce
from PIL import Image
from .util import create_grid, get_filled_array_from_starting_block, invert_dimension, dimension_order_with_negative, \
    dimension_directions, merge_dicts, objects_with_id_field_to_dict, color_connected_parts, random_color, \
    dimensional_dict_to_tuple
import numpy as np
import math
from voxels.magicavoxwrapper import visualize_voxel
import random

TEXTURE_CONSTRAINT_ORDER = ["x", "-x", "y", "-y", "z", "-z"] #["y", "-y"]# ["x", "-x", "y", "-y", "z", "-z"] # ["x", "-x", "z", "-z"]

MAX_RESTARTS = 1000
VISUALIZE_INTERMEDIATE_SUCCESS = False
VISUALIZE_FAILURE = False

class SimpleSolver:
    """
    Controls blocks
    """
    # grid size is the amount of blocks in every dimension in the grid (with blocks being a solved block entity)
    def __init__(self, grid_size, grid_creation_function=create_grid, block_args_dict = None,restarts=MAX_RESTARTS, random_solve_order=False):
        creation_function = lambda id: Block(id)
        self.grid_size = grid_size
        self.blocks = grid_creation_function(grid_size, creation_function)
        if block_args_dict:
            self.block_args_dict = block_args_dict
        self.restarts = restarts
        self.logger = SolvingLogger()
        self.solver_technique = self.solve_picking_randomely

    def is_void_block(self, block):
        return block.void

    def set_empty_block(self, block_size, cell_size, empty_tile):
        empty_block = SimpleSolver.fill_mocked_block_with_empty_tiles(block_size, cell_size, empty_tile)
        self.empty_block = empty_block

    @staticmethod
    def get_unique_blocks_from_multiple_block_collection_solve_order(multiple_block_collection_solve_order):
        return reduce(lambda agg, indices: agg.union(indices),
                                    multiple_block_collection_solve_order, set())

    @staticmethod
    def get_unique_blocks_from_multiple_block_collection_solve_order_labeled(multiple_block_collection_solve_order):
        return reduce(lambda agg, t: agg.union([(t[0], index) for index in t[1]]),
                                    enumerate(multiple_block_collection_solve_order), set())

    @staticmethod
    def group_multiple_blocks(multiple_block_collection_solve_order):
        labeled_indices = SimpleSolver.get_unique_blocks_from_multiple_block_collection_solve_order(
            multiple_block_collection_solve_order)
        return reduce(lambda agg, t: merge_dicts(agg, {t[1]: t[0]}), labeled_indices, {})

    def solve_multiple(self,
                    solver,
                    block_size: dict,
                    cell_size: dict,
                    profile: Profile,
                    empty_tile=None,
                    multiple_block_collection_solve_order=[]):

        # boundary_with_empty = boundary_with_empty and not not empty_texture
        self.set_empty_block(block_size, cell_size, empty_tile)

        blocks_dict = {}
        for block in self.blocks:
            blocks_dict[block.id] = block

        self.solve_picking_randomely(multiple_block_collection_solve_order, solver, profile, blocks_dict, block_size,
                                     cell_size,
                                     self.empty_block, 0, True)
        return self


    # TODO also add filled_texture as parameter for terrain comprehension
    def solve(self,
              solver,
              block_size: dict,
              cell_size: dict,
              profile: Profile,
              empty_tile=None,
              blocks_solve_order=None,
              boundary_with_empty=True):
        # FIXME remove this variable setting and fix the logic
        blocks_solve_order = None

        # if there is no custom solve order, then do this by default
        if blocks_solve_order is None:
            positions = [block.id for block in self.blocks]
            # calculate grid_shape from the block indices
            grid_shape = \
            [int(np.max(one_dimensional_positions)) + 1
             for one_dimensional_positions in [[position[d]
                                               for position in positions]
                                               for d in range(0, len(block_size))]]
            # create the block solve order
            blocks_solve_order = product(*[range(0, d) for d in grid_shape])

        return self.solve_multiple(solver, block_size, cell_size, profile, empty_tile,
                                   [{x} for x in blocks_solve_order])

    def solve_picking_randomely(self, blocks_solve_order: [[]], solver, profile, blocks_dict, block_size, cell_size,
                                empty_block, level, prefer_lower=False):
        solve_picking_randomely(self, blocks_solve_order, solver, profile, blocks_dict, block_size, cell_size,
                                empty_block, level, prefer_lower)


    def filter_neighbors(self, block):
        neighbors = block.neighbors
        return reduce(lambda agg, key: dict(agg, **{key: neighbors[key]})
                if not neighbors[key].solution is None #key in neighbors and neighbors[key].id < block.id
        else agg, list(neighbors), {})



    def add_empty_neighbors_at_boundaries(self, cell, empty_block):
        """
        Create neighbor boxes completely filled with empty_block. Used to enforce empty block adjacency.
        """
        boundary_dimensions = [dim for dim in TEXTURE_CONSTRAINT_ORDER if dim not in cell.neighbors or cell.neighbors[dim].void]
        return reduce(lambda agg, dim: dict(agg, **{dim: empty_block}), boundary_dimensions, {})

    @staticmethod
    def fill_mocked_block_with_empty_tiles(block_size, cell_size, empty_tile):
        return BlockSolver(block_size, cell_size, Profile(objects_with_id_field_to_dict([empty_tile]), None, None, None,
                                                          None, None, None, None))

    def show(self):
        if not self.blocks:
            return
        if len(list(self.grid_size)) > 2:
            return self.show_voxels()
        else:
            return self.show_img()

    def show_voxels(self, method=lambda x: x.show()):
        # get the first block as a reference for information about any block
        first_block = self.blocks[0]
        if first_block.solution == None:
            pass
        return get_filled_array_from_starting_block(first_block, 3,
                                                    lambda block:
                                                    # FIXME can't actually put empty block defined in solve here, what if solve is not called first then it breaks.
                                                    method(block.solution) if not block.solution is None else self.empty_block.show(),
                                                    "block")

    def flatten_into_block(self):
        """
        flatten blocks in one block
        :return: BlockSolver
        """
        # FIXME it is (ofcourse) really slow to first convert to voxel and then create a block from that
        # clear improvement is to create a new flattened block from the references of the other blocks
        solved_block = next((block.solution for block in self.blocks if block.solution.successful))
        if not solved_block:
            raise ValueError("there are no solved blocks")
        shown = self.show()
        return create_block_from_voxels(
            shown,
            dimensional_dict_to_tuple(solved_block.cell_size),
            solved_block.profile)


    def show_adjacency_type(self, type):
        return self.show_voxels(lambda x: x.show_adjacency(type))

    def show_different_color_per_tile(self, profile):
        color_map = reduce(lambda agg, t: merge_dicts(agg, {t: random_color()}), profile.tiles, {})
        return self.show_voxels(lambda x: x.show_different_color_per_tile(color_map))

    def show_img(self):
        # get the first block as a reference for information about any block
        first_block = self.blocks[0]
        # the amount of cells in a block
        first_block_size = first_block.solution.block_shape
        # the total size in pixels in a block
        block_width = reduce(
            lambda agg, key: dict(agg, **{key: first_block.solution.block_size[key] *
                                               first_block.solution.cell_size[key]}), first_block.solution.block_size, {})
        # total size of the block
        total_size = reduce(
            lambda agg, key:
                dict(agg, **{key: block_width[key] * self.grid_size[key]}), list(first_block_size), {})
        img = Image.new('RGB', (total_size['x'], total_size['y']), color=(255, 255, 255))
        # create the image for all cells
        for i, block in enumerate(self.blocks):
            # left up corner of the block in the complete image
            coord = [(i % self.grid_size['x']) * block_width["x"], math.floor(i / self.grid_size['x']) * block_width["y"]]
            # right down corner of the block in the complete image
            coord2 = map(sum, zip(coord, list(block_width.values())))
            coord.extend(list(coord2))
            coord = tuple(coord)
            img.paste(
                block.solution.show()
                , coord)
        img.show()
        img.save('export.png')
        return img
