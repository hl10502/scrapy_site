#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 时间、日期
Desc : 
"""

import time
def get_curdate():
    curdate = (time.strftime('%Y-%m-%d', time.localtime(time.time())))
    return curdate


