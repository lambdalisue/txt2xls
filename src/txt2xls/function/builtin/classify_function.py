# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os


def default_classify_function(data):
    """
    A default classify_function which recieve `data` and return filename without
    characters just after the last underscore

    >>> # [<filename>] is mimicking `data`
    >>> default_classify_function(['./foo/foo_bar_hoge.piyo'])
    './foo/foo_bar.piyo'
    >>> default_classify_function(['./foo/foo_bar.piyo'])
    './foo/foo.piyo'
    >>> default_classify_function(['./foo/foo.piyo'])
    './foo/foo.piyo'
    >>> default_classify_function(['./foo/foo'])
    './foo/foo'
    """
    # data[0] indicate the filename of the data
    rootname, basename = os.path.split(data[0])
    filename, ext = os.path.splitext(basename)
    if '_' in filename:
        filename = filename.rsplit('_', 1)[0]
    filename = os.path.join(rootname, filename + ext)
    return filename

# define __call__
__call__ = default_classify_function


if __name__ == '__main__':
    import doctest; doctest.testmod()
