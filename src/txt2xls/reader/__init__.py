# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import maidenhair
from maidenhair.utils.plugins import registry
from maidenhair.filters.relative import relative
from maidenhair.filters.baseline import baseline
from maidenhair.classification.unite import unite_dataset
from maidenhair.classification.classify import classify_dataset
from txt2xls.function import parse_function


class Reader(object):
    def __init__(self, conf):
        self.parser = registry.find(conf['parser'])()
        self.loader = registry.find(conf['loader'])()
        self.using = conf['using']

        # classify
        def config_classify(conf):
            self.classify = conf['enabled']
            self.classify_function = parse_function(conf['function'])
        config_classify(conf['classify'])

        # unite
        def config_unite(conf):
            self.unite = conf['enabled']
            self.unite_function = parse_function(conf['function'])
            self.unite_basecolumn = conf['basecolumn']
        config_unite(conf['unite'])

        # relative
        # Note:
        #   basecolumn +1 for filename column
        def config_relative(conf):
            self.relative = conf['enabled']
            self.relative_origin = conf['origin']
            self.relative_basecolumn = conf['basecolumn'] + 1
        config_relative(conf['relative'])

        # baseline
        # Note:
        #   basecolumn +1 for filename column
        def config_baseline(conf):
            self.baseline = conf['enabled']
            self.baseline_function = parse_function(conf['function'])
            self.baseline_basecolumn = conf['basecolumn'] + 1
        config_baseline(conf['baseline'])

    def read(self, pathname, fail_silently):
        # load dataset with filename without
        # - unite
        # - relative
        # - baseline
        # because there will be proceeded in txt2xls way
        dataset = maidenhair.load(pathname,
                                  using=self.using,
                                  unite=False,
                                  relative=False,
                                  baseline=None,
                                  parser=self.parser,
                                  loader=self.loader,
                                  with_filename=True)
        # classify dataset
        if self.classify:
            collection = classify_dataset(dataset, self.classify_function)
        else:
            collection = {'': dataset}

        # run processes
        for name, dataset in collection.items():
            # unite dataset
            if self.unite:
                dataset = unite_dataset(dataset,
                                        self.unite_basecolumn,
                                        self.unite_function)
            # baseline
            if self.baseline:
                dataset = baseline(dataset,
                                   self.baseline_basecolumn,
                                   self.baseline_function,
                                   fail_silently)
            # relative
            if self.relative:
                dataset = relative(dataset,
                                   self.relative_origin,
                                   self.relative_basecolumn,
                                   fail_silently)
            # save modified dataset into the collection
            collection[name] = dataset

        return collection
