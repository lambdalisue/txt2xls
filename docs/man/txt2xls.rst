txt2xls manual page
====================

Synopsis
----------
**txt2xls** [*options*] -o <*output filename*> [*pathnames* ...]


Description
------------
:program:`txt2xls` is a tool for automatic convertion for raw text files
into a single Microsoft Excel file.

It use maidenhair_ parser and loader plugins for loading raw text files.
It means that :program:`txt2xls` can load any formats of raw text files when
there are plugins suite for the format.

.. _maidenhair: https://github.com/lambdalisue/maidenhair

Options
--------
``-h, --help``
    show this help message and exit
``-v, --version``
    show program's version number and exit
``--raise-exception``
    If it is specified, raise exceptions.
``-o OUTFILE, --outfile OUTFILE``
    An output filename without extensions. The required
    filename extension will be automatically determined
    from an output format.

Reading options
~~~~~~~~~~~~~~~~~~~~~~
``-p PARSER, --parser PARSER``
    A maidenhair parser name which will be used to parse
    the raw text data.
``-l LOADER, --loader LOADER``
    A maidenhair loader name which will be used to load
    the raw text data.
``-u USING, --using USING``
    A colon (:) separated column indexes. It is used for
    limiting the reading columns.

Unite options
~~~~~~~~~~~~~~~~~~~~~~
``--unite``
    Join the columns of classified dataset with respecting
    `--unite-basecolumn`. The dataset is classified with
    `--unite-function`.
``--unite-basecolumn UNITE_BASECOLUMN``
    An index of columns which will be used as a base
    column for regulating data point region.
``--unite-function UNITE_FUNCTION``
    A python script file path or a content of python
    lambda expression which will be used for classifing
    dataset. If it is not spcified, a filename character
    before period (.) will be used to classify.
    See **Function expression** section below.

Classify options
~~~~~~~~~~~~~~~~~~~~~~
``--classify``
    Classify dataset with --classify-function. It will
    influence the results of --relative and --baseline.
``--classify-function CLASSIFY_FUNCTION``
    A python script file path or a content of python
    lambda expression which will be used for classifing
    dataset. If it is not specified, a filename character
    before the last underscore (_) will be used to
    classify.
    See **Function expression** section below.

Relative options
~~~~~~~~~~~~~~~~~~~~~~
``--relative``
    If it is True, the raw data will be converted to
    relative data from the specified origin, based on the
    specified column. See `--relative-origin` and
    `--relative-basecolumn` also.
``--relative-origin RELATIVE_ORIGIN``
    A dataset number which will be used as an orign of the
    relative data. It is used with `--relative` option.
``--relative-basecolumn RELATIVE_BASECOLUMN``
    A column number which will be used as a base column to
    make the data relative. It is used with `--relative`
    option.

Baseline options
~~~~~~~~~~~~~~~~~~~~~~
``--baseline``
    If it is specified, the specified data file is used as
    a baseline of the dataset. See `--baseline-basecolumn`
    and `--baseline-function` also.
``--baseline-basecolumn BASELINE_BASECOLUMN``
    A column index which will be proceeded for baseline
    regulation. It is used with `--baseline` option.
``--baseline-function BASELINE_FUNCTION``
    A python script file path or a content of python
    lambda expression which will be used to determine the
    baseline value from the data. `columns` and `column`
    variables are available in the lambda expression.
    See **Function expression** section below.

Peakset options
~~~~~~~~~~~~~~~~~~~~~~
``--peakset-method {argmin, argmax}``
    A method to find peak data point.
``--peakset-basecolumn PEAKSET_BASECOLUMN``
    A column index which will be used for finding peak
    data point.
``--peakset-where-function PEAKSET_WHERE_FUNCTION``
    A python script file path or a content of python
    lambda expression which will be used to limit the
    range of data points for finding. peak data point.
    `data` is available in the lambda expression.
    See **Function expression** section below.


Function expression
--------------------
There are four types of function expressions and there are identified by
leading function type indicator; characters before the first colon (:).

lambda function
~~~~~~~~~~~~~~~~
A function expression starts from ``lambda:`` indicate the lambda function
expression and the body (string after the ``lambda:``) indicate the body of
the lambda function.
The lambda function will recieve ``*args`` and ``**kwargs`` arguments when it
is called so you can write a lambda function which return the first argument
as::

    lambda:args[0]

The function expression above will be converted to::

    lambda *args, **kwargs: args[0]

regex function
~~~~~~~~~~~~~~~
A function expression starts from ``regex:`` indicate the regex function
expression and the body indicate the regular expression pattern string.
The regex function will recieve ``data`` which first item indicate the
filename of the data (a row text filename) and the function check the filename
with the specified regular expression pattern.
This function is mainly used for classification function such as
``--unite-function`` or ``--classify-function``.

If the regular expression pattern has group patterns, it will return the first
group as a classification string.
It it does not have group patterns, it will return the entire match string.
If nothing can be mathced in the specified filename, entire filename will be
returned as a classification string.

file function
~~~~~~~~~~~~~~
A function expression starts from ``file:`` indicate the file function
expression and the body indicate the path of the python script.
The python script will be loaded and it's ``__call__(data)`` function will be
used as a function.
It the python script does not have the function, it raise ``ImportError``.

builtin function
~~~~~~~~~~~~~~~~~
A function expression starts from ``builtin:`` is a shortcut alias of file
function which points to builtin python script files.
Currently four builtin scripts are available (``baseline_function``,
``classify_function``, ``unite_function``, and ``where_function``).

Preference
-----------
You can create configure file as ``~/.config/txt2xls/txt2xls.cfg`` (Linux),
``~/.txt2xls.cfg`` (Mac), or ``%APPDATA%\txt2xls\txt2xls.cfg`` (Windows).

The default preference is equal to the configure file as below::

    [default]
    raise_exception = False

    [reader]
    parser = 'parsers.PlainParser'
    loader = 'loaders.PlainLoader'
    using = None

        [[classify]]
        enabled = False
        function = 'builtin:classify_function'

        [[unite]]
        enabled = False
        function = 'builtin:unite_function'
        basecolumn = 0

        [[relative]]
        enabled = False
        origin = 0
        basecolumn = 1

        [[baseline]]
        enabled = False
        function = 'builtin:baseline_function'
        basecolumn = 1

    [writer]
    default_filename = 'output.xls'

        [[peakset]]
        method = 'argmax'
        basecolumn = -1
        where_function = 'builtin:where_function'

