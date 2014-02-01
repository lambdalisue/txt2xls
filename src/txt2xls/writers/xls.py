# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import numpy as np
from xlwt import Formula
from xlwt import Workbook
from xlwt.Utils import rowcol_pair_to_cellrange
import maidenhair.statistics
import txt2xls.utils


def ensure_iterable(axis):
    """
    Ensure the axis is iterable (XY array)

    >>> axis1 = [
    ...     [0, 1, 2],
    ...     [3, 4, 5],
    ...     [6, 7, 8],
    ... ]
    >>> assert axis1 == ensure_iterable(axis1)
    >>> axis21 = [0, 1, 2]
    >>> axis22 = [[0], [1], [2]]
    >>> assert axis22 == ensure_iterable(axis21)
    """
    iterable = (np.ndarray, list, tuple)
    if not isinstance(axis[0], iterable):
        return [[r] for r in axis]
    return axis


def prefer_alphabet(i):
    """
    Convert an integer to an alphabet if it is within 0 to 51.

    >>> prefer_alphabet(0)
    'A'
    >>> prefer_alphabet(25)
    'Z'
    >>> prefer_alphabet(26)
    'a'
    >>> prefer_alphabet(51)
    'z'
    >>> prefer_alphabet(100)
    '100'
    """
    if 0 <= i <= 25:
        return chr(i + 65)
    if 26 <= i <= 51:
        return chr(i + 97 - 26)
    return str(i)

def write(filename, dataset):
    book = Workbook()
    write_dataset(book, dataset)
    if len(dataset) > 1:
        write_peakset(book, dataset)
    book.save(filename)


def write_sheet(sheet, axes, offset=0):
    for a, axis in enumerate(axes):
        # ensure iterable
        axis = ensure_iterable(axis)
        # write header into sheet
        ncol = len(axis[0])
        header = ["%s %d" % (prefer_alphabet(a), i+1) for i in range(ncol)]
        if ncol > 1:
            header += ['Avg']
            ncol += 1
        if ncol > 2:
            header += ['Std']
            ncol += 1
        for c, cell in enumerate(header):
            sheet.write(0, c+offset, cell)

        # write data into sheet
        for r, columns in enumerate(axis):
            for c, cell in enumerate(columns):
                sheet.write(r+1, c+offset, cell)
            # get cell range
            cr = rowcol_pair_to_cellrange(
                    r+1, offset,
                    r+1, offset+len(columns)-1)
            # add average if there are more than 1 column
            if ncol > 1:
                sheet.write(r+1, offset+len(columns),
                            Formula('average(%s)' % cr))
            # add stdev if there are more than 2 columns
            if ncol > 2:
                sheet.write(r+1, offset+len(columns)+1,
                            Formula('stdev(%s)' % cr))
        offset += ncol + 1

def write_dataset(book, dataset):
    for data in dataset:
        sheet_name = data[0]
        sheet_name = os.path.basename(sheet_name)
        sheet_name = os.path.splitext(sheet_name)[0]
        sheet = book.add_sheet(sheet_name)
        write_sheet(sheet, data[1:])

def write_peakset(book, dataset):
    sheet = book.add_sheet('peakset')

    # write filenames
    for r, data in enumerate(dataset):
        filename = data[0]
        filename = os.path.basename(filename)
        filename = os.path.splitext(filename)[0]
        sheet.write(r+1, 0, filename)
    # write peakset
    peakset = txt2xls.utils.find_peaks(dataset,
                                       basecolumn=-1,
                                       method='argmax')
    write_sheet(sheet, peakset, 1)
