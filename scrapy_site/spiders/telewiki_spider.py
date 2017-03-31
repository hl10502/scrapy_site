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
        "http://www.telewiki.cn/viewLogin.action"
    ]

    def __init__(self, name=None, **kwargs):
        self.pno = 1
        self.rand = 0
        self.pno__ = 1
        self.rand__ = 0

        super(TelewikiSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        yield scrapy.Request("http://www.telewiki.cn/notice/notice!querySupplierNoticeList.action?random=0.2697122781100487&noticeSO.subject=&noticeSO.releasedate_start=&noticeSO.releasedate_end=&noticeSO.noticesource=0&noticeSO.noticetype=6&noticeSO.status2=1&noticeSO.isopen=1",
                                 callback=self.parse_1)
        yield scrapy.Request("http://www.telewiki.cn/notice/notice!queryPurchaseList.action?random=0.17062830067799784&queryListSO.queryProjectName=&queryListSO.queryRegionCompany=&queryListSO.queryOpMethod=&queryListSO.queryBegindate=&queryListSO.queryEnddate=&paging.currentIndex=1&queryListSO.step=&queryListSO.applyState=&queryListSO.purchaseType=&queryListSO.status=0",
                                callback=self.parse_2)
        yield scrapy.Request("http://www.telewiki.cn/notice/notice!querySupplierNoticeList.action?random=0.11960641437720354&noticeSO.subject=&noticeSO.releasedate_start=&noticeSO.releasedate_end=&noticeSO.noticesource=0&noticeSO.noticetype=99&noticeSO.status2=1&noticeSO.isopen=1",
                                callback=self.parse_3)

    def parse_1(self, response):
        nowtime = ""
        detail = response.xpath('//table[@class="default_ListHeight"]//table[@id="testtr"]//div')
        # print ('============================================={}'.format(detail))
        for temp in detail:
            item = SiteItem()
            temp_title = temp.xpath('table[@width="99%"]//tr[1]//td[@width="725"]//h4//text()').extract_first()
            if not temp_title:
                continue
            item['title'] = temp_title.strip()
            # print ('*****************************************=====%s' % item['title'])
            item['pubtime'] = temp.xpath('table[@width="99%"]//tr[2]//td//div[@ class="note_date"]//text()').extract_first().strip()[5:15]
            # print ('*****************************************=====%s' % item['pubtime'])
            noticeid = temp.xpath('table[@width="99%"]//tr[4]//td//input//@onclick').extract_first().split('(')[1].split(')')[0]
            # print ('--------------------------------------------------------------%s' % noticeid)
            item['link'] = "http://www.telewiki.cn/notice/notice!queryNoticeDetail.action?random="+str(random.uniform(0,1))+"&noticeSO.noticeid="+noticeid
            # print ('===============================================--------------------------------%s' % item['link'])

            nowtime = (item['pubtime']).strip()
            yield item
        #
        # self.pno = self.pno + 1
        # self.rand = random.uniform(0,1)

        # if date.get_curdate() == nowtime:
        #     yield scrapy.Request("http://www.telewiki.cn/supplier/notice/notice!queryPurchaseList.action?random="+str(self.rand)+"&queryListSO.qProjectName=&queryListSO.qRegionCompany=&queryListSO.qOpMethod=&queryListSO.qBegindate=&queryListSO.qEnddate=&paging.currentIndex="+str(self.pno)+"&queryListSO.step=&queryListSO.applyState=&queryListSO.purchaseType=&queryListSO.status=0",callback=self.parse_)

    def parse_2(self, response):
        nowtime = ""
        detail = response.xpath('//table[@class="default_ListHeight"]//tr//td[@valign="top"]//table[@id="testtr"]//tr')
        for temp in detail:
            item = SiteItem()
            item['title'] = temp.xpath('td//div//table[@width="99%"]//tr[@height="40"]//td[@align="left"]//span[@class="ptitle"]//a//text()').extract_first()
            if not item['title']:
                continue
            # print ('=============================================================%s' % item['title'])
            noticeid = temp.xpath('td//div//table[@width="99%"]//tr[@height="40"]//td[@align="left"]//span[@class="ptitle"]//a//@onclick').extract_first()[5:10]
            # print ('--------------------------------------------------------------%s' % noticeid)
            item['pubtime'] = temp.xpath('td//div//table[@width="99%"]//tr[@height="35"]//span[@class="pscontent"][1]//text()').extract_first().strip()[0:10]
            # print ('=============================================================%s' % item['pubtime'])
            item['link'] = "http://www.telewiki.cn/notice/notice!queryNoticeDetail.action?random="+str(random.uniform(0,1))+"&noticeSO.noticeid="+noticeid
            # print ('===============================================--------------------------------%s' % item['link'])
            nowtime = item['pubtime']
            yield item

        self.pno__ = self.pno__ + 1
        self.rand__ = random.uniform(0,1)
        if date.get_curdate() == nowtime:
            yield scrapy.Request("http://www.telewiki.cn/notice/notice!queryPurchaseList.action?random="+str(self.rand__)
                                 +"&queryListSO.queryProjectName=&queryListSO.queryRegionCompany=&queryListSO."
                                  "queryOpMethod=&queryListSO.queryBegindate=&queryListSO.queryEnddate=&paging.currentIndex="
                                 +str(self.pno__)+"&queryListSO.step=&queryListSO.applyState=&queryListSO.purchaseType=&queryListSO.status=0",
                                 callback=self.parse__)

    def parse_3(self, response):
        nowtime = ""
        detail = response.xpath('//table[@class="default_ListHeight"]//table[@id="testtr"]//div')
        # print ('============================================={}'.format(detail))
        for temp in detail:
            item = SiteItem()
            temp_title = temp.xpath('table[@width="99%"]//tr[1]//td[@width="725"]//h4//text()').extract_first()
            if not temp_title:
                continue
            item['title'] = temp_title.strip()
            # print ('*****************************************=====%s' % item['title'])
            item['pubtime'] = temp.xpath('table[@width="99%"]//tr[2]//td//div[@ class="note_date"]//text()').extract_first().strip()[5:15]
            # print ('*****************************************=====%s' % item['pubtime'])
            noticeid = temp.xpath('table[@width="99%"]//tr[4]//td//input//@onclick').extract_first().split('(')[1].split(')')[0]
            # print ('--------------------------------------------------------------%s' % noticeid)
            item['link'] = "http://www.telewiki.cn/notice/notice!queryNoticeDetail.action?random="+str(random.uniform(0,1))+"&noticeSO.noticeid="+noticeid
            # print ('===============================================--------------------------------%s' % item['link'])

            nowtime = (item['pubtime']).strip()
            yield item
        #
        # self.pno = self.pno + 1
        # self.rand = random.uniform(0,1)

        # if date.get_curdate() == nowtime:
        #     yield scrapy.Request("http://www.telewiki.cn/supplier/notice/notice!queryPurchaseList.action?random="+str(self.rand)+"&queryListSO.qProjectName=&queryListSO.qRegionCompany=&queryListSO.qOpMethod=&queryListSO.qBegindate=&queryListSO.qEnddate=&paging.currentIndex="+str(self.pno)+"&queryListSO.step=&queryListSO.applyState=&queryListSO.purchaseType=&queryListSO.status=0",callback=self.parse_)
