# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-

import scrapy
import re

from scrapy_site.items import SiteItem
from scrapy_site.utils import date


# 中国采购与招标网爬虫
class ChinabiddingSpider(scrapy.Spider):
    name = "chinabidding"
    allowed_domains = ["chinabidding.cn"]
    start_urls = [
        "https://www.chinabidding.cn/zbxx/zbgg/",
        "https://www.chinabidding.cn/zbxx/bggg/",
        "https://www.chinabidding.cn/cgxx/zfcg/",
        "https://www.chinabidding.cn/cgxx/qycg/"
    ]

    def parse(self, response):
        pubtime = ""
        detail = response.xpath('//table[@id="list"]/tbody/tr[@class="yj_nei"]')
        for temp in detail:
            item = SiteItem()
            item['title'] = temp.xpath('td[@class="td_1"]/a/text()').extract_first().strip()
            item['link'] = "https://www.chinabidding.cn" + temp.xpath(
                    'td[@class="td_1"]/a/@href').extract_first().strip()
            item['pubtime'] = temp.xpath('td[@class="td_2"]/text()').extract()[1].strip()

            pubtime = item['pubtime']
            yield item
        if response.xpath(u'//span[@class="Disabled"]/a[text()="下一页>>"]/@href').extract_first():
            nextPagehref = "https://www.chinabidding.cn" + response.xpath(
                    u'//span[@class="Disabled"]/a[text()="下一页>>"]/@href').extract_first()
            # /zbxx/zbgg/249.html
            print ('------------------------------------------------------------%s' % nextPagehref)
        # nextPageNum = int(re.findall(r"\d+", nextPagehref)[0])
        # and nextPageNum < (int(self.pagenum['pagenum']) + 50)
        nextPageNum = int(re.findall(r"\d+", nextPagehref)[0])
        print('下一页===================================%s' % nextPageNum)
        if pubtime == date.get_curdate():
            if nextPagehref:
                yield scrapy.Request(nextPagehref, callback=self.parse)
