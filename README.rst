txt2xls
==========================
.. image:: https://secure.travis-ci.org/lambdalisue/txt2xls.png?branch=master
    :target: http://travis-ci.org/lambdalisue/txt2xls
    :alt: Build status

.. image:: https://coveralls.io/repos/lambdalisue/txt2xls/badge.png?branch=master
    :target: https://coveralls.io/r/lambdalisue/txt2xls/
    :alt: Coverage

.. image:: https://pypip.in/d/txt2xls/badge.png
    :target: https://pypi.python.org/pypi/txt2xls/
    :alt: Downloads

.. image:: https://pypip.in/v/txt2xls/badge.png
    :target: https://pypi.python.org/pypi/txt2xls/
    :alt: Latest version

.. image:: https://pypip.in/wheel/txt2xls/badge.png
    :target: https://pypi.python.org/pypi/txt2xls/
    :alt: Wheel Status

.. image:: https://pypip.in/egg/txt2xls/badge.png
    :target: https://pypi.python.org/pypi/txt2xls/
    :alt: Egg Status

.. image:: https://pypip.in/license/txt2xls/badge.png
    :target: https://pypi.python.org/pypi/txt2xls/
    :alt: License

txt2xls convert raw text data files into a single excel file.
It use `maidenhair <https://github.com/lambdalisue/maidenhair>`_ for reading raw
text files so any kind of raw text file can be used if there is a maidenhair
plugins.

Installation
------------
Use pip_ like::

    $ pip install txt2xls

.. _pip:  https://pypi.python.org/pypi/pip

Quick Usage
-------------
Assume there are several raw text data files like::

    # Sample1.txt
    0 10
    1 20
    2 30
    3 40
    4 50
    5 60
    # Sample2.txt
    0 15
    1 25
    2 35
    3 45
    4 55
    5 65
    # Sample3.txt
    0 12
    1 22
    2 32
    3 42
    4 52
    5 62

Then run *txt2xls* with

    % txt2xls -o output Sample*.txt

It will produce ``output.xls`` file.
The excel file have ``Sample1``, ``Sample2``, and ``Sample3`` sheets.

Usage
------

::

    usage: txt2xls [-h] [-v] [-p PARSER] [-l LOADER] [-u USING] [--unite]
                [--unite-basecolumn UNITE_BASECOLUMN]
                [--unite-function UNITE_FUNCTION] [--classify]
                [--classify-function CLASSIFY_FUNCTION] [--relative]
                [--relative-origin RELATIVE_ORIGIN]
                [--relative-basecolumn RELATIVE_BASECOLUMN] [--baseline]
                [--baseline-basecolumn BASELINE_BASECOLUMN]
                [--baseline-function BASELINE_FUNCTION]
                [--peakset-method {argmax,argmin}]
                [--peakset-basecolumn PEAKSET_BASECOLUMN]
                [--peakset-where-function PEAKSET_WHERE_FUNCTION]
                [--raise-exception] [-o OUTFILE]
                infiles [infiles ...]

    positional arguments:
    infiles               Path list of data files or directories which have data
                            files.

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    --raise-exception     If it is specified, raise exceptions.
    -o OUTFILE, --outfile OUTFILE
                            An output filename without extensions. The required
                            filename extension will be automatically determined
                            from an output format.

    Reading options:
    -p PARSER, --parser PARSER
                            A maidenhair parser name which will be used to parse
                            the raw text data.
    -l LOADER, --loader LOADER
                            A maidenhair loader name which will be used to load
                            the raw text data.
    -u USING, --using USING
                            A colon (:) separated column indexes. It is used for
                            limiting the reading columns.

    Unite options:
    --unite               Join the columns of classified dataset with respecting
                            --unite-basecolumn.The dataset is classified with
                            --unite-function.
    --unite-basecolumn UNITE_BASECOLUMN
                            An index of columns which will be used as a base
                            column for regulating data point region.
    --unite-function UNITE_FUNCTION
                            A python script file path or a content of python
                            lambda expression which will be used for classifing
                            dataset. If it is not spcified, a filename character
                            before period (.) will be used to classify.

    Classify options:
    --classify            Classify dataset with --classify-function. It will
                            influence the results of --relative and --baseline.
    --classify-function CLASSIFY_FUNCTION
                            A python script file path or a content of python
                            lambda expression which will be used for classifing
                            dataset. If it is not specified, a filename character
                            before the last underscore (_) will be used to
                            classify.

    Relative options:
    --relative            If it is True, the raw data will be converted to
                            relative data from the specified origin, based on the
                            specified column. See `--relative-origin` and
                            `--relative-basecolumn` also.
    --relative-origin RELATIVE_ORIGIN
                            A dataset number which will be used as an orign of the
                            relative data. It is used with `--relative` option.
    --relative-basecolumn RELATIVE_BASECOLUMN
                            A column number which will be used as a base column to
                            make the data relative. It is used with `--relative`
                            option.

    Baseline options:
    --baseline            If it is specified, the specified data file is used as
                            a baseline of the dataset. See `--baseline-basecolumn`
                            and `--baseline-function` also.
    --baseline-basecolumn BASELINE_BASECOLUMN
                            A column index which will be proceeded for baseline
                            regulation. It is used with `--baseline` option.
    --baseline-function BASELINE_FUNCTION
                            A python script file path or a content of python
                            lambda expression which will be used to determine the
                            baseline value from the data. `columns` and `column`
                            variables are available in the lambda expression.

    Peakset options:
    --peakset-method {argmax,argmin}
                            A method to find peak data point.
    --peakset-basecolumn PEAKSET_BASECOLUMN
                            A column index which will be used for finding peak
                            data point.
    --peakset-where-function PEAKSET_WHERE_FUNCTION
                            A python script file path or a content of python
                            lambda expression which will be used to limit the
                            range of data points for finding. peak data point.
                            `data` is available in the lambda expression.

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

I don't use Microsoft Windows so the location of the configure file in Windows
might be wrong.
Let me know if there are any mistakes.
