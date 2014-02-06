# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import numpy as np
import maidenhair.statistics


def find_peakset(dataset, basecolumn=-1, method='', where=None):
    """
    Find peakset from the dataset

    Args:
        dataset (list): A list of data
        basecolumn (int): An index of column for finding peaks
        method (str): A method name of numpy for finding peaks
        where (function): A function which recieve ``data`` and return
            numpy indexing list

    Returns:
        peakset: A list of peaks of each axis (list)
    """
    peakset = []
    for data in dataset:
        base = data[basecolumn]
        base = maidenhair.statistics.average(base)
        # limit data points
        if where:
            base = base[np.where(where(data))]
        # find peak index
        index = getattr(np, method, np.argmax)(base)
        # create peakset
        for a, axis in enumerate(data[1:]):
            if len(peakset) <= a:
                peakset.append([])
            peakset[a].append(axis[index])
    peakset = np.array(peakset)
    return peakset
