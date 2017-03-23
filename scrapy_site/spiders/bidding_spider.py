# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-

import scrapy
from scrapy_site.items import SiteItem
from scrapy_site.utils import date

# 南方电网招标网爬虫
class BiddingSpider(scrapy.Spider):
    name = "bidding"
    allowed_domains = ["bidding.csg.cn"]
    start_urls = [
        "http://www.bidding.csg.cn/zbcg/index.jhtml",
        "http://www.bidding.csg.cn/tzgg/index.jhtml",
        "http://www.bidding.csg.cn/zbgg/index.jhtml"
    ]

    def parse(self, response):
        detail = response.xpath('//ul/li/span[@class="Right Gray"]/..')
        for temp in detail:
            item = SiteItem()
            item['title'] = temp.xpath('a/text()').extract_first().strip()
            # link没有前缀，增加网站前缀url：http://www.bidding.csg.cn
            item['link'] = "http://www.bidding.csg.cn" + temp.xpath('a/@href').extract_first().strip()
            item['pubtime'] = temp.xpath('span[@class="Right Gray"]/text()').extract_first().strip()
            pubtime = item['pubtime']
            yield item
        if pubtime == date.get_curdate():
            # 得到下一页
            hrefs = response.xpath('//a')
            for next_page in hrefs:
                temp = next_page.xpath('text()').extract_first()
                if temp == u'下一页':
                    print '=============================南方电网翻页========================='
                    if next_page.xpath('@href').extract_first():
                        next_page_href = "http://www.bidding.csg.cn/zbcg/" + (
                            str(next_page.xpath('@href').extract_first()))
                        yield scrapy.FormRequest(next_page_href, callback=self.parse)

                    if next_page.xpath('@href').extract_first():
                        next_page_href = "http://www.bidding.csg.cn/tzgg/" + (
                            str(next_page.xpath('@href').extract_first()))
                        yield scrapy.FormRequest(next_page_href, callback=self.parse)

                    if next_page.xpath('@href').extract_first():
                        next_page_href = "http://www.bidding.csg.cn/zbgg/" + (
                            str(next_page.xpath('@href').extract_first()))
                        yield scrapy.FormRequest(next_page_href, callback=self.parse)
