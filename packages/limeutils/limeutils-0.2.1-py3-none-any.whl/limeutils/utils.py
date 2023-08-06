from typing import Optional, Union


def isfloat(val: Union[int, float, str]):
    """
    Checks if the contents of a string is a float.
    :param val: String to parse
    :return:    bool
    """
    try:
        if isinstance(val, str):
            val.strip()
        float(val)
        return True
    except ValueError:
        return False
    

def byte_conv(val: Union[bytes, str]):
    """
    Converts bytes to a python string. This string could later be parsed into the correct
    python data type using parse_str(). Used mostly with Redis return values which always return in
    bytes.
    :param val: Bytes string to convert to python string
    :return:    str
    """
    if isinstance(val, str):
        return val
    
    try:
        x = val.decode()
        x = isinstance(x, bytes) and len(x) == 0 and '' or parse_str(x)
        return x
    except (UnicodeDecodeError, AttributeError):
        return val
    # return val.decode('utf-8')


def parse_str(string: str):
    """
    Converts a string to either an int, float, or str depending on its value.
    :param string:   String to convert
    :return:    int, float, or str
    """
    if not isinstance(string, str):
        raise ValueError('Only valid strings can be parsed.')
    
    string = string.strip()
    if string.isdigit():
        return int(string)
    elif isfloat(string):
        return float(string)
    return string


def split_fullname(fullname: str, default: str = '',
                   prefix: Optional[Union[str, list, tuple]] = None,
                   suffix: Optional[Union[str, list, tuple]] = None) -> tuple:
    """
    Splits a fullname into their respective first_name and last_name fields.
    If only one name is given, that becomes the first_name
    :param fullname:    The name to split
    :param default:     The value if only one name is given
    :param prefix:      Custom prefixes to append to the default list
    :param suffix:      Custom suffixes to append to the default list
    :return:            tuple
    """
    if prefix and not isinstance(prefix, (str, list, tuple)):
        raise TypeError('`prefix` must be a list/str for multi/single values.')

    if suffix and not isinstance(suffix, (str, list, tuple)):
        raise TypeError('`suffix` must be a list/str for multi/single values.')

    prefix = isinstance(prefix, str) and [prefix] or prefix or []
    suffix = isinstance(suffix, str) and [suffix] or suffix or []
    PREFIX_LASTNAME = ['dos', 'de', 'delos', 'san', 'dela', 'dona', *prefix]
    SUFFIX_LASTNAME = ['phd', 'md', 'rn', *suffix]

    list_ = fullname.split()
    lastname_idx = None
    if len(list_) > 2:
        for idx, val in enumerate(list_):
            if val.lower() in PREFIX_LASTNAME:
                lastname_idx = idx
                break
            elif val.lower().replace('.', '') in SUFFIX_LASTNAME:
                lastname_idx = idx - 1
            else:
                if idx == len(list_) - 1:
                    lastname_idx = idx
                else:
                    continue
        list_[:lastname_idx] = [' '.join(list_[:lastname_idx])]
        list_[1:] = [' '.join(list_[1:])]
    try:
        first, last = list_
    except ValueError:
        first, last = [*list_, default]
    return first, last