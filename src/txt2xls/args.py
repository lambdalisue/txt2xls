# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import re
import argparse
import txt2xls

USING_FORMAT_PATTERN = re.compile(r"^(\d+:)*\d+$")

def parse_using(value):
    m = USING_FORMAT_PATTERN.match(value)
    if m is None:
        raise argparse.ArgumentTypeError('Value has to be a colon (:) '
                                         'separated column indexes (e.g. '
                                         '"0:1" or "0:1:2").')
    indexes = value.split(":")
    return tuple(map(int, indexes))


def parse_args(args=None):
    usage = None
    description = None

    parser = argparse.ArgumentParser(prog='txt2xls',
                                     usage=usage,
                                     description=description,
                                     version=txt2xls.__version__)

    group1 = parser.add_argument_group('Reading options')
    group1.add_argument('-p', '--parser', default=None,
                        help=('A maidenhair parser name which will be used to '
                              'parse the raw text data.'))
    group1.add_argument('-l', '--loader', default=None,
                        help=('A maidenhair loader name which will be used to '
                              'load the raw text data.'))
    group1.add_argument('-u', '--using', default=None, type=parse_using,
                        help=('A colon (:) separated column indexes. '
                              'It is used for limiting the reading columns.'))
    # unite
    group2 = parser.add_argument_group('Unite options')
    group2.add_argument('--unite', default=None, action='store_true',
                        help=('Join the columns of classified dataset with '
                              'respecting --unite-basecolumn.'
                              'The dataset is classified with '
                              '--unite-function.'))
    group2.add_argument('--unite-basecolumn', default=None, type=int,
                        help=('An index of columns which will be used as a '
                              'base column for regulating data point region. '))
    group2.add_argument('--unite-function', default=None,
                        help=('A python script file path or a content of '
                              'python lambda expression which will be used '
                              'for classifing dataset. '
                              'If it is not spcified, a filename character '
                              'before period (.) will be used to classify.'))
    # classify
    group3 = parser.add_argument_group('Classify options')
    group3.add_argument('--classify', default=None, action='store_true',
                        help=('Classify dataset with --classify-function. '
                              'It will influence the results of --relative '
                              'and --baseline.'))
    group3.add_argument('--classify-function', default=None,
                        help=('A python script file path or a content of '
                              'python lambda expression which will be used '
                              'for classifing dataset. '
                              'If it is not specified, a filename character '
                              'before the last underscore (_) will be used '
                              'to classify.'))
    # relative
    group4 = parser.add_argument_group('Relative options')
    group4.add_argument('--relative', default=None, action='store_true',
                        help=('If it is True, the raw data will be converted to '
                              'relative data from the specified origin, based '
                              'on the specified column. '
                              'See `--relative-origin` and '
                              '`--relative-basecolumn` also.'))
    group4.add_argument('--relative-origin', default=None, type=int,
                        help=('A dataset number which will be used as an orign '
                              'of the relative data. '
                              'It is used with `--relative` option.'))
    group4.add_argument('--relative-basecolumn', default=None, type=int,
                        help=('A column number which will be used as a base '
                              'column to make the data relative. '
                              'It is used with `--relative` option.'))
    # baseline
    group5 = parser.add_argument_group('Baseline options')
    group5.add_argument('--baseline', default=None, action='store_true',
                        help=('If it is specified, the specified data file '
                              'is used as a baseline of the dataset. '
                              'See `--baseline-basecolumn` and '
                              '`--baseline-function` also.'))
    group5.add_argument('--baseline-basecolumn', default=None, type=int,
                        help=('A column index which will be proceeded for '
                              'baseline regulation. '
                              'It is used with `--baseline` option.'))
    group5.add_argument('--baseline-function',
                        default=None,
                        help=('A python script file path or a content of '
                              'python lambda expression which will be used to '
                              'determine the baseline value from the data. '
                              '`columns` and `column` variables are '
                              'available in the lambda expression.'))
    # peakset
    group6 = parser.add_argument_group('Peakset options')
    group6.add_argument('--peakset-method', default=None,
                        choices=('argmax', 'argmin'),
                        help=('A method to find peak data point. '))
    group6.add_argument('--peakset-basecolumn', default=None, type=int,
                        help=('A column index which will be used for '
                              'finding peak data point. '))
    group6.add_argument('--peakset-where-function', default=None,
                        help=('A python script file path or a content of '
                              'python lambda expression which will be used to '
                              'limit the range of data points for finding. '
                              'peak data point. '
                              '`data` is available in the lambda expression.'))
    parser.add_argument('--raise-exception', default=None,
                        action='store_true',
                        help=('If it is specified, raise exceptions.'))
    parser.add_argument('-o', '--outfile', default=None,
                        help=('An output filename without extensions. '
                              'The required filename extension will be '
                              'automatically determined from an output format.'))
    parser.add_argument('infiles', nargs='+',
                        help=('Path list of data files or directories which '
                              'have data files. '))
    args = parser.parse_args(args)
    return args
