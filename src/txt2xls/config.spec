[default]
raise_exception = boolean(default=False)

[reader]
parser = string(default='parsers.PlainParser')
loader = string(default='loaders.PlainLoader')
using = int_list(min=2, max=2, default=None)

    [[classify]]
    enabled = boolean(default=False)
    function = string(default='builtin:classify_function')

    [[unite]]
    enabled = boolean(default=False)
    function = string(default='builtin:unite_function')
    basecolumn = integer(default=0)

    [[relative]]
    enabled = boolean(default=False)
    origin = integer(min=0, default=0)
    basecolumn = integer(default=1)

    [[baseline]]
    enabled = boolean(default=False)
    function = string(default='builtin:baseline_function')
    basecolumn = integer(default=1)

[writer]
default_filename = string(default='output.xls')

    [[peakset]]
    method = string(default='argmax')
    basecolumn = integer(default=-1)
    where_function = string(default=None)
