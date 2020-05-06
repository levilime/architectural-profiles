import json
import unittest
from solving.blocksignature import BlockSignature


class TestBlockSignature(unittest.TestCase):

    def setUp(self):
        positioned_tiles = {(0, 0, 0): ('flatsurface', 0, 3, 0), (0, 0, 1): ('flatsurface', 0, 3, 0), (0, 0, 2): ('flatsurface', 0, 3, 0), (0, 0, 3): ('flatsurface', 0, 3, 0), (0, 0, 4): ('flatsurface', 0, 3, 0), (0, 1, 0): ('void', 0, 3, 0), (0, 1, 1): ('void', 0, 3, 0), (0, 1, 2): ('void', 0, 3, 0), (0, 1, 3): ('void', 0, 3, 0), (0, 1, 4): ('void', 0, 3, 0), (1, 0, 0): ('flatsurface', 0, 3, 0), (1, 0, 1): ('flatsurface', 0, 3, 0), (1, 0, 2): ('corner', 0, 0, 0), (1, 0, 3): ('door', 0, 1, 0), (1, 0, 4): ('corner', 0, 1, 0), (1, 1, 0): ('void', 0, 3, 0), (1, 1, 1): ('void', 0, 3, 0), (1, 1, 2): ('roof', 0, 3, 0), (1, 1, 3): ('roof', 0, 3, 0), (1, 1, 4): ('roof', 0, 3, 0), (2, 0, 0): ('flatsurface', 0, 3, 0), (2, 0, 1): ('flatsurface', 0, 3, 0), (2, 0, 2): ('door', 0, 0, 0), (2, 0, 3): ('inside', 0, 3, 0), (2, 0, 4): ('door', 0, 2, 0), (2, 1, 0): ('void', 0, 3, 0), (2, 1, 1): ('void', 0, 3, 0), (2, 1, 2): ('roof', 0, 3, 0), (2, 1, 3): ('roof', 0, 3, 0), (2, 1, 4): ('roof', 0, 3, 0), (3, 0, 0): ('corner', 0, 0, 0), (3, 0, 1): ('corner', 0, 1, 0), (3, 0, 2): ('corner', 0, 3, 0), (3, 0, 3): ('door', 0, 3, 0), (3, 0, 4): ('corner', 0, 2, 0), (3, 1, 0): ('roof', 0, 3, 0), (3, 1, 1): ('roof', 0, 3, 0), (3, 1, 2): ('roof', 0, 3, 0), (3, 1, 3): ('roof', 0, 3, 0), (3, 1, 4): ('roof', 0, 3, 0), (4, 0, 0): ('door', 0, 0, 0), (4, 0, 1): ('door', 0, 2, 0), (4, 0, 2): ('flatsurface', 0, 3, 0), (4, 0, 3): ('flatsurface', 0, 3, 0), (4, 0, 4): ('flatsurface', 0, 3, 0), (4, 1, 0): ('roof', 0, 3, 0), (4, 1, 1): ('roof', 0, 3, 0), (4, 1, 2): ('void', 0, 3, 0), (4, 1, 3): ('void', 0, 3, 0), (4, 1, 4): ('void', 0, 3, 0)}
        self.ref_bs = BlockSignature(positioned_tiles)

    def test_0_rotate_equals_original(self):
        self.assertEqual(self.ref_bs, self.ref_bs.rotate_y_signature(0))

    def test_4_rotate_equals_original(self):
        self.assertEqual(self.ref_bs, self.ref_bs.rotate_y_signature(4))



