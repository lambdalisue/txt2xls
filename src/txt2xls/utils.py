# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import numpy as np
import maidenhair.statistics


def find_peakset(dataset, basecolumn=-1, method=''):
    peakset = []
    for data in dataset:
        # find index
        abase = maidenhair.statistics.average(data[basecolumn])
        index = getattr(np, method, 'argmax')(abase)
        # create peakset
        for a, axis in enumerate(data[1:]):
            if len(peakset) <= a:
                peakset.append([])
            peakset[a].append(axis[index])
    peakset = np.array(peakset)
    return peakset
