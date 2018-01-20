#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.append(os.path.dirname(__file__) + "/../lib/")
import bcom_checker as bcom

class BcomComponentTest(unittest.TestCase):
    """Test cases for determining the component to check """
    def setUp(self):
        self.common_func = cf.CommonFunc()

    def test_is_bcom(self):
        self.assertEqual(self.common_func.parse_component('Bcom '), 'bcom')

    def test_is_fdb(self):
        self.assertEqual(self.common_func.parse_component('fdb '), 'fdb')
         
    def test_is_not_fdb_or_bcom(self):
        self.assertEqual(self.common_func.parse_component('not on component'), None)
