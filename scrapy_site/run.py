# -*- coding: utf-8 -*-
import scrapy
import os
import sys

sys.path.append('../scrapy_site')

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from scrapy_site.common.consts import const

import myemail

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)

# 运行所有的spider
for spider_name in runner.spider_loader.list():
    runner.crawl(spider_name)

d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()  # the script will block here until all crawling jobs are finished

# send mail
emails = []
# 获取当前目录，当前目录为scrapy_site项目的根目录
path = os.getcwd()
# 读取email.confi根据对应网站返回邮件内容字符串
fe = open(path + '/scrapy_site/' + const.EMAIL_CONF, 'r')
while True:
    line = fe.readline().strip()
    if line:
        config = line.split('===')
        temp = [config[1], config[2]]
        emails.append(temp)
    else:
        break
fe.close()
for email in emails:
    myemail.sendMail(email[0], email[1])
