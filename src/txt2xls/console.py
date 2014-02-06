#!/usr/bin/env python
# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'

def txt2xls(args=None):
    from txt2xls.args import parse_args
    from txt2xls.conf import parse_conf
    from txt2xls.reader import Reader
    from txt2xls.writer import Writer

    # parse config file and arguments
    args = parse_args(args)
    conf = parse_conf('txt2xls', args)

    fail_silently = not conf['default']['raise_exception']

    # read
    reader = Reader(conf['reader'])
    collection = reader.read(args.infiles, fail_silently)

    # write
    writer = Writer(conf['writer'])
    writer.write(collection, args.outfile, fail_silently)

if __name__ == '__main__':
    txt2xls()
