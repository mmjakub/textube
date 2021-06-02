import unittest

from textube import ytapi

class TestYTApi(unittest.TestCase):

    def test_subs(self):
        subs = ytapi.get_captions_from_config('2Ze22BNftAA')
        self.assertIsNotNone(subs)
        self.assertEqual(len(subs), 21725)
