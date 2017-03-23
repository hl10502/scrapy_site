#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 常量定义
Desc : 
"""
from scrapy_site.utils import const

# 编码
const.ENCODE = 'UTF-8'
#检索关键字配置文件
const.KEYWORD_CONF = 'keyword.conf'
#email收件人配置文件
const.EMAIL_CONF = 'email.conf'

# 第三方 SMTP 服务
const.MAIL_HOST = "smtp.126.com"  # 设置服务器
const.SENDER = 'zhujt1990@126.com'
const.MAIL_USER = "zhujt1990"  # 用户名
const.MAIL_PASS = "zhujiantao"  # 口令


