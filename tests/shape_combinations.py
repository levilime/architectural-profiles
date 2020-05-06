import unittest

from solving.util import create_shape_solve_combinations
from tile.shape import Nameable


class ShapeCombinations(unittest.TestCase):

    def setUp(self):
        self.shapes = [Nameable("a"),Nameable("a"),Nameable("a"), Nameable("b"), Nameable("b"), Nameable("c")]

    def test_all_elements(self):
        ll = create_shape_solve_combinations(self.shapes, len(self.shapes), len(self.shapes))
        self.assertCountEqual(self.shapes, list(ll)[0])

    def test_only_two_in_container(self):
        ll = create_shape_solve_combinations(self.shapes, len(self.shapes), 2)
        self.assertIs(len(list(ll)), 3)

    def test_only_one_in_container(self):
        ll = list(create_shape_solve_combinations(self.shapes, len(self.shapes), 1))
        self.assertIs(len(ll), 6)
        self.assertIs(len(ll[0]), 3)

    def test_total_max_shapes_one_smaller(self):
        ll = list(create_shape_solve_combinations(self.shapes, 5, len(self.shapes)))
        self.assertIs(len(ll), 6)
        self.assertIs(len(ll[0]), 5)