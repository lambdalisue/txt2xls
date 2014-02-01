#!/usr/bin/env python
# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from txt2xls.conf.args import parse_args
from txt2xls.conf.conf import parse_conf

def txt2xls(args=None):
    from txt2xls.readers.txt import read
    from txt2xls.writers.xls import write

    # parse config file and arguments
    args = parse_args(args)
    conf = parse_conf('txt2xls', args)

    # read
    dataset = read(args.infiles, conf)

    # write
    write(conf['main']['output'] + ".xls", dataset)

if __name__ == '__main__':
    txt2xls()
