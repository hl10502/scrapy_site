# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-

import scrapy

from scrapy_site.items import SiteItem
from scrapy_site.utils import date


# 南航集团招标网爬虫
class CsbiddingSpider(scrapy.Spider):
    name = "csbidding"
    allowed_domains = ["csbidding.com.cn"]
    start_urls = [
        "http://www.csbidding.com.cn/nhzb/"
    ]

    def parse(self, response):
        for temp in response.xpath('//p[@class="all_title"]'):
            item = SiteItem()
            item['title'] = temp.xpath('span[@class="f_l"]/strong/text()').extract_first().strip()
            item['link'] = (temp.xpath('span[@class="f_r"]/a/@href').extract_first()).strip()
            url = response.urljoin(item['link'])
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        pubtime = None
        detail = response.xpath('//ul[@id="xx"]/li')
        for temp in detail:
            item = SiteItem()
            item['title'] = (temp.xpath('a/text()').extract_first()).strip()
            print ('-------------------------------------%s' % item['title'])
            item['link'] = "http://www.csbidding.com.cn" + (temp.xpath('a/@href').extract_first()).strip()
            item['pubtime'] = (temp.xpath('span/text()').extract_first()).strip()[0:10]
            pubtime = (item['pubtime'])
            print ('-------------------------------------%s' % pubtime)
            yield item
        # 得到当前页
        currentPage = int(response.xpath('//input[@name="currentPage"]/@value').extract_first())
        pageCount = int(response.xpath('//input[@name="pageCount"]/@value').extract_first())
        rowCount = int(response.xpath('//input[@name="rowCount"]/@value').extract_first())
        toPage = int(currentPage) + 1

        currentPageStr = str(currentPage)
        pageCountStr = str(pageCount)
        toPageStr = str(toPage)
        rowCountStr = str(rowCount)
        if pubtime and pubtime.strip() == date.get_curdate():
            yield scrapy.FormRequest(
                    "http://www.csbidding.com.cn/nhzb/infoListAction.do?show=bid&outs=outs",
                    formdata={"typeId": "0", "companyId": "0", "infoNameQuery": "",
                              "toPage": toPageStr,
                              "rowCount": rowCountStr, "currentPage": currentPageStr,
                              "pageCount": pageCountStr}, callback=self.parse_article)
            yield scrapy.FormRequest(
                    "http://www.csbidding.com.cn/nhzb/infoListAction.do?show=news&outs=outs",
                    formdata={"typeId": "0", "companyId": "0", "infoNameQuery": "",
                              "toPage": toPageStr,
                              "rowCount": rowCountStr, "currentPage": currentPageStr,
                              "pageCount": pageCountStr}, callback=self.parse_article)
            yield scrapy.FormRequest(
                    "http://www.csbidding.com.cn/nhzb/infoListAction.do?show=bidwin&outs=outs",
                    formdata={"typeId": "0", "companyId": "0", "infoNameQuery": "",
                              "toPage": toPageStr,
                              "rowCount": rowCountStr, "currentPage": currentPageStr,
                              "pageCount": pageCountStr}, callback=self.parse_article)
            yield scrapy.FormRequest(
                    "http://www.csbidding.com.cn/nhzb/infoListAction.do?show=newsres&outs=outs",
                    formdata={"typeId": "0", "companyId": "0", "infoNameQuery": "",
                              "toPage": toPageStr,
                              "rowCount": rowCountStr, "currentPage": currentPageStr,
                              "pageCount": pageCountStr}, callback=self.parse_article)
