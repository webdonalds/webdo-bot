import re
import datetime as dt


class ParseError(Exception):
    pass


_re_time_str = re.compile(r'^(?P<size>[\d]+)(?P<is_time>:?)(?P<unit>[smh]|\d{1,2})$')


def get_time_diff(t) -> int:
    """
    Get time difference from now
    only accepts 'HH:MM' format
    """
    if not isinstance(t, str):
        raise ParseError

    current_time_utc = dt.datetime.utcnow()
    korea_timedelta = dt.timedelta(hours=9)
    current_time_local = (current_time_utc + korea_timedelta).strftime('%H:%M')

    current_time = dt.datetime.strptime(current_time_local, '%H:%M')
    input_time = dt.datetime.strptime(t, '%H:%M')
    return (input_time - current_time).seconds


def parse_time_str(s) -> int:
    """
    Parse time string and return as second(s).
    """
    match = _re_time_str.match(s)
    if match is None:
        raise ParseError

    size = int(match.group('size'))
    is_time = (match.group('is_time') == ':')
    unit = match.group('unit')

    if unit == 's':
        return size
    elif unit == 'm':
        return size * 60
    elif unit == 'h':
        return size * 60 * 60
    elif is_time and unit.isdigit() and 0 <= size < 24 and 0 <= int(unit) < 60:
        hour = size
        minute = int(unit)
        seconds = get_time_diff(f'{hour}:{minute}')
        return seconds
    else:
        raise ParseError
