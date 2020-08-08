# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import Ip66Item


class Ip66cnSpider(scrapy.Spider):
    name = 'ip66cn'
    allowed_domains = ['www.66ip.cn']
    start_urls = ['http://www.66ip.cn/']

    # 通过首页地址得分页地址
    def parse(self, response):  # response为start_urls响应的内容
        links1 = response.xpath('//ul[@class="textlarge22"]')[0]
        links = links1.xpath('./li[not(@class)]//a/@href').extract()
        for link in links:
            yield Request(url='http://www.66ip.cn' + link, callback=self.get_details, dont_filter=True)

    # 进一步处理提取的数据中的url：处理分页信息
    def get_details(self, response):  # 此response为Request中url响应的内容
        results = response.xpath('//div[@class="containerbox boxindex"]//table//tr')  # 爬取分页地址对应的内容
        for tr in results:  # 对于列表需迭代爬取
            data = tr.xpath('./td/text()').extract()
            item = Ip66Item()
            item['proxy'] = data[0]
            item['port'] = data[1]
            item['location'] = data[2]
            item['time'] = data[4]
            yield item
