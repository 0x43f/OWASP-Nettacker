#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import texttable
from core.alert import messages
from core.alert import info
from core.alert import error
from core import compatible
from core._time import now
from core._die import __die_failure
import lockfile

flock = lockfile.FileLock('log.txt')


def build_graph(graph_flag, language, data, _HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION):
    info(messages(language, 88))
    try:
        start = getattr(
            __import__('lib.graph.{0}.engine'.format(graph_flag.rsplit('_graph')[0]),
                       fromlist=['start']),
            'start')
    except:
        __die_failure(messages(language, 98).format(graph_flag))

    info(messages(language, 89))
    return start(graph_flag, language, data, _HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION)


def _get_log_values(log_in_file):
    o = open(log_in_file)
    data = ''
    for value in o:
        if value[0] == '{':
            data += value + ','
    return data[:-1]


def sort_logs(log_in_file, language, graph_flag):
    _HOST = messages(language, 53)
    _USERNAME = messages(language, 54)
    _PASSWORD = messages(language, 55)
    _PORT = messages(language, 56)
    _TYPE = messages(language, 57)
    _DESCRIPTION = messages(language, 58)
    _TIME = messages(language, 115)
    if compatible.version() is 2:
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
    if (len(log_in_file) >= 5 and log_in_file[-5:] == '.html') or (
            len(log_in_file) >= 4 and log_in_file[-4:] == '.htm'):
        data = sorted(json.loads('[' + _get_log_values(log_in_file) + ']'), key=lambda x: sorted(x.keys()))
        # if user want a graph
        _graph = ''
        if graph_flag is not None:
            _graph = build_graph(graph_flag, language, data, 'HOST', 'USERNAME', 'PASSWORD', 'PORT', 'TYPE',
                                 'DESCRIPTION')
        from lib.html_log import _log_data
        _css = _log_data.css_1
        _table = _log_data.table_title.format(_graph, _css, _HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION,
                                              _TIME)

        for value in data:
            _table += _log_data.table_items.format(value['HOST'], value['USERNAME'], value['PASSWORD'],
                                                   value['PORT'], value['TYPE'], value['DESCRIPTION'], value['TIME'])
        _table += _log_data.table_end + '<p class="footer">' + messages(language, 93) \
            .format(compatible.__version__, compatible.__code_name__, now()) + '</p>'
        __log_into_file(log_in_file, 'w' if type(_table) == str else 'wb', _table)
    elif len(log_in_file) >= 5 and log_in_file[-5:] == '.json':
        data = json.dumps(sorted(json.loads('[' + _get_log_values(log_in_file) + ']')))
        __log_into_file(log_in_file, 'wb', data)
    else:
        data = sorted(json.loads('[' + _get_log_values(log_in_file) + ']'))
        _table = texttable.Texttable()
        _table.add_rows([[_HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION, _TIME]])
        for value in data:
            _table.add_rows([[_HOST, _USERNAME, _PASSWORD, _PORT, _TYPE, _DESCRIPTION, _TIME],
                             [value['HOST'], value['USERNAME'], value['PASSWORD'], value['PORT'], value['TYPE'],
                              value['DESCRIPTION'], value['TYPE']]])
        data = _table.draw().encode('utf8') + '\n\n' 
        + messages(language, 93).format(compatible.__version__, compatible.__code_name__,
                                                 now()).encode('utf8')
        __log_into_file(log_in_file, 'wb', data)
    return 0

def __log_into_file(filename, mode, data):
    flock.acquire()
    with open(filename, mode) as save:
        save.write(data + '\n')
    flock.release()