from functools import reduce

from oldprofiles.addmetarules import retrieve_metapositions
from solving.util import merge_dicts, dimension_order_with_negative, group_to_dict, get_block_solved_surrounding
import numpy as np

class Metadata:

    def __init__(self, profile, block_size: {str: int},
                 metapositions: [str],
                 cell_assigns: {(int, int, int): (str, int, int, int)},
                 equal_blocks, equal_cells, null_blocks, null_cells, current_index=(0, 0, 0), closed_on_types=(),
                 required_shapes=frozenset()):
        """
        :param profile: profile of the block
        :param expanded_boundaries: how much the block size may change
        actual block size = block_size - expanded_boundaries
        :param metapositions:
        whether the block is adjacent to an edge of the solution, a list of directions
        :param neighbor_adjacencies:
        whether the block is adjacent to a neighbor, a list of directions
        :param cell_assigns:
        preassigned cell values = {cell_position: (tile_id, rotX, rotY, rotZ)}, cell positions relative to this block
        :param equal_blocks:
        what blocks are to be equal to this block, this block is denoted by the
        value of current_index
        :param equal_cells:
        what cells need to be equal to what other cells, cell positions relative to this block
        :param null_blocks:
        what blocks need not to be assigned
        :param null_cells:
        what cells need not to be assigned, cell positions relative to this block
        :param current_index:
        the relative index of this block
        """
        self.profile = profile
        self.metapositions = metapositions
        self.neighbor_adjacencies = reduce(lambda agg, objective: merge_dicts(agg,
                                                              {objective: set(dimension_order_with_negative).difference(
                                                                  metapositions[objective])}),
                                           self.metapositions,
                           {})
        self.block_size = block_size
        self.cell_assigns = cell_assigns
        self.equal_blocks = equal_blocks
        self.equal_cells = equal_cells
        self.null_blocks = null_blocks
        self.null_cells = null_cells
        self.current_index = current_index
        self.surrounding_level = 2
        self.models = 0
        self.closed_on_types = closed_on_types
        self.required_shapes = required_shapes
        self.shape_annotations = dict()

    def get_relative_equal_blocks(self, index):
        return self.get_data_relative_to_index(self.equal_blocks, index)

    def get_data_relative_to_index(self, data, index):
        absolute_data = data[index]
        relative_data = [np.subtract(current, index) for current in absolute_data]
        return relative_data

    def relative_metadata_for_objectives(self, objectives):
        """
        create metadata relative to objectives
        :param objectives:
        :return: Metadata
        """
        pass

    @staticmethod
    def get_surrounding_blocks_static(blocks, level):
        return reduce(lambda agg, i:
               merge_dicts(agg,
                           {i: get_block_solved_surrounding(i, blocks,
                                                            level)}),
               blocks, {})

    # @staticmethod
    # def get_unique_surrounding_blocks(indices, surroundings):
    #     unique_surroundings_set = set()
    #     for index in indices:
    #         unique_surroundings_set.union(surroundings[index])
    #     return reduce(lambda agg, i: merge_dicts(agg, {i: surroundings[i]}), unique_surroundings_set, {})

    @staticmethod
    def resolve_metadata(profile, block_size, indices, equal_block_groups: [{(int, int, int)}]= [],
                         null_blocks: [(int, int, int)] = [], equal_cell_dict= {}, null_cell_dict = {}):
        metapositions = retrieve_metapositions(indices)
        equal_blocks_dict = group_to_dict(equal_block_groups)
        null_blocks_set = set(null_blocks)
        return Metadata(profile, block_size, metapositions, None, equal_blocks_dict, equal_cell_dict, null_blocks_set,
                        null_cell_dict)


