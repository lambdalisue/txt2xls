# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os

def default_unite_function(data):
    """
    A default unite_function which recieve `data` and return filename without
    middle extensions

    >>> # [<filename>] is mimicking `data`
    >>> default_unite_function(['./foo/foo.bar.hoge.piyo'])
    './foo/foo.piyo'
    >>> default_unite_function(['./foo/foo.piyo'])
    './foo/foo.piyo'
    >>> default_unite_function(['./foo/foo'])
    './foo/foo'
    """
    # data[0] indicate the filename of the data
    rootname, basename = os.path.split(data[0])
    filename, ext = os.path.splitext(basename)
    if '.' in filename:
        filename = filename.rsplit('.')[0]
    filename = os.path.join(rootname, filename + ext)
    return filename


# define __call__
__call__ = default_unite_function


if __name__ == '__main__':
    import doctest; doctest.testmod()
