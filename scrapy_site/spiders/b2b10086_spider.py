# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-

import scrapy

from scrapy_site.items import SiteItem
from scrapy_site.utils import date as dateutil

# 移动采集网爬虫
class B2b10086Spider(scrapy.Spider):
    name = "b2b10086"
    allowed_domains = ["b2b.10086.cn"]
    start_urls = [
        "http://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2"
    ]

    def parse(self, response):
        yield scrapy.FormRequest(
            "http://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2",
            formdata={
                "page.currentPage": "1",
                "page.perPageSize": "20",
                "noticeBean.sourceCH": "",
                "noticeBean.source": "",
                "noticeBean.title": "",
                "noticeBean.startDate": "",
                "noticeBean.endDate": ""
            },
            callback=self.parse_)

    def parse_(self, response):
        detail = response.xpath('//table[@width="100%"]/tr')
        nowtime = ''
        for temp in detail[2:]:
            # print('----------------------------------------------------------------------------------------')
            item = SiteItem()
            item['pubtime'] = temp.xpath('td[@style="width:100px"]/text()').extract_first().strip()
            nowtime = (item['pubtime']).strip()
            if len(nowtime) == 9:
                date = nowtime.split('-')
                # 如果月份为一位
                if len(date[1]) == 1:
                    item['pubtime'] = '%s%s%s' % (nowtime[:5], '0', nowtime[5:])
                else:
                    item['pubtime'] = '%s%s%s' % (nowtime[:8], '0', nowtime[8:])
            nowtime = item['pubtime']
            item['title'] = temp.xpath('td[@style="width:280px;"]/a/text()').extract_first().strip()
            id = temp.xpath('@onclick').extract_first().split("'")[1]
            item['link'] = "http://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=" + id
            yield item

        if dateutil.get_curdate() == nowtime:
            nextPage = (response.xpath(
                u'//td//span[contains(text(),"下一页")]/../@onclick').extract_first()).split('(')[1][
                       :-2]
            print('============================---------------------%s' % (nextPage))
            yield scrapy.FormRequest(
                "http://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2",
                formdata={
                    "page.currentPage": nextPage,
                    "page.perPageSize": "20",
                    "noticeBean.sourceCH": "",
                    "noticeBean.source": "",
                    "noticeBean.title": "",
                    "noticeBean.startDate": "",
                    "noticeBean.endDate": ""
                },
                callback=self.parse_)
