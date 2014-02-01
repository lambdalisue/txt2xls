# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
import textwrap
from configobj import ConfigObj
from configobj import flatten_errors
from validate import Validator


def get_user_config_filename(appname):
    """
    Get user config filename.

    It will return operating system dependent config filename.

    Parameters
    ----------
    appname : string
        An application name used for filename

    Returns
    -------
    string
        A filename of user configuration.

    """
    import platform
    system = platform.system()
    if system == 'Windows':
        rootname = os.path.join(os.environ['APPDATA'], appname)
        filename = appname + ".cfg"
        prefix = ''
    elif system == 'Linux':
        XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME', None)
        rootname = XDG_CONFIG_HOME or os.path.join('~', '.config')
        rootname = os.path.expanduser(rootname)
        # check if XDG_CONFIG_HOME exists
        if not os.path.exists(rootname) and XDG_CONFIG_HOME is None:
            # XDG_CONFIG_HOME is not used
            rootname = os.path.expanduser('~')
            filename = appname + ".cfg"
            prefix = '.'
        else:
            rootname = os.path.join(rootname, appname)
            filename = appname + ".cfg"
            prefix = ''
    elif system == 'Darwin':
        rootname = os.path.expanduser('~')
        filename = appname + ".cfg"
        prefix = '.'
    else:
        # Unknown
        rootname = os.path.expanduser('~')
        filename = appname + ".cfg"
        prefix = ''
    return os.path.join(rootname, prefix + filename)


def parse_conf(appname, args=None):
    # load confspec
    confspec = ConfigObj(
            os.path.join(os.path.dirname(__file__), 'confspec.cfg'),
            list_values=False,
            _inspec=True)
    # load config
    config = ConfigObj(
            get_user_config_filename(appname),
            configspec=confspec)

    # validation
    validator = Validator()
    results = config.validate(validator)
    if results != True:
        for (section_list, key, _) in flatten_errors(config, results):
            if key is not None:
                print
                print "Validation Error"
                msg = ("The '%s' key in the section '%s' failed validation. "
                       "Please make sure the format of the value is correct.")
                msg = msg % (key, ', '.join(section_list))
                msg = "\n| ".join(textwrap.wrap(msg))
                print "|", msg
                print
            else:
                print
                print "Validation Error"
                msg = ("The follwoing section was missing: %s")
                msg = msg % (', '.join(section_list))
                msg = "\n| ".join(textwrap.wrap(msg))
                print "|", msg
                print

    if args:
        for section in config:
            for key in config[section]:
                value = getattr(args, key, None)
                if value is not None:
                    config[section][key] = value
    return config
