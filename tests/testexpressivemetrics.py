import json
import unittest
import numpy as np

from metrics.expressivemetrics import repetition_calculation


class TestRepetition(unittest.TestCase):


    def test_all_equal(self):
        M = np.full((8,4,8), True).astype(float)
        self.assertEquals(repetition_calculation(M), 1.0)

    def test_no_equal(self):
        M = np.full((8,4,8), False).astype(float)
        self.assertEquals(repetition_calculation(M), 0.0)

    def test_one_repetition(self):
        M = np.full((8,4,8), False)
        M[0,0,0] = True
        M[3,0,0] = True
        M[6,0,0] = True
        M = M.astype(float)
        self.assertEquals(repetition_calculation(M), 1.0)





