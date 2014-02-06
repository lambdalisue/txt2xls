#!/usr/bin/env nosetests -v
# coding=utf-8
from nose.tools import *
import numpy as np
from argparse import ArgumentTypeError
from mock import MagicMock as Mock

from txt2xls.args import parse_using
from txt2xls.args import parse_args


#-------------------------------------------------------------------------------
# parse_using
#-------------------------------------------------------------------------------
def test_parse_using_valid_format():
    eq_(parse_using('0:1'), (0, 1))
    eq_(parse_using('0:1:2'), (0, 1, 2))

@raises(ArgumentTypeError)
def test_parse_using_format1():
    parse_using('0:')

@raises(ArgumentTypeError)
def test_parse_using_format2():
    parse_using(':1')

@raises(ArgumentTypeError)
def test_parse_using_format3():
    parse_using('foo')


#-------------------------------------------------------------------------------
# parse_args
#-------------------------------------------------------------------------------
# reading options
def test_parse_args_parser_short():
    args = parse_args(['-p', 'foobar', 'piyo'])
    eq_(args.parser, 'foobar')
def test_parse_args_parser():
    args = parse_args(['--parser', 'foobar', 'piyo'])
    eq_(args.parser, 'foobar')
def test_parse_args_loader_short():
    args = parse_args(['-l', 'foobar', 'piyo'])
    eq_(args.loader, 'foobar')
def test_parse_args_loader():
    args = parse_args(['--loader', 'foobar', 'piyo'])
    eq_(args.loader, 'foobar')
def test_parse_args_using_short():
    args = parse_args(['-u', '0:1', 'piyo'])
    eq_(args.using, (0, 1))
def test_parse_args_using():
    args = parse_args(['--using', '0:1:2', 'piyo'])
    eq_(args.using, (0, 1, 2))

# unite options
def test_parse_args_unite():
    args = parse_args(['--unite', 'piyo'])
    ok_(args.unite)
def test_parse_args_unite_basecolumn():
    args = parse_args(['--unite-basecolumn', '10', 'piyo'])
    eq_(args.unite_basecolumn, 10)
def test_parse_args_unite_function():
    args = parse_args(['--unite-function', 'foo', 'piyo'])
    eq_(args.unite_function, 'foo')

# classify options
def test_parse_args_classify():
    args = parse_args(['--classify', 'piyo'])
    ok_(args.classify)
def test_parse_args_classify_function():
    args = parse_args(['--classify-function', 'foo', 'piyo'])
    eq_(args.classify_function, 'foo')

# relative options
def test_parse_args_relative():
    args = parse_args(['--relative', 'piyo'])
    ok_(args.relative)
def test_parse_args_relative_basecolumn():
    args = parse_args(['--relative-basecolumn', '10', 'piyo'])
    eq_(args.relative_basecolumn, 10)
def test_parse_args_relative_function():
    args = parse_args(['--relative-origin', '10', 'piyo'])
    eq_(args.relative_origin, 10)

# baseline options
def test_parse_args_baseline():
    args = parse_args(['--baseline', 'piyo'])
    ok_(args.baseline)
def test_parse_args_baseline_basecolumn():
    args = parse_args(['--baseline-basecolumn', '10', 'piyo'])
    eq_(args.baseline_basecolumn, 10)
def test_parse_args_baseline_function():
    args = parse_args(['--baseline-function', 'foo', 'piyo'])
    eq_(args.baseline_function, 'foo')

# peakset options
def test_parse_args_peakset_method():
    args = parse_args(['--peakset-method', 'argmin', 'piyo'])
    eq_(args.peakset_method, 'argmin')
def test_parse_args_peakset_basecolumn():
    args = parse_args(['--peakset-basecolumn', '10', 'piyo'])
    eq_(args.peakset_basecolumn, 10)
def test_parse_args_peakset_where_function():
    args = parse_args(['--peakset-where-function', 'foo', 'piyo'])
    eq_(args.peakset_where_function, 'foo')

# other options
def test_parse_args_raise_exception():
    args = parse_args(['--raise-exception', 'piyo'])
    ok_(args.raise_exception)
def test_parse_args_outfile():
    args = parse_args(['--outfile', 'foo', 'piyo'])
    eq_(args.outfile, 'foo')
def test_parse_args_infiles():
    args = parse_args(['foo', 'bar', 'piyo'])
    eq_(args.infiles, ['foo', 'bar', 'piyo'])
