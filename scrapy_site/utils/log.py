#!/usr/bin/env python
# -*-coding:utf-8-*-

import logging
from logging import FileHandler

FORMAT = "%(asctime)s %(name)s [%(levelname)s] %(thread)d %(module)s %(funcName)s %(lineno)s: %(message)s"

def get_log(name, log_file):
    handler = FileHandler(filename=log_file)
    handler.setFormatter(logging.Formatter(FORMAT))
    handler.setLevel(logging.DEBUG)
    _log = logging.getLogger(name)
    _log.addHandler(handler)
    # _log.addFilter(FilterFunc(funcname))
    return _log

