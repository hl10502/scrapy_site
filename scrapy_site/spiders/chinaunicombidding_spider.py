# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-

import scrapy

from scrapy_site.items import SiteItem
from scrapy_site.utils import date


# 中国联通采购与招标网爬虫
class ChinaunicombiddingSpider(scrapy.Spider):
    name = "chinaunicombidding"
    allowed_domains = ["chinaunicombidding.cn"]
    start_urls = [
        "http://www.chinaunicombidding.cn/jsp/cnceb/web/forword.jsp"
    ]

    def parse(self, response):
        yield scrapy.FormRequest(
            "http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?page=1",
            formdata={
                "type": "",
                "province": "",
                "city": "",
                "notice": "",
                "time1": "",
                "time2": ""
            }, callback=self.parse_)

    def parse_(self, response):
        detail = response.xpath('//table[@bordercolor="lightgray"]/tr')
        # 最后一行为翻页
        for temp in detail[:-1]:
            item = SiteItem()
            item['title'] = temp.xpath('td/span/@title').extract_first().strip()
            if temp.xpath('td/span/@onclick').extract_first():
                item['link'] = 'http://www.chinaunicombidding.cn' + \
                               (temp.xpath('td/span/@onclick').extract_first()).split(',')[0].split(
                                   '(')[1][1:-1].strip()
            item['pubtime'] = temp.xpath('td[@width="15%"]/text()').extract_first().strip()
            yield item
        nowPage = str(int(response.xpath('//span[@id="nowPage"]/text()').extract_first()) + 1)
        print ('nowpage======================================' + str(nowPage))
        if item['pubtime'] == date.get_curdate():
            yield scrapy.FormRequest(
                "http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?page=" + nowPage,
                formdata={
                    "type": "",
                    "province": "",
                    "city": "",
                    "notice": "",
                    "time1": "",
                    "time2": ""
                }, callback=self.parse_)
