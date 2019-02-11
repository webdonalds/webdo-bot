import re


class ParseError(Exception):
    pass


_re_time_str = re.compile(r'^(?P<size>[\d]+)(?P<unit>[smh])$')

def parse_time_str(s) -> int:
    """
    Parse time string and return as second(s).
    """
    match = _re_time_str.match(s)
    if match is None:
        raise ParseError 

    size = int(match.group('size'))
    unit = match.group('unit')
    if unit == 's':
        return size
    elif unit == 'm':
        return size * 60
    elif unit == 'h':
        return size * 60 * 60
    else:
        raise ParseError
