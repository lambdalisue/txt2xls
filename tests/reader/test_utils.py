#!/usr/bin/env nosetests -v
# coding=utf-8
import numpy as np
from nose.tools import *
from mock import MagicMock as Mock

from txt2xls.reader.utils import unite_dataset
from txt2xls.reader.utils import classify_dataset
from txt2xls.function.builtin.unite_function import default_unite_function
from txt2xls.function.builtin.classify_function import default_classify_function


def create_test_dataset():
    X = np.array([0, 1, 2, 3, 4, 5])
    Y = np.array([10, 11, 12, 13, 14, 15])
    dataset = [
        ['./test/dataset_type01_00.000.000.txt', X, Y],
        ['./test/dataset_type01_00.001.000.txt', X, Y],
        ['./test/dataset_type01_00.002.000.txt', X, Y],
        ['./test/dataset_type01_01.000.000.txt', X, Y],
        ['./test/dataset_type01_01.001.000.txt', X, Y],
        ['./test/dataset_type01_01.002.000.txt', X, Y],
        ['./test/dataset_type02_00.000.000.txt', X, Y],
        ['./test/dataset_type02_00.001.000.txt', X, Y],
        ['./test/dataset_type02_00.002.000.txt', X, Y],
        ['./test/dataset_type02_01.000.000.txt', X, Y],
        ['./test/dataset_type02_01.001.000.txt', X, Y],
        ['./test/dataset_type02_01.002.000.txt', X, Y],
    ]
    return dataset


def test_unite_dataset_default():
    dataset = create_test_dataset()
    dataset = unite_dataset(dataset,
                            basecolumn=0,
                            fn=default_unite_function)

    # return dataset should be an instance of list, tuple
    ok_(isinstance(dataset, (list, tuple)))

    # default unite_fn will classify dataset with middle extension (.000.000)
    eq_(dataset[0][0], './test/dataset_type01_00.txt')
    eq_(dataset[1][0], './test/dataset_type01_01.txt')
    eq_(dataset[2][0], './test/dataset_type02_00.txt')
    eq_(dataset[3][0], './test/dataset_type02_01.txt')

    # there should be 6 rows in each axis
    for i in range(0, 4):
        eq_(len(dataset[i][1]), 6)
        eq_(len(dataset[i][2]), 6)

    # there should be 3 columns in each axis
    for i in range(0, 4):
        eq_(len(dataset[i][1][0]), 3)
        eq_(len(dataset[i][2][0]), 3)


def test_unite_dataset_unite_fn_called():
    mock_function = Mock(return_value='')
    dataset = create_test_dataset()
    dataset = unite_dataset(dataset,
                            basecolumn=0,
                            fn=mock_function)
    ok_(mock_function.called)


def test_classify_dataset_default():
    dataset = create_test_dataset()
    nameset = [x[0] for x in dataset]
    collection = classify_dataset(dataset,
                                  fn=default_classify_function)

    # return collection should be an instance of dictionary
    ok_(isinstance(collection, dict))

    # default fn will classify dataset with filename before last '_'
    # character
    eq_(collection.keys(), [
        './test/dataset_type01.txt',
        './test/dataset_type02.txt',
    ])

    # there should be 6 dataset
    for name, dataset in collection.items():
        eq_(len(dataset), 6)

    # there should be 3 columns in each data
    for name, dataset in collection.items():
        for i in range(0, 6):
            eq_(len(dataset[i]), 3)

    # there should be 6 rows in each axis
    for (name, dataset) in collection.items():
        for i in range(0, 6):
            eq_(len(dataset[i][1]), 6)
            eq_(len(dataset[i][2]), 6)

    # there should be 1 columns in each axis
    for (name, dataset) in collection.items():
        for i in range(0, 6):
            ok_(isinstance(dataset[i][1][0], (int, float, np.float64)))
            ok_(isinstance(dataset[i][2][0], (int, float, np.float64)))


def test_classify_dataset_fn_called():
    mock_function = Mock(return_value='')
    dataset = create_test_dataset()
    dataset = classify_dataset(dataset,
                               fn=mock_function)
    ok_(mock_function.called)
