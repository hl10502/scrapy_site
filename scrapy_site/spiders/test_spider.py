# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# """
# Topic: 登录爬虫
# Desc : 模拟登录https://github.com后将自己的issue全部爬出来
# tips：使用chrome调试post表单的时候勾选Preserve log和Disable cache
# """
# import logging
# import re
# import sys
# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from scrapy.http import Request, FormRequest, HtmlResponse
#
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     handlers=[logging.StreamHandler(sys.stdout)])
#
#
# class GithubSpider(CrawlSpider):
#     name = "github"
#     allowed_domains = ["github.com"]
#     start_urls = [
#         'https://github.com/issues',
#     ]
#     rules = (
#         # 消息列表
#         Rule(LinkExtractor(allow=('/issues/\d+',),
#                            restrict_xpaths='//ul[starts-with(@class, "table-list")]/li/div[2]/a[2]'),
#              callback='parse_page'),
#         # 下一页, If callback is None follow defaults to True, otherwise it defaults to False
#         Rule(LinkExtractor(restrict_xpaths='//a[@class="next_page"]')),
#     )
#     post_headers = {
#         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#         "Accept-Encoding":"gzip, deflate, br",
#         "Accept-Language":"zh-CN,zh;q=0.8",
#         "Cache-Control":"max-age=0",
#         "Connection":"keep-alive",
#         "Content-Length":"168",
#         "Content-Type":"application/x-www-form-urlencoded",
#         "Cookie":"_octo=GH1.1.1229562122.1472626443; logged_in=no;_gh_sess=eyJfY3NyZl90b2tlbiI6IlNHQWxEWGo2TjlnbWtXWlVJZ3JZWHhIVGd6SXpkdWRCdmM5azVPNjhWUW89IiwibGFzdF93cml0ZSI6MTQ3NDUyMzI3OTg1MywiZmxhc2giOnsiZGlzY2FyZCI6W10sImZsYXNoZXMiOnsiYW5hbHl0aWNzX2xvY2F0aW9uX3F1ZXJ5X3N0cmlwIjoidHJ1ZSJ9fSwic2Vzc2lvbl9pZCI6IjBmYjQzYTQzYjg3NzZmYmVjOTliM2EzMzViN2ViYjk2IiwicmVmZXJyYWxfY29kZSI6Imh0dHA6Ly93d3cucHljb2RpbmcuY29tLzIwMTYvMDQvMTIvc2NyYXB5LTExLmh0bWwifQ%3D%3D--08a41f6b11fc6352b8857a9c8f75d81da784185b; _ga=GA1.2.996517265.1472626435; _gat=1; tz=Asia%2FShanghai",
#         "Host":"github.com",
#         "Origin":"https://github.com",
#         "Referer":"https://github.com/",
#         "Upgrade-Insecure-Requests":"1",
#         "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.21 Safari/537.36"
#     }
#
#     # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
#     def start_requests(self):
#         return [Request("https://github.com/login",
#                         meta={'cookiejar': 1}, callback=self.post_login)]
#
#     # FormRequeset
#     def post_login(self, response):
#         print ('================================================================================%s')
#         # 先去拿隐藏的表单参数authenticity_token
#         authenticity_token = response.xpath(
#             '//input[@name="authenticity_token"]/@value').extract_first()
#         logging.info('authenticity_token=' + authenticity_token)
#         # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
#         # 登陆成功后, 会调用after_login回调函数，如果url跟Request页面的一样就省略掉
#
#         return [FormRequest.from_response(response,
#                                           url='https://github.com/session',
#                                           meta={'cookiejar': response.meta['cookiejar']},
#                                           headers=self.post_headers,  # 注意此处的headers
#                                           formdata={
#                                               'utf8': '✓',
#                                               'login': 'zhujiantao',
#                                               'password': 'zhu7358755',
#                                               'authenticity_token': authenticity_token
#                                           },
#                                           callback=self.after_login,
#                                           dont_filter=True
#                                           )]
#
#     def after_login(self, response):
#         for url in self.start_urls:
#             # 因为我们上面定义了Rule，所以只需要简单的生成初始爬取Request即可
#             yield Request(url, meta={'cookiejar': response.meta['cookiejar']})
#
#     def parse_page(self, response):
#         """这个是使用LinkExtractor自动处理链接以及`下一页`"""
#         logging.info(u'--------------消息分割线-----------------')
#         logging.info(response.url)
#         issue_title = response.xpath(
#             '//span[@class="js-issue-title"]/text()').extract_first()
#         logging.info(u'issue_title：' + issue_title.encode('utf-8'))
#
#     def _requests_to_follow(self, response):
#         """重写加入cookiejar的更新"""
#         if not isinstance(response, HtmlResponse):
#             return
#         seen = set()
#         for n, rule in enumerate(self._rules):
#             links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]
#             if links and rule.process_links:
#                 links = rule.process_links(links)
#             for link in links:
#                 seen.add(link)
#                 r = Request(url=link.url, callback=self._response_downloaded)
#                 # 下面这句是我重写的
#                 r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])
#                 yield rule.process_request(r)