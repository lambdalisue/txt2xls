# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import numpy as np
from xlwt import Formula
from xlwt import Workbook
from xlwt.Utils import rowcol_pair_to_cellrange
from txt2xls.writers.utils import ensure_iterable
from txt2xls.writers.utils import prefer_alphabet
from txt2xls.writers.utils import get_sheet_name
from txt2xls.utils import find_peakset


class Writer(object):
    def write(self, collection, filename):
        book = Workbook()

        # write dataset
        for name, dataset in collection.items():
            self._write_dataset(dataset, book)

        # write peakset if there are more than single dataset
        if len(dataset) > 1:
            sheet = book.add_sheet('peakset')
            offsets = [0, 1]
            for name, dataset in collection.items():
                # write classify name
                # Note: +1 for heading line
                sheet.write(offsets[0]+1, 0, get_sheet_name(name))
                # write peakset
                self._write_peakset(dataset, offsets, sheet)
                # update offsets
                offsets[0] += len(dataset) + 1

        # save
        book.save(filename)


    def _write_axis_header(self, a, axis, offsets, sheet):
        """
        Write axis header

        Args:
            a (int): An index of the axis
            axis (iterable): An axis
            offsets (list): A list of row and column offsets
            sheet (instance): An instance of xlwt sheet

        Returns:
            header: A list of header strings
        """
        # find the maximum number of columns
        ncol = max([len(columns) for columns in axis])
        # create alphabetic headers
        header = ["%s %d" % (prefer_alphabet(a), i+1) for i in range(ncol)]
        # are Avg and Std columns required?
        avg_required = ncol > 1
        std_required = ncol > 2
        # add Avg and/or Std columns if these are required
        if avg_required:
            header.append('Avg')
        if std_required:
            header.append('Std')
        # write header
        for c, cell in enumerate(header):
            sheet.write(offsets[0], offsets[1]+c, cell)
        return header


    def _write_axes(self, axes, offsets, sheet):
        """
        Write axes

        Args:
            axes (list): A list of axes
            offsets (list): A list of row and column offsets
            sheet (instance): An instance of xlwt sheet
        """
        for a, axis in enumerate(axes):
            # ensure axis is iterable
            axis = ensure_iterable(axis)
            # write header
            header = self._write_axis_header(a, axis, offsets, sheet)
            # write data
            for r, columns in enumerate(axis):
                for c, cell in enumerate(columns):
                    sheet.write(offsets[0]+1+r,
                                offsets[1]+c,
                                cell)
                # create cell range
                crange = rowcol_pair_to_cellrange(
                        offsets[0]+1+r, offsets[1],
                        offsets[0]+1+r, offsets[1] + len(columns) - 1)
                # Add average if it is required
                if 'Avg' in header:
                    ind = header.index('Avg')
                    sheet.write(offsets[0]+1+r,
                                offsets[1]+ind,
                                Formula('average(%s)' % crange))
                # Add stdev if it is required
                if 'Std' in header:
                    ind = header.index('Std')
                    sheet.write(offsets[0]+1+r,
                                offsets[1]+ind,
                                Formula('stdev(%s)' % crange))
            # update column offset
            offsets[1] += len(header) + 1

    def _write_dataset(self, dataset, book):
        """
        Write dataset

        Args:
            dataset (list): A list of data
            book (instance): An instance of xlwt book
        """
        for i, data in enumerate(dataset):
            # create sheet name from dataset name
            sheet_name = get_sheet_name(data[0])
            # create sheet
            sheet = book.add_sheet(sheet_name)
            # write axes
            self._write_axes(data[1:], [0, 0], sheet)

    def _write_peakset(self, dataset, offsets, sheet):
        """
        Write peakset of the dataset

        Args:
            dataset (list): A list of data
            offsets (list): A list of row and column offsets
            sheet (instance): An instance of xlwt sheet
            instance

        Returns:
            sheet: An instance of xlwt sheet
        """
        # write filenames
        for r, data in enumerate(dataset):
            name = get_sheet_name(data[0])
            # Note: +1 for heading line
            sheet.write(offsets[0]+r+1, offsets[1], name)
        # write peakset
        peakset = find_peakset(dataset,
                               basecolumn=-1,
                               method='argmax')
        self._write_axes(peakset, [offsets[0], offsets[1]+1], sheet)

