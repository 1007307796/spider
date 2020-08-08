# -*- coding: utf-8 -*-
import scrapy
from ..items import XiciItem


class XiciSpider(scrapy.Spider):
    name = "xici"
    allowed_domains = ["xicidaili.com"]
    start_urls = (
        'http://www.xicidaili.com/',
    )

    def start_requests(self):
        res = []
        for i in range(1, 2):
            for s in ['nn', 'nt', 'wn', 'wt']:
                url = 'http://www.xicidaili.com/%s/%d' % (s, i)
                req = scrapy.Request(url)
                # 存储所有对应地址的请求
                res.append(req)
        return res

    def parse(self, response):
        table = response.xpath('//table[@id="ip_list"]')[0]
        trs = table.xpath('//tr')[1:]   # 去掉标题行
        items = []
        for tr in trs:
            pre_item = XiciItem()
            pre_item['proxy'] = tr.xpath('td[2]/text()').extract()[0]
            pre_item['port'] = tr.xpath('td[3]/text()').extract()[0]
            pre_item['type'] = tr.xpath('td[6]/text()').extract()[0]
            pre_item['location'] = tr.xpath('string(td[4])').extract()[0].strip()
            pre_item['time'] = tr.xpath('td[10]/text()').extract()[0]
            items.append(pre_item)
        return items
