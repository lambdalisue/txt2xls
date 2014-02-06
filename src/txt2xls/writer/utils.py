# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import numpy as np


def get_sheet_name(filename):
    """
    Return extension and parent directory stripped filename which is used as a
    sheet name

    Args:
        filename (string): A file path

    Returns:
        filename: A extension and parent directory stripped filename

    Examples:
        >>> get_sheet_name('./foo/bar/hogehoge.piyo')
        'hogehoge'
        >>> len(get_sheet_name("*"*100))
        31
    """
    filename = os.path.basename(filename)
    filename = os.path.splitext(filename)[0]
    # there are 31 character limitation
    if len(filename) > 31:
        filename = filename[:31]
    return filename


def ensure_iterable(axis):
    """
    Ensure the axis is iterable (XY array)

    >>> axis1 = [
    ...     [0, 1, 2],
    ...     [3, 4, 5],
    ...     [6, 7, 8],
    ... ]
    >>> assert axis1 == ensure_iterable(axis1)
    >>> axis21 = [0, 1, 2]
    >>> axis22 = [[0], [1], [2]]
    >>> assert axis22 == ensure_iterable(axis21)
    """
    iterable = (np.ndarray, list, tuple)
    if not isinstance(axis[0], iterable):
        return [[r] for r in axis]
    return axis


def prefer_alphabet(i):
    """
    Convert an integer to an alphabet if it is within 0 to 51.

    >>> prefer_alphabet(0)
    'A'
    >>> prefer_alphabet(25)
    'Z'
    >>> prefer_alphabet(26)
    'a'
    >>> prefer_alphabet(51)
    'z'
    >>> prefer_alphabet(100)
    '100'
    """
    if 0 <= i <= 25:
        return chr(i + 65)
    if 26 <= i <= 51:
        return chr(i + 97 - 26)
    return str(i)

