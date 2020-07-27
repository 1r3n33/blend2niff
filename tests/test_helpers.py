"""Helper methods Tests."""

import unittest
from parameterized import parameterized

from blend2niff.helpers import correct_gamma


class TestHelpers(unittest.TestCase):
    @parameterized.expand([("rgb_0.0", [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
                           ("rgb_0.5", [0.5, 0.5, 0.5], [0.7297, 0.7297, 0.7297]),
                           ("rgb_1.0", [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]),
                           ("rgba", [0.5, 0.5, 0.5, 0.5], [0.7297, 0.7297, 0.7297, 0.5])])
    def test_niff2_name_builder(self, _, input_color, expected_color):
        corrected_color = correct_gamma(input_color)
        for i in range(len(expected_color)):
            self.assertAlmostEqual(corrected_color[i], expected_color[i], 4)
