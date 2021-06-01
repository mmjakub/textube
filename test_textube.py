#!/usr/bin/env python3.9

import unittest

import textube

class TestPytsub(unittest.TestCase):

    def test_subs(self):
        subs = textube.get_captions_from_config('2Ze22BNftAA')
        self.assertIsNotNone(subs)
        self.assertEqual(len(subs), 21725)

if __name__ == '__main__':
    unittest.main()
