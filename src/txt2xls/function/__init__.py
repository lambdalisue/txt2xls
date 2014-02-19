# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import re
import imp


def parse_function(function, default_type='lambda'):
    """
    Parse function expression which start from function type (e.g. 'lambda:')

    The function expression has to be start from 'lambda:', 'file:', 'regex:',
    or 'builtin:' (shortcut alias of 'file:' type for builtin functions).
    If no function type is specified, the function will be treated as
    :attr:`default_type`.

    Args:
        function (string): A function expression
        default_type (string): A default function expression type

    Returns:
        function: A function

    Raises:
        AttributeError: Raise when unknown function type has been specified.
    """
    if function is None:
        return None
    if ":" not in function:
        function = "%s:%s" % (default_type, function)
    name, body = function.split(":", 1)

    if name == 'regex':
        return create_regex_function(body)
    elif name == 'file':
        return create_file_function(body)
    elif name == 'lambda':
        return create_lambda_function(body)
    elif name == 'builtin':
        BUILTIN = os.path.join(os.path.dirname(__file__), 'builtin')
        body = os.path.join(BUILTIN, body + ".py")
        return create_file_function(body)
    else:
        raise AttributeError("Unknown function type '%s' "
                             "has specified" % name)


def create_regex_function(body):
    """
    Create function from regex pattern.
    
    It is used for creating a function for classification.

    Args:
        body (string): A regex pattern

    Returns:
        function: A function which will return string for classification
    """
    pattern = re.compile(body)
    def fn(data):
        filename = data[0]
        m = pattern.search(filename)
        if m and len(m.groups()) > 0:
            # use a first group if there are any groups
            return m.group(1)
        elif m:
            # use entire match
            return m.group()
        # no mathced text found
        return filename
    return fn


def create_file_function(body):
    """
    Create function from specified python script file.

    The python script file has to have ``__call__(data)__`` function.

    Args:
        body (string): A filename of the python script

    Returns:
        function: A function
    """
    filename = os.path.expanduser(body)
    if not os.path.exists(filename):
        raise IOError("%s is not found." % body)
    basename = os.path.splitext(os.path.basename(filename))[0]
    module = imp.load_source(basename, filename)
    if not hasattr(module, '__call__'):
        raise ImportError("%s does not have '__call__' function. "
                          "A script file must have '__call__(data)' "
                          "function." % filename)
    return module.__call__


def create_lambda_function(body):
    """
    Create lambda function with partial code.

    The partial code (:attr:`body`) will be put inside of lambda expression as::

        lambda *args, **kwargs: <BODY>

    Args:
        body (string): A body part of lambda expression

    Returns:
        function: A lambda function
    """
    fn = eval("lambda *args, **kwargs: %s" % body)
    return fn
