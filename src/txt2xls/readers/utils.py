# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import collections
from maidenhair.loaders.base import unite_dataset as _unite_dataset


def default_unite_fn(data):
    # data[0] indicate the filename of the data
    rootname, basename = os.path.split(data[0])
    filename, ext = os.path.splitext(basename)
    if '.' in filename:
        filename = filename.rsplit('.')[0]
    filename = os.path.join(rootname, filename + ext)
    return filename, data[1:]


def default_classify_fn(data):
    # data[0] indicate the filename of the data
    rootname, basename = os.path.split(data[0])
    filename, ext = os.path.splitext(basename)
    if '_' in filename:
        filename = filename.rsplit('_', 1)[0]
    filename = os.path.join(rootname, filename + ext)
    return filename, data


def unite_dataset(dataset, basecolumn, unite_fn=None):
    """
    Unite dataset via unite_fn

    Parameters
    ----------
    dataset : list
        A list of data
    basecolumn : int
        A number of column which will be respected in uniting dataset
    unite_fn : function
        A function which recieve `data` and return (string, data)

    Returns
    -------
    list
        A united dataset
    """
    # create default unite_fn
    if unite_fn is None:
        unite_fn = default_unite_fn
    # classify dataset via unite_fn
    united_dataset = collections.OrderedDict()
    for data in dataset:
        unite_name, data_mod = unite_fn(data)
        if unite_name not in united_dataset:
            united_dataset[unite_name] = []
        united_dataset[unite_name].append(data_mod)
    # unite dataset via maidenhair.loaders.base.unite_dataset
    for name, dataset in united_dataset.items():
        united_dataset[name] = _unite_dataset(dataset, basecolumn)[0]
    # create new dataset (respect the order of the dataset)
    dataset = []
    for name, _dataset in united_dataset.items():
        dataset.append([name] + _dataset)
    return dataset


def classify_dataset(dataset, classify_fn=None):
    """
    Classify dataset via classify_fn

    Parameters
    ----------
    dataset : list
        A list of data
    classify_fn : function
        A function which recieve `data` and return (string, data)

    Returns
    -------
    list
        A united dataset
    """
    # create default classify_fn
    if classify_fn is None:
        classify_fn = default_classify_fn
    # classify dataset via classify_fn
    classified_dataset = collections.OrderedDict()
    for data in dataset:
        classify_name, data_mod = classify_fn(data)
        if classify_name not in classified_dataset:
            classified_dataset[classify_name] = []
        classified_dataset[classify_name].append(data_mod)
    return classified_dataset
