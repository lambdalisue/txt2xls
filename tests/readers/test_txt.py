#!/usr/bin/env nosetests -v
# coding=utf-8
import numpy as np
from nose.tools import *
from mock import MagicMock

from txt2xls.readers.txt import auto_unite

def test_auto_unite():
    dataset = [
        ['./test/dataset01.000.000.txt',
         np.array([0, 1, 2, 3, 4, 5]),
         np.array([0, 1, 2, 3, 4, 5])],
        ['./test/dataset01.001.000.txt',
         np.array([0, 1, 2, 3, 4, 5]),
         np.array([0, 1, 2, 3, 4, 5])],
        ['./test/dataset01.002.000.txt',
         np.array([0, 1, 2, 3, 4, 5]),
         np.array([0, 1, 2, 3, 4, 5])],
        ['./test/dataset02.000.000.txt',
         np.array([0, 1, 2, 3, 4, 5]),
         np.array([0, 1, 2, 3, 4, 5])],
        ['./test/dataset02.001.000.txt',
         np.array([0, 1, 2, 3, 4, 5]),
         np.array([0, 1, 2, 3, 4, 5])],
        ['./test/dataset03.002.000.txt',
         np.array([0, 1, 2, 3, 4, 5]),
         np.array([0, 1, 2, 3, 4, 5])],
    ]

    dataset = auto_unite(dataset, basecolumn=0)

    eq_(dataset[0][0], './test/dataset01.txt')
    eq_(dataset[1][0], './test/dataset02.txt')
    eq_(dataset[2][0], './test/dataset03.txt')

    eq_(len(dataset[0][1][0]), 3)
    eq_(len(dataset[1][1][0]), 2)
    ok_(isinstance(dataset[2][1][0], np.int64))

    eq_(len(dataset[0][2][0]), 3)
    eq_(len(dataset[1][2][0]), 2)
    ok_(isinstance(dataset[2][2][0], np.int64))
