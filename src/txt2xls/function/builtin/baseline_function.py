# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'


def default_baseline_function(data, column):
    return data[column][0]

# define __call__
__call__ = default_baseline_function


if __name__ == '__main__':
    import doctest; doctest.testmod()
