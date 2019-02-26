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

    def test_time_diff_success(self):
        _current_time_in_utc = dt.datetime.utcnow()
        korea_timedelta = dt.timedelta(hours=9)
        current_time = _current_time_in_utc + korea_timedelta

        future = (current_time + dt.timedelta(minutes=5)).strftime('%H:%M')
        past = (current_time - dt.timedelta(minutes=5)).strftime('%H:%M')
        now = current_time.strftime('%H:%M')

        cases = [
            (future, 300),
            (past, 86100),
            (now, 0)
        ]
        for s, expected in cases:
            self.assertEqual(get_time_diff(s), expected)

    def test_time_diff_failure(self):
        cases = [
            1259,
            dt.datetime(year=2019, month=1, day=1),
            12.59
        ]
        for s in cases:
            with self.assertRaises(ParseError):
                get_time_diff(s)

    def test_hour_success(self):
        _current_time_in_utc = dt.datetime.utcnow()
        korea_timedelta = dt.timedelta(hours=9)
        current_time = _current_time_in_utc + korea_timedelta

        future = (current_time + dt.timedelta(minutes=5)).strftime('%H:%M')
        past = (current_time - dt.timedelta(minutes=5)).strftime('%H:%M')
        now = current_time.strftime('%H:%M')

        cases = [
            ('23:59', get_time_diff('23:59')),
            ('00:00', get_time_diff('00:00')),
            (future, 300),
            (past, 86100),
            (now, 0)
        ]
        for s, expected in cases:
            self.assertEqual(parse_time_str(s), expected)

    def test_hour_failure(self):
        cases = [
            '24:00',
            '13:60',
            '1234:00',
            '23:000',
            '12;59',
            '12.59',
            '12 59',
            '12 : 59'
        ]
        for s in cases:
            with self.assertRaises(ParseError):
                parse_time_str(s)
