# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import collections
import maidenhair
from maidenhair.utils.plugins import registry
from maidenhair.filters.relative import relative
from maidenhair.filters.baseline import baseline
from txt2xls.readers.utils import unite_dataset
from txt2xls.readers.utils import classify_dataset


class Reader(object):
    def read(self, pathname, conf):
        # get arguments from configobj
        using = conf['maidenhair']['using']
        parser_class = registry.find(conf['maidenhair']['parser'])
        loader_class = registry.find(conf['maidenhair']['loader'])

        # load dataset with filename without
        # - unite
        # - relative
        # - baseline
        # because there will be proceeded in txt2xls way
        dataset = maidenhair.load(pathname,
                                  using=using,
                                  unite=False,
                                  relative=False,
                                  baseline=None,
                                  parser=parser_class(),
                                  loader=loader_class(),
                                  with_filename=True)

        # unite dataset
        if conf['maidenhair']['unite']:
            dataset = self._unite(dataset, conf)

        # classify dataset or put everything in an item of dictionary
        if conf['maidenhair']['classify']:
            collection = self._classify(dataset, conf)
        else:
            collection = collections.OrderedDict(**{'': dataset})

        # modulate dataset
        if conf['filters']['baseline']:
            collection = self._baseline(collection, conf)
        if conf['filters']['relative']:
            collection = self._relative(collection, conf)

        return collection


    def _unite(self, dataset, conf):
        # get arguments from configobj
        unite_basecolumn = conf['maidenhair']['unite_basecolumn']
        unite_function = conf['maidenhair']['unite_function']
        if unite_function is not None:
            if os.path.exists(unite_function):
                unite_function = execfile(unite_function, {}, kwargs)
            elif unite_function.startswith('regex '):
                unite_function = regex_function(unite_function)
            else:
                unite_function = "lambda data: %s" % unite_function
                unite_function = eval(unite_function)
        dataset = unite_dataset(dataset,
                                unite_basecolumn,
                                unite_function)
        return dataset

    def _classify(self, dataset, conf):
        # get arguments from configobj
        classify_function = conf['maidenhair']['classify_function']
        if classify_function is not None:
            if os.path.exists(classify_function):
                classify_function = execfile(classify_function, {}, kwargs)
            elif classify_function.startswith('regex '):
                classify_function = regex_function(classify_function)
            else:
                classify_function = "lambda data: %s" % classify_function
                classify_function = eval(classify_function)
        collection = classify_dataset(dataset,
                                      classify_function)
        return collection

    def _baseline(self, collection, conf):
        # get arguments from configobj
        fail_silently = not conf['main']['raise_exception']
        baseline_function = conf['filters']['baseline_function']
        baseline_basecolumn = conf['filters']['baseline_basecolumn']

        kwargs = {'column': baseline_basecolumn + 1}
        if os.path.exists(baseline_function):
            baseline_function = execfile(baseline_function, {}, kwargs)
        else:
            baseline_function = "lambda *columns: %s" % baseline_function
            baseline_function = eval(baseline_function, {}, kwargs)

        for name, dataset in collection.items():
            # Note: +1 for omitting filename column
            collection[name] = relative(dataset,
                                        baseline_column + 1,
                                        baseline_function,
                                        fail_silently)
        return collection

    def _relative(self, collection, conf):
        # get arguments from configobj
        fail_silently = not conf['main']['raise_exception']
        relative_origin = conf['filters']['relative_origin']
        relative_basecolumn = conf['filters']['relative_basecolumn']

        for name, dataset in collection.items():
            # Note: +1 for omitting filename column
            collection[name] = relative(dataset,
                                        relative_origin,
                                        relative_basecolumn + 1,
                                        fail_silently)
        return collection

