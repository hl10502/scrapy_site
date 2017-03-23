# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-

import scrapy
import re

from scrapy_site.items import SiteItem
from scrapy_site.utils import date


# 电信供应商外部门户系统爬虫
class MssPortalSpider(scrapy.Spider):
    name = "mssportal"
    #allowed_domains = ["42.99.33.26/MSS-PORTAL/"]
    start_urls = [
        "https://42.99.33.26/MSS-PORTAL/announcementjoin/list.do?provinceJT=JT",
        #"https://42.99.33.26/MSS-PORTAL/announcementjoin/list.do?provinceJT=NJT"
    ]

    currentPage = 0

    def parse(self, response):
        pubtime = ""
        detail = response.xpath('//table[@class="table_data"]/tr')
        # provinceJT = ''
        # if '?' in response.url:
        #     provinceJT = (response.url).split('?')[1]
        # item = None
        for temp in detail[1:]:
            item = SiteItem()
            item['title'] = (temp.xpath('td[2]/a/text()')).extract_first().strip()
            onclick = str(temp.xpath('td[2]/a/@onclick').extract_first())
            item['pubtime'] = (temp.xpath('td[5]/text()')).extract_first()[0:10].strip()

            if 'view' in onclick:
                id = onclick.split(',')[0].split("'")[1]
                urlPart = onclick.split(',')[1].split("'")[1]
                print (
                    '========================================---------------------------------------%s' % urlPart)
                # if provinceJT == 'provinceJT=NJT':
                if 'TenderAnnouncement' == urlPart:
                    item[
                        'link'] = "https://42.99.33.26/MSS-PORTAL/tenderannouncement/viewHome.do?id=" + id
                elif 'Enquiry' == urlPart:
                    item['link'] = "https://42.99.33.26/MSS-PORTAL/enquiry/viewForAd.do?id=" + id
                elif 'PurchaseAnnounceBasic' == urlPart:
                    item[
                        'link'] = "https://42.99.33.26/MSS-PORTAL/purchaseannouncebasic/viewHome.do?id=" + id
                elif 'CompareSelect' == urlPart:
                    item[
                        'link'] = "https://42.99.33.26/MSS-PORTAL/tenderannouncement/viewCompare.do?id=" + id
                else:
                    item['link'] = "https://42.99.33.26/MSS-PORTAL/"
                print ('====%s' % item['link'])

            pubtime = (temp.xpath('td[5]/text()')).extract_first()[0:10]
            yield item

        if pubtime == date.get_curdate():
            # 得到包含总行数的字符串
            tt = response.xpath('//td[@width="10%"]/text()').extract()
            if len(tt) > 1:
                countPageStr = str(tt[1].encode('GB18030'))
                # 提取数字
                countPage = int(re.findall(r"\d+", countPageStr)[0]) / 10 + 1
                currentPageStr1 = response.xpath('//td[@width="10%"]/text()').extract_first()
                currentPage = int(re.findall(r"\d+", currentPageStr1)[0])
                pagingStart = str((int(currentPage)) * 10 + 1)
                toPage = int(currentPage) + 1
                toPageStr = str(toPage)
                if currentPage < countPage:
                    next_page = response.urljoin(
                            "https://42.99.33.26/MSS-PORTAL/announcementjoin/list.do?provinceJT=NJT")
                    yield scrapy.FormRequest(next_page,
                                             formdata={"provinceJT": "NJT", "docTitle": "",
                                                       "docCode": "",
                                                       "provinceCode": "", "startDate": "",
                                                       "endDate": "",
                                                       "docType": "", "paging.start": pagingStart,
                                                       "paging.pageSize": "10", "pageNum": "10",
                                                       "goPageNum": toPageStr,
                                                       "paging.start": pagingStart,
                                                       "paging.pageSize": "10",
                                                       "pageNum": "10", "goPageNum": toPageStr},
                                             callback=self.parse)
                    next_page = response.urljoin(
                            "https://42.99.33.26/MSS-PORTAL/announcementjoin/list.do?provinceJT=JT")
                    yield scrapy.FormRequest(next_page,
                                             formdata={"provinceJT": "NJT", "docTitle": "",
                                                       "docCode": "",
                                                       "provinceCode": "", "startDate": "",
                                                       "endDate": "",
                                                       "docType": "", "paging.start": pagingStart,
                                                       "paging.pageSize": "10", "pageNum": "10",
                                                       "goPageNum": toPageStr,
                                                       "paging.start": pagingStart,
                                                       "paging.pageSize": "10",
                                                       "pageNum": "10", "goPageNum": toPageStr},
                                             callback=self.parse)
