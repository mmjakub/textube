#!/usr/bin/env python3.9

import unittest

from .context import ytapi

class TestYTApi(unittest.TestCase):

    def test_subs(self):
        subs = ytapi.get_captions_from_config('2Ze22BNftAA')
        self.assertIsNotNone(subs)
        self.assertEqual(len(subs), 21725)

if __name__ == '__main__':
    unittest.main()
