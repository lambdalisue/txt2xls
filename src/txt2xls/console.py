#!/usr/bin/env python
# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'

def txt2xls(args=None):
    from txt2xls.conf.args import parse_args
    from txt2xls.conf.conf import parse_conf
    from txt2xls.readers import Reader
    from txt2xls.writers import Writer

    # parse config file and arguments
    args = parse_args(args)
    conf = parse_conf('txt2xls', args)

    # read
    reader = Reader()
    collection = reader.read(args.infiles, conf)

    # write
    writer = Writer()
    writer.write(collection, conf['main']['output'] + ".xls")

if __name__ == '__main__':
    txt2xls()
