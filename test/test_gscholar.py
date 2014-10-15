#!/usr/bin/env python
# coding: utf8

import unittest
import time
import random

from gscholar import gscholar as gs


class TestGScholar(unittest.TestCase):

    def tearDown(self):
        # wait 1-2 seconds between tests, so we don't hammer google's
        # servers and get banned.
        time.sleep(random.uniform(1, 2))

    def test_query(self):
        """Normal query with latin encoding should give non empty result."""
        result = gs.query('Albert Einstein', gs.FORMAT_BIBTEX)
        self.assertTrue(result)

    def test_query_utf8(self):
        """Normal query with utf8 encoding should give non empty result."""
        result = gs.query("Anders Jonas Ångström", gs.FORMAT_BIBTEX)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()

