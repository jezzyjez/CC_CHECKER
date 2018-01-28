#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.append(os.path.dirname(__file__) + "/../lib/")
import bcom_checker 

class BcomComponentTest(unittest.TestCase):
    """Test cases for determining the component to check """
    def setUp(self):
        self.bcom = bcom_checker.BcomChecker()

    def test_get_command(self):
        test_parameters = ['bcom', 'int:db:write']
        bcom_command = self.bcom.get_command(test_parameters)
        self.assertEqual(bcom_command, 'int:db:write')

    def test_invalid_get_command(self):
        test_parameters = ['bcom', 'int:ds:write']
        bcom_command = self.bcom.get_command(test_parameters)
        self.assertEqual(bcom_command, None)


