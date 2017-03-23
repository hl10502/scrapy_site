# #!/usr/bin/env python
# -*- encoding: utf-8 -*-

import scrapy
import json

from scrapy_site.items import SiteItem
from scrapy_site.utils import date


# 贵州省公共资源交易平台爬虫
class GzsggzyjyzxSpider(scrapy.Spider):
    name = "gzsggzyjyzx"
    allowed_domains = ["gzsggzyjyzx.cn"]
    start_urls = [
        "http://www.gzsggzyjyzx.cn/tra_info?cls=4B"
    ]

    def __init__(self, name=None, **kwargs):
        self.pno = 2
        self.rownum = 20
        super(GzsggzyjyzxSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        yield scrapy.FormRequest("http://www.gzsggzyjyzx.cn/ajax_trace",
                                 formdata={
                                     "cls": "4B",
                                     "type": "All",
                                     "classif_no": "All",
                                     "rownum": "20",
                                     "pno": "1"
                                 }, callback=self.parse_)

    def parse_(self, response):
        self.pno = self.pno + 1
        self.rownum = self.rownum + 10
        body = response.body  # json
        detail = json.loads(body)
        datalist = detail['dataList']
        page = detail["page"]
        pubtime = None
        for temp in datalist:
            item = SiteItem()
            item['title'] = temp['title'].strip()
            item['link'] = "http://www.gzsggzyjyzx.cn" + temp['page_url'].strip()
            item['pubtime'] = temp['date'].strip()
            pubtime = (str(item['pubtime'])).strip()
            yield item
        print ("----------%s" % page["count"])
        print ("----------%s" % page["rownum"])
        print ("----------%s" % page["no"])
        print ("----------%s" % str(int(page["count"]) / 20 + 1))
        countPage = int(page["count"]) / 20 + 1
        pageNow = int(page["no"])
        if int(pageNow) < int(countPage) and date.get_curdate() == pubtime:
            yield scrapy.FormRequest("http://www.gzsggzyjyzx.cn/ajax_trace",
                                     formdata={
                                         "cls": "4B",
                                         "type": "All",
                                         "classif_no": "All",
                                         "rownum": str(self.rownum),
                                         "pno": str(self.pno)
                                     }, callback=self.parse_)
