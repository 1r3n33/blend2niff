"""Niff2 Name Tests"""

import unittest
from parameterized import parameterized

from blend2niff.niff2.niff2_name import niff2_name_node_builder


class TestNiff2Name(unittest.TestCase):

    @parameterized.expand([
        ("empty", 0, "", 16),
        ("A", 0, "A", 20),
        ("AB", 0, "AB", 20),
        ("ABC", 0, "ABC", 20),
        ("ABCD", 0, "ABCD", 20),
        ("ABCDE", 0, "ABCDE", 24),
    ])
    def test_niff2_name_builder(self, _, index, name, expected_size):
        name_node = niff2_name_node_builder(index, name)
        self.assertEqual(name_node.name_tag, 0x00110100)
        self.assertEqual(name_node.this_name_index, index)
        self.assertEqual(name_node.name_header_size, 16)
        self.assertEqual(name_node.name_size, expected_size)
        self.assertEqual(name_node.node_name, name)
