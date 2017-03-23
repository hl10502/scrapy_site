# #!/usr/bin/env python
# -*- encoding: utf-8 -*-

import scrapy

from scrapy_site.items import SiteItem
from scrapy_site.utils import date


# 广东省政府采购系统爬虫
class GdgpoGovSpider(scrapy.Spider):
    name = "gdgpogov"
    allowed_domains = ["gdgpo.gov.cn"]
    start_urls = [
        "http://www.gdgpo.gov.cn/queryMoreInfoList/channelCode/0005.html"
    ]

    def __init__(self, name=None, **kwargs):
        self.iipage = 1
        super(GdgpoGovSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        detail = response.xpath('//ul[@class="m_m_c_list"]/li')
        for temp in detail:
            item = SiteItem()
            item['title'] = temp.xpath('a/text()').extract_first().strip()
            item['link'] = "http://www.gdgpo.gov.cn" + temp.xpath('a/@href').extract_first().strip()
            item['pubtime'] = temp.xpath('em/text()').extract_first().strip()[0:10]
            print("------------------------------------------------------------------------------")
            yield item
        if date.get_curdate() == (item['pubtime']):
            pageindex = response.xpath('//input[@id="pointPageIndexId"]/@value').extract_first()
            self.iipage += 1
            last_page = response.xpath(
                u'//a/span[contains(text(),"尾  页")]/../@href').extract_first()
            total_pagenum = last_page.split('(')[1][:-1]
            if int(self.iipage) < int(total_pagenum):
                yield scrapy.FormRequest("http://www.gdgpo.gov.cn/queryMoreInfoList.do",
                                         formdata={
                                             "sitewebId": "4028889705bebb510105bec068b00003",
                                             "channelCode": '0005',
                                             'pageIndex': str(self.iipage),
                                             'pageSize': "15",
                                             'pointPageIndexId': "1"
                                         }, callback=self.parse)
