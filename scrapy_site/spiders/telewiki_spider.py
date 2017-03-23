# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-

import scrapy
import random

from scrapy_site.items import SiteItem
from scrapy_site.utils import date

#电信维基网爬虫
class TelewikiSpider(scrapy.Spider):
    name = "telewiki"
    allowed_domains = ["telewiki.cn"]
    start_urls = [
        "http://www.telewiki.cn/"
    ]

    def __init__(self, name=None, **kwargs):
        self.pno = 1
        self.rand = 0
        super(TelewikiSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        yield scrapy.Request("http://www.telewiki.cn/notice/notice!forwardToSearch.action?todo=1#",
                                 callback=self.parse_)
        yield scrapy.Request("http://www.telewiki.cn/notice/notice!forwardToSearch.action?todo=2#",
                                callback=self.parse__)
        yield scrapy.Request("http://www.telewiki.cn/notice/notice!forwardToSearch.action?todo=3#",
                                callback=self.parse___)

    def parse_(self, response):
        nowtime = ""
        detail = response.xpath('//tr/td/span[@class="ptitle"]/a')
        for temp in detail:
            item = SiteItem()
            item['pubtime'] = temp.xpath('../../../.././tr[3]//span[@class="pscontent"][1]/text()').extract_first()[0:10].strip()
            print ('*****************************************=====%s' % item['pubtime'])
            item['title'] = temp.xpath('text()').extract_first().strip()
            print ('*****************************************=====%s' % item['title'])
            noticeid = temp.xpath('@onclick').extract_first().split('(')[1].split(')')[0]
            print ('--------------------------------------------------------------%s' % noticeid)
            item['link'] = "http://www.telewiki.cn/supplier/notice/notice!queryNoticeDetail.action?random="+str(random.uniform(0,1))+"&noticeSO.noticeid="+noticeid
            print ('===============================================--------------------------------%s' % item['link'])

            nowtime = (item['pubtime']).strip()
            yield item

        self.pno = self.pno + 1
        self.rand = random.uniform(0,1)

        if date.get_curdate() == nowtime:
            yield scrapy.Request("http://www.telewiki.cn/supplier/notice/notice!queryPurchaseList.action?random="+str(self.rand)+"&queryListSO.qProjectName=&queryListSO.qRegionCompany=&queryListSO.qOpMethod=&queryListSO.qBegindate=&queryListSO.qEnddate=&paging.currentIndex="+str(self.pno)+"&queryListSO.step=&queryListSO.applyState=&queryListSO.purchaseType=&queryListSO.status=0",callback=self.parse_)

    def parse__(self, response):
        detail = response.xpath('//ul/li')
        for temp in detail:
            item = SiteItem()
            item['pubtime'] = temp.xpath('text()').extract_first().strip()
            print ('=============================================================%s' % item['pubtime'])
            item['title'] = temp.xpath('a[@class="a_xx"]/text()').extract_first().strip()
            print ('=============================================================%s' % item['title'])
            noticeid = temp.xpath('a/@onclick').extract_first().split("'")[1]
            print ('--------------------------------------------------------------%s' % noticeid)
            item['link'] = "http://www.telewiki.cn/supplier/notice/notice!queryNoticeDetail.action?random="+str(random.uniform(0,1))+"&noticeSO.noticeid="+noticeid
            print ('===============================================--------------------------------%s' % item['link'])
            yield item

    def parse___(self, response):
        detail = response.xpath('//ul/li')
        for temp in detail:
            item = SiteItem()
            item['pubtime'] = temp.xpath('text()').extract_first().strip()
            print ('======================================*******************%s' % item['pubtime'])
            item['title'] = temp.xpath('a[@class="a_xx"]/text()').extract_first().strip()
            print ('====================================*****************%s' % item['title'])
            noticeid = temp.xpath('a/@onclick').extract_first().split("'")[1]
            print ('--------------------------------------------------------------%s' % noticeid)
            item['link'] = "http://www.telewiki.cn/supplier/notice/notice!queryNoticeDetail.action?random="+str(random.uniform(0,1))+"&noticeSO.noticeid=65496"+noticeid
            print ('===============================================--------------------------------%s' % item['link'])
            yield item
