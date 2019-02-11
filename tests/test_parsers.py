import unittest

from parsers import *

class ParseTimeStrTestCase(unittest.TestCase):
    def test_parse_success(self):
        cases = [
            ('1s', 1),
            ('30s', 30),
            ('1m', 60),
            ('30m', 60 * 30),
            ('1h', 60 * 60),
            ('12h', 60 * 60 * 12),
        ]
        for s, expected in cases:
            self.assertEqual(parse_time_str(s), expected)

    def test_parse_failure(self):
        cases = [
            '20w',
            'abcd',
            '1m1s',
            '20 s',
        ]
        for s in cases:
            with self.assertRaises(ParseError):
                parse_time_str(s)
