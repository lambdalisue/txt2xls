#!/usr/bin/env nosetests -v
# coding=utf-8
import numpy as np
from nose.tools import *
from mock import MagicMock as Mock
from txt2xls.utils import find_peakset

def create_test_dataset():
    X = np.array([0, 2, 0, 0, 1, 1])
    Y = np.array([1, 1, 3, 2, 0, 1])
    Z = np.array([3, 2, 1, 6, 2, 2])

    dataset = [
        ['', X, Y, Z],
        ['', X*2, Y*2, Z*2],
        ['', X*3, Y*2, Z*2],
        ['', X*4, Y*4, Z*3],
    ]
    
    return dataset

def test_find_peakset_default():
    dataset = create_test_dataset()
    # basecolumn = -1
    # method=''
    # where=None
    peakset = find_peakset(dataset)

    np.testing.assert_array_equal(peakset, [
        [0, 0, 0, 0],
        [2, 4, 4, 8],
        [6, 12, 12, 18],
    ])

def test_find_peakset_basecolumn():
    dataset = create_test_dataset()
    # method=''
    # where=None
    # Note: +1 for filename column
    peakset = find_peakset(dataset, basecolumn=0+1)
    np.testing.assert_array_equal(peakset, [
        [2, 4, 6, 8],
        [1, 2, 2, 4],
        [2, 4, 4, 6],
    ])

    peakset = find_peakset(dataset, basecolumn=1+1)
    np.testing.assert_array_equal(peakset, [
        [0, 0, 0, 0],
        [3, 6, 6, 12],
        [1, 2, 2, 3],
    ])

def test_find_peakset_method():
    dataset = create_test_dataset()
    # where=None
    # Note: +1 for filename column
    peakset = find_peakset(dataset, basecolumn=1+1, method='argmin')
    np.testing.assert_array_equal(peakset, [
        [1, 2, 3, 4],
        [0, 0, 0, 0],
        [2, 4, 4, 6],
    ])

def test_find_peakset_where():
    dataset = create_test_dataset()
    where = lambda data: data[3] < 6
    # where=None
    # Note: +1 for filename column
    peakset = find_peakset(dataset, where=where)
    np.testing.assert_array_equal(peakset, [
        [0, 0, 0, 0],
        [1, 2, 2, 4],
        [3, 6, 6, 9],
    ])
