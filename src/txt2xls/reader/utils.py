# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
from maidenhair.loaders.base import unite_dataset as _unite_dataset
from txt2xls.compat import OrderedDict


def unite_dataset(dataset, basecolumn, fn):
    """
    Unite dataset via fn

    Args:
        dataset (list): A list of data
        basecolumn (int): A number of column which will be respected in uniting
            dataset
        fn (function): A function which recieve `data` and return string

    Returns:
        dataset: A united dataset (list)
    """
    # create default unite_fn
    # classify dataset via unite_fn
    united_dataset = OrderedDict()
    for data in dataset:
        unite_name = fn(data)
        if unite_name not in united_dataset:
            united_dataset[unite_name] = []
        united_dataset[unite_name].append(data[1:])
    # unite dataset via maidenhair.loaders.base.unite_dataset
    for name, dataset in united_dataset.items():
        united_dataset[name] = _unite_dataset(dataset, basecolumn)[0]
    # create new dataset (respect the order of the dataset)
    dataset = []
    for name, _dataset in united_dataset.items():
        dataset.append([name] + _dataset)
    return dataset


def classify_dataset(dataset, fn):
    """
    Classify dataset via fn

    Args:
        dataset (list): A list of data
        fn (function): A function which recieve `data` and return string

    Returns:
        collection: A classified dataset (dict)
    """
    # classify dataset via classify_fn
    classified_dataset = OrderedDict()
    for data in dataset:
        classify_name = fn(data)
        if classify_name not in classified_dataset:
            classified_dataset[classify_name] = []
        classified_dataset[classify_name].append(data)
    return classified_dataset
