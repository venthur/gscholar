#!/usr/bin/env python
# coding: utf8

import unittest

from gscholar import gscholar as gs


class TestGScholar(unittest.TestCase):

    def test_query(self):
        """Normal query with latin encoding should give non empty result."""
        result = gs.query('Albert Einstein', gs.FORMAT_BIBTEX)
        self.assertTrue(result)

    def test_query_utf8(self):
        """Normal query with utf8 encoding should give non empty result."""
        result = gs.query("Anders Jonas Ångström", gs.FORMAT_BIBTEX)
        self.assertTrue(result)
