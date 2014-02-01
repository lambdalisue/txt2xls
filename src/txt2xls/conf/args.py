# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import re
import argparse
import txt2xls


class ParseUsingAction(argparse.Action):
    pattern = re.compile(r"(\d+):(\d+)")
    def __call__(self, parser, namespace, values, option_string=None):
        m = self.pattern.match(values)
        if m is None:
            raise AttributeError('using options should be a comma separated '
                                 'column numbers (e.g. "0:1").')
        lhs = int(m.group(1))
        rhs = int(m.group(2))
        # save in namespace
        setattr(namespace, 'using', (lhs, rhs))


def parse_args(args=None):
    usage = None
    description = None
    parser = argparse.ArgumentParser(prog='txt2xls',
                                     usage=usage,
                                     description=description,
                                     version=txt2xls.__version__)

    parser.add_argument('-o', '--output', default=None,
                        help=('An output filename without extensions. '
                              'The required filename extension will be '
                              'automatically determined from an output format.'))
    parser.add_argument('--raise-exceptions', default=None,
                        action='store_true',
                        help=('If it is specified, raise exceptions.'))
    parser.add_argument('-p', '--parser', default=None,
                        help=('A maidenhair parser name which will be used to '
                              'parse the raw text data. '
                              'If it is not specified, a parser which was '
                              'specified in a txt2xls configure file will be '
                              'used.'))
    parser.add_argument('-l', '--loader', default=None,
                        help=('A maidenhair loader name which will be used to '
                              'load the raw text data. '
                              'If it is not specified, a parser which was '
                              'specified in a txt2xls configure file will be '
                              'used.'))
    parser.add_argument('-a', '--auto-unite', default=None, action='store_true',
                        help=('Automatically unite thedataset which '
                              'filename middle extensions have only integers. '
                              'See "Filename middle extensions" also.'))
    parser.add_argument('--unite-basecolumn', default=None, type=int,
                        help=('A column number which will be used to regulate '
                              'data regions for automatical unite. '
                              'See `--auto` option also.'))
    parser.add_argument('-u', '--using', default=None, action=ParseUsingAction,
                        help=('A colon separated column number of the raw text '
                              'data which will be used to determine X and Y '
                              'columns.'))
    parser.add_argument('--relative', default=None, action='store_true',
                        help=('If it is True, the raw data will be converted to '
                              'relative data from the specified origin, based '
                              'on the specified column. '
                              'See `--relative-origin` and '
                              '`--relative-basecolumn` also.'))
    parser.add_argument('--relative-origin', default=None, type=int,
                        help=('A dataset number which will be used as an orign '
                              'of the relative data. '
                              'It is used with `--relative` option.'))
    parser.add_argument('--relative-basecolumn', default=None, type=int,
                        help=('A column number which will be used as a base '
                              'column to make the data relative. '
                              'It is used with `--relative` option.'))
    parser.add_argument('--baseline', default=None, 
                        help=('If it is specified, the specified data file '
                              'is used as a baseline of the dataset. '
                              'See `--baseline-column` and '
                              '`--baseline-function` also.'))
    parser.add_argument('--baseline-column', default=None, type=int,
                        help=('A column number which will be proceeded for '
                              'baseline regulation. '
                              'It is used with `--baseline` option.'))
    parser.add_argument('--baseline-function',
                        default=None,
                        help=('A python code of a "lambda" function which is '
                              'used to determine the baseline value from the '
                              'data. '
                              '`columns` and `column` variables are '
                              'available in the code.'))
    parser.add_argument('infiles', nargs='+',
                        help=('Path list of data files or directories which '
                              'have data files. '))
    args = parser.parse_args(args)
    return args
