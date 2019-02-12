import re
import datetime as dt


class ParseError(Exception):
    pass


_re_time_str = re.compile(r'^(?P<size>[\d]+)(?P<is_time>:?)(?P<unit>[smh]|\d{1,2})$')

def get_time_diff(t) -> int:
    """
    Get time difference from now
    """
    _current_time = dt.datetime.now().strftime('%H:%M')
    current_time = dt.datetime.strptime(_current_time, '%H:%M')
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
    is_time = True if match.group('is_time') == ':' else False
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
        seconds = seconds if seconds >= 0 else seconds + 60 * 60 * 24   # if input time is smaller then it is timer for next day
        return seconds
    else:
        raise ParseError
