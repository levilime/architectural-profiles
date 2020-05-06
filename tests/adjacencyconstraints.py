import json
import unittest

from run_utils.profileimporter import import_profile, EMPTY_TILE
from run_utils.reflectexample import reflects_examples
from solving.util import dimensional_dict_to_tuple
from tile.allconnected import AllConnectedPart


class TestReflection(unittest.TestCase):

    def setUp(self):
        cell_size = {"x": 5, "y": 4, "z": 5}
        cell_size_t = dimensional_dict_to_tuple(cell_size)
        with open("tests/testprofilebasic.json", 'r') as f:
            profile_json = json.load(f)

        profile = import_profile(profile_json, '5x4x5x', cell_size_t)
        self.profile = profile
        self.profile_json = profile_json


    def test_satisfied_adjacency_constraints(self):
        cell_size = {"x": 5, "y": 4, "z": 5}
        cell_size_t = dimensional_dict_to_tuple(cell_size)
        block_size = {"x": 4, "y": 4, "z": 4}
        block_size_t = dimensional_dict_to_tuple(block_size)
        profile = self.profile.copy_profile_other_tiles(self.profile.tiles, self.profile.tiles[EMPTY_TILE])
        self.assertTrue(reflects_examples(profile, self.profile_json, '5x4x5x', block_size, cell_size, False))

    def test_satisfied_all_connected(self):
        cell_size = {"x": 5, "y": 4, "z": 5}
        cell_size_t = dimensional_dict_to_tuple(cell_size)
        block_size = {"x": 4, "y": 4, "z": 4}
        block_size_t = dimensional_dict_to_tuple(block_size)
        profile = self.profile.copy_profile_other_tiles(self.profile.tiles, self.profile.tiles[EMPTY_TILE])
        profile.all_connected = [AllConnectedPart("routing", "routing")]
        self.assertTrue(reflects_examples(profile, self.profile_json, '5x4x5x', block_size, cell_size, False))



