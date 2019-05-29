# -*- coding: utf-8 -*-
import requests
import scrapy

from ..items import Ip89Item


class Ip89cnSpider(scrapy.Spider):
    name = 'ip89cn'
    allowed_domains = ['www.89ip.cn']
    start_urls = (
        'http://www.89ip.cn/'
    )

    def start_requests(self):
        res = []
        for i in range(1, 101):
            url = 'http://www.89ip.cn/index_%d.html' % i
            req = scrapy.Request(url)
            res.append(req)
        return res

    def parse(self, response):
        table = response.xpath('//table[@class="layui-table"]')[0]
        trs = table.xpath('//tr')[1:]
        items = []
        for tr in trs:
            pre_item = Ip89Item()
            pre_item['proxy'] = tr.xpath('td[1]/text()').extract()[0].strip()
            pre_item['port'] = tr.xpath('td[2]/text()').extract()[0].strip()
            pre_item['location'] = tr.xpath('string(td[3])').extract()[0].strip()
            pre_item['time'] = tr.xpath('td[5]/text()').extract()[0].strip()
            items.append(pre_item)
        return items



