# -*- coding: utf8 -*-


import unittest

import pylatest


class TestBase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_example(self):
        msg = "strings should be the same"
        self.assertEqual("foo", "foo", msg)
