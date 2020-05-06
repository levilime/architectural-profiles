import json
import unittest

from run_utils.habitationresolver import habitation_resolver
from oldprofiles.util import get_indices
from run_utils.profileimporter import import_profile, EMPTY_TILE
from solving.util import dimensional_dict_to_tuple


class ConnectivityDistance(unittest.TestCase):

    def setUp(self):
        cell_size = {"x": 5, "y": 4, "z": 5}
        cell_size_t = dimensional_dict_to_tuple(cell_size)
        with open("tests/testprofile.json", 'r') as f:
            profile_json = json.load(f)

        profile = import_profile(profile_json, '5x4x5x', cell_size_t)
        self.profile = profile


    def test_proper_dimensions_two(self):
        cell_size = {"x": 5, "y": 4, "z": 5}
        cell_size_t = dimensional_dict_to_tuple(cell_size)
        block_size = {"x": 1, "y": 5, "z": 1}
        block_size_t = dimensional_dict_to_tuple(block_size)
        profile = self.profile.copy_profile_other_tiles(self.profile.tiles, self.profile.tiles[EMPTY_TILE])
        profile.connectivities[0].length = (2, 2)
        result = habitation_resolver(profile, block_size, cell_size, get_indices(1, 1, 1),
                                     {
                                         (0, 0, 0):
                                             {
                                                 "filled_assignment":
                                                     {(0, 0, 0): True},(0, 1, 0): True},
                                                 "void_assignment":
                                                     {(0, 4, 0): True, (0, 3, 0): True}
                                             }
                                     )
        self.assertTrue(result.blocks[0].solution.successful)

    def test_proper_dimensions_one(self):
        cell_size = {"x": 5, "y": 4, "z": 5}
        cell_size_t = dimensional_dict_to_tuple(cell_size)
        block_size = {"x": 1, "y": 5, "z": 1}
        block_size_t = dimensional_dict_to_tuple(block_size)
        profile = self.profile.copy_profile_other_tiles(self.profile.tiles, self.profile.tiles[EMPTY_TILE])
        profile.connectivities[0].length = (1, 1)
        result = habitation_resolver(profile, block_size, cell_size, get_indices(1, 1, 1),
                                     {
                                         (0, 0, 0):
                                             {
                                                 "filled_assignment":
                                                     {(0, 0, 0): True}},
                                                 "void_assignment":
                                                     {(0, 2, 0): True, (0, 4, 0): True, (0, 3, 0): True}
                                             }
                                     )
        self.assertTrue(result.blocks[0].solution.successful)

    def test_maximum_0_no_placement(self):
        cell_size = {"x": 5, "y": 4, "z": 5}
        cell_size_t = dimensional_dict_to_tuple(cell_size)
        block_size = {"x": 1, "y": 5, "z": 1}
        block_size_t = dimensional_dict_to_tuple(block_size)
        profile = self.profile.copy_profile_other_tiles(self.profile.tiles, self.profile.tiles[EMPTY_TILE])
        profile.connectivities[0].length = (0, 0)
        result = habitation_resolver(profile, block_size, cell_size, get_indices(1, 1, 1),
                                     {
                                         (0, 0, 0):
                                             {
                                                 "filled_assignment":
                                                     {(0, 0, 0): True},
                                                 "void_assignment":
                                                     {(0, 4, 0): True}
                                             }
                                     }
                                     )
        self.assertIsNone(result.blocks[0].solution)

    def test_placement_cant_satisfy_minimum(self):
        cell_size = {"x": 5, "y": 4, "z": 5}
        cell_size_t = dimensional_dict_to_tuple(cell_size)
        block_size = {"x": 1, "y": 5, "z": 1}
        block_size_t = dimensional_dict_to_tuple(block_size)
        profile = self.profile.copy_profile_other_tiles(self.profile.tiles, self.profile.tiles[EMPTY_TILE])
        profile.connectivities[0].length = (2, 5)
        result = habitation_resolver(profile, block_size, cell_size, get_indices(1, 1, 1),
                                     {
                                         (0, 0, 0):
                                             {
                                                 "filled_assignment":
                                                     {(0, 0, 0): True},
                                                 "void_assignment":
                                                     {(0, 2, 0): True}
                                             }
                                     }
                                     )
        self.assertIsNone(result.blocks[0].solution)

    def test_placement_cant_satisfy_minimum_bigger_than_maximum(self):
        cell_size = {"x": 5, "y": 4, "z": 5}
        cell_size_t = dimensional_dict_to_tuple(cell_size)
        block_size = {"x": 1, "y": 5, "z": 1}
        block_size_t = dimensional_dict_to_tuple(block_size)
        profile = self.profile.copy_profile_other_tiles(self.profile.tiles, self.profile.tiles[EMPTY_TILE])
        profile.connectivities[0].length = (3, 2)
        result = habitation_resolver(profile, block_size, cell_size, get_indices(1, 1, 1),
                                     {
                                         (0, 0, 0):
                                             {
                                                 "filled_assignment":
                                                     {(0, 0, 0): True},
                                                 "void_assignment":
                                                     {(0, 4, 0): True}
                                             }
                                     }
                                     )
        self.assertIsNone(result.blocks[0].solution)



