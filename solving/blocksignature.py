from functools import reduce

from solving.util import merge_dicts, max_of_list, min_of_list, create_tile_enum

import math
import numpy as np

from voxels.magicavoxwrapper import visualize_voxel

TILE_ROTATIONS = 4

class BlockSignature:

    def __init__(self, positioned_tiles):
        self.positioned_tiles = positioned_tiles

    def __eq__(self, other_signature):
        return self.equal_signature_with_rotation(other_signature)

    def amount_of_different_tiles(self, other_signature):
        '''
        can be used as a distance metric to compare signatures
        :param other_signature:
        :return:
        '''
        return sum(1 for position in self.positioned_tiles
                   if self.positioned_tiles[position] == other_signature.positioned_tiles[position])

    def to_matrix_notation_only_tiles(self, tile_to_number_d):
        M = np.full(max_of_list(self.positioned_tiles), -1, dtype=np.int8)
        for i in self.positioned_tiles:
            M[i] = tile_to_number_d[tile_to_number_d[self.positioned_tiles[i][0]]]
        return M

    @staticmethod
    def block_to_positioned_tiles(block):
        #TODO remove visualize here
        # visualize_voxel(block.show())
        return reduce(lambda agg, cell: merge_dicts(agg,
                                                        {cell.id: (cell.get_tile_in_contains()["tile"].id,
                                                                   0, int(cell.get_tile_in_contains()["rotY"]), 0)}),
                          block.cells, {})


    def has_tile_id(self, tile_id):
        for i in self.positioned_tiles:
            if self.positioned_tiles[i][0] == tile_id:
                return True
        return False

    def rotate_y_signature(self, amount):
        if not type(amount) == int:
            ValueError(f"{amount} is not an integer, can only rotate in steps of 90 degrees")

        # TODO consider making a utility function for position rotation
        s = int(math.sin(math.pi * 0.5 * amount))
        c = int(math.cos(math.pi * 0.5 * amount))

        def y_rot(x, y, z):
            return int(c * x + s * z), int(y),  int(- s * x + c * z)

        new_positions = {}
        for position in self.positioned_tiles:
            sig = self.positioned_tiles[position]
            new_position = y_rot(*position)
            if new_position in new_positions:
                print("error")
            new_positions[new_position] = (sig[0], sig[1], (sig[2] + amount) % 4, sig[3])

        distance_from_origin = reduce(lambda a, b: np.minimum(a,b), new_positions)
        translated_points = reduce(lambda agg, p: merge_dicts(agg,
                                   {tuple(np.subtract(p, distance_from_origin)): new_positions[p]}), new_positions, {})
        return BlockSignature(translated_points)

    def rotate_y_clockwise(self):
        return self.rotate_y_signature(1)

    def amount_of_positions(self):
        return len(self.positioned_tiles)

    def equal_signature_with_rotation(self, other_signature):
        return not not len([i for i in range(0,4) if self.equals(other_signature.rotate_y_signature(i))])

    def equals(self, other_signature):
        if len(self.positioned_tiles) != len(other_signature.positioned_tiles):
            return False
        for position in self.positioned_tiles:
            if not position in other_signature.positioned_tiles or \
                    not self.equal_tiles(self.positioned_tiles[position],
                                         other_signature.positioned_tiles[position],
                                         False):
                return False
        return True

    def equal_tiles(self, tile_tuple_a, tile_tuple_b, add_rotation=True):
        if add_rotation:
            return tile_tuple_a == tile_tuple_b
        else:
            return tile_tuple_a[0] == tile_tuple_b[0]

    def convert_to_dict_notation(self, tiles):
        return reduce(lambda agg, p: merge_dicts(agg, {p: {"tile": tiles[self.positioned_tiles[p][0]],
                                                           "rotY": self.positioned_tiles[p][2]}})
                                                 , self.positioned_tiles, {})

    def to_matrix_representation(self, profile):
        tile_enum = create_tile_enum(profile)
        M = np.full(max_of_list(self.positioned_tiles) + 1, 0)
        for i in self.positioned_tiles:
            M[i] = tile_enum[self.positioned_tiles[i][0]] * TILE_ROTATIONS + self.positioned_tiles[i][2]
        return M


def remove_duplicate_blocks(blocks, sorted=False, max_blocks_in_storage=None, exit_on_subsequent_duplicate_count=0,
                            absolute_duplicate_occurrence_limit=0):
    agg = []
    indices = set()
    absolute_dups = 0
    subsequent_dup = 0
    for i, block in enumerate(blocks):
        signature = BlockSignature(BlockSignature.block_to_positioned_tiles(block))
        if signature not in agg:
            subsequent_dup = 0
            if sorted:
                agg = []
            if max_blocks_in_storage and max_blocks_in_storage <= len(agg):
                agg.pop(0)
            agg.append(signature)
            # unique_blocks.append(block)
            indices.add(i)
            print(signature.positioned_tiles)
            print(f"added {str(i)}")
            print(f"total {str(len(indices))}")
            yield block
        else:
            absolute_dups += 1
            subsequent_dup += 1
        if exit_on_subsequent_duplicate_count and exit_on_subsequent_duplicate_count < subsequent_dup:
            break
        if absolute_duplicate_occurrence_limit and absolute_dups > absolute_duplicate_occurrence_limit:
            break




