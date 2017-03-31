# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-

import scrapy

from scrapy_site.items import SiteItem
from scrapy_site.utils import date

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

# 中央政府招标网爬虫
class ZycgGovSpider(scrapy.Spider):
    name = "zycggov"
    allowed_domains = ["zycg.gov.cn"]
    start_urls = [
        "http://www.zycg.gov.cn/article/llist?catalog=zqyjgg",
        "http://www.zycg.gov.cn/article/llist?catalog=StockAffiche",
        "http://www.zycg.gov.cn/article/llist?catalog=ZhongBiao",
        "http://www.zycg.gov.cn/home/jqkbxm?catalog=StockAffiche",
        "http://www.zycg.gov.cn/article/llist?catalog=bggg",
        "http://www.zycg.gov.cn/article/llist?catalog=fbgg",
        "http://www.zycg.gov.cn/article/wsjjxq_list",
        "http://www.zycg.gov.cn/article/wsjjcj_list",
        "http://www.zycg.gov.cn/article/llist?catalog=wsjjfbgg",
        "http://www.zycg.gov.cn/ra_project/fp_xqgg",
        "http://www.zycg.gov.cn/ra_project/fp_zbgg",
        "http://www.zycg.gov.cn/ra_project/fp_fbgg"
    ]

    def parse(self, response):
        detail = response.xpath('//ul[@class="lby-list"]//li')
        pubtime = None
        for temp in detail[:20]:
            item = SiteItem()
            temp_pubtime = temp.xpath('span/text()').extract_first().strip()[1:11]
            if temp_pubtime:
                item['pubtime'] = temp.xpath('span/text()').extract_first().strip()[1:11]
                pubtime = item['pubtime']
            item['title'] = temp.xpath('a//text()').extract_first()
            print "------------------------------{}----".format(item['title'])
            if temp.xpath('a/@href').extract_first():
                item['link'] = "http://www.zycg.gov.cn" + temp.xpath('a//@href').extract_first()
            yield item
        # 如果内容不是当天发布则停止翻页
        # print ('-----------------------开始-------------------------------')
        # print ('-------pubtime----------------{}-------------------------------'.format(pubtime))
        # print ('------date.get_curdate-----------------{}-------------------------------'.format(date.get_curdate()))
        if pubtime == date.get_curdate():
            # 得到下一页
            # print "-----------------翻页-----------------"
            next_page_href = "http://www.zycg.gov.cn" + (
                str(response.xpath('//a[@class="next_page"]//@href').extract_first()))
            yield scrapy.FormRequest(next_page_href, callback=self.parse)
