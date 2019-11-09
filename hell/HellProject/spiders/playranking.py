'''
@Description: 
@Version: 
@School: Tsinghua Univ
@Date: 2019-11-05 21:29:52
@LastEditors: Xie Yufeng
@LastEditTime: 2019-11-05 22:23:09
'''
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PlayrankingSpider(CrawlSpider):
    name = 'playranking'
    allowed_domains = ['www.ttmeiju.me']
    start_urls = ['http://www.ttmeiju.me/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination"]//a[@class="next"]'), callback='parse_item', follow=True),
    )

    # def parse_item(self, response):
    #     item = {}
    #     #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
    #     #item['name'] = response.xpath('//div[@id="name"]').get()
    #     #item['description'] = response.xpath('//div[@id="description"]').get()
    #     return item
    def parse_item(self, response):
        print(response.url)
