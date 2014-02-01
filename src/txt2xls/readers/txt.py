# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import natsort
import maidenhair
from maidenhair.utils.plugins import registry
from maidenhair.filters.relative import relative
from maidenhair.filters.baseline import baseline
from maidenhair.loaders.base import unite_dataset


def read(pathname, conf):
    fail_silently = not conf['main']['raise_exception']
    # find parser/loader class from registry
    parser_class = registry.find(conf['maidenhair']['parser'])
    loader_class = registry.find(conf['maidenhair']['loader'])

    # load dataset with filename
    dataset = maidenhair.load(pathname,
                              using=conf['maidenhair']['using'],
                              unite=False,
                              relative=False,
                              baseline=None,
                              parser=parser_class(),
                              loader=loader_class(),
                              with_filename=True)
    # auto unite
    if conf['maidenhair']['auto_unite']:
        dataset = auto_unite(dataset, conf['maidenhair']['unite_basecolumn'])
        
    # modulate dataset
    if conf['filters']['baseline']:
        # create baseline function from specified partial python code
        baseline_column = conf['filters']['baseline_column'] + 1
        baseline_function = conf['filters']['baseline_function']
        kwargs = {
            'column': baseline_column,
        }
        fn = eval("lambda *columns: %s" % baseline_function, {}, kwargs)
        dataset = baseline(dataset,
                           column=baseline_column,
                           fn=fn,
                           fail_silently=fail_silently)
    if conf['filters']['relative']:
        relative_origin = conf['filters']['relative_origin']
        relative_basecolumn = conf['filters']['relative_basecolumn'] + 1
        dataset = relative(dataset,
                           ori=relative_origin,
                           column=relative_basecolumn,
                           fail_silently=fail_silently)
    return dataset


def auto_unite(dataset, basecolumn):
    united_dataset = {}
    # clusterize dataset with filename
    for data in dataset:
        rootname, basename = os.path.split(data[0])
        filename, ext = os.path.splitext(basename)
        if '.' in filename:
            filename = filename.rsplit('.')[0]
        filename = os.path.join(rootname, filename + ext)
        if filename not in united_dataset:
            united_dataset[filename] =[]
        united_dataset[filename].append(data[1:])
    # unite dataset
    for key, value in united_dataset.items():
        united_dataset[key] = unite_dataset(value, basecolumn)[0]
    # create new dataset
    dataset = []
    for key, value in united_dataset.items():
        dataset.append([key] + value)
    # naturally sort with filename
    dataset = natsort.natsorted(dataset,
                                key=lambda x: x[0],
                                number_type=None)
    return dataset
