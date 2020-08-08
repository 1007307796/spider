# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import Spider
from ..items import DoubanItem


class DoubanspiderSpider(scrapy.Spider):
    name = 'doubanspider'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.62 Mobile Safari/537.36',

    }   # 携带头信息，模拟用户访问
    # allowed_domains = ['movie.douban.com']
    # start_urls = ['https://movie.douban.com/top250']
    # 将信息封装交给下面的函数处理

    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        # scrapy自带命令调试
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # 可以使用xpath进行调试，也可以用view(response)将爬虫源码和原网页相对比

        item = DoubanItem()
        movies = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movies:
            item['ranking'] = movie.xpath('.//div[@class="pic"]/em/text()').extract()[0]
            # xpath返回的是Selectorlist的一个对象，extract将他转化为普通的字典
            item['movie_name'] = movie.xpath('.//span[@class="title"][1]/text()').extract()[0]
            item['score'] = movie.xpath('.//span[@class="rating_num"]/text()').extract()[0]
            item['score_num'] = movie.xpath('.//div[@class="star"]/span[4]/text()').re(ur'(\d+)人评价')[0]
            # python正则表达式中需要在reg之前加u，匹配输出括号里的表达式
            yield item   # 每执行一次就存储一次
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        # 构造新的url
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url, headers=self.headers)   # 回调请求
