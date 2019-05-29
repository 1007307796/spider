# -*- coding: utf-8 -*-
import re
import json

from ..items import DoubanajaxItem
from scrapy import Request
from scrapy.spiders import Spider


class DoubanAJAXSpider(Spider):
    name = 'doubanajax'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.62 Mobile Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20'
        # 爬去ajax动态加载网页时，起始网址应为数据请求的json网址
        yield Request(url, headers=self.headers)

    def parse(self, response):
        datas = json.loads(response.body)   # 读取页面的json数据/load为读取文件,loads为读取字符串，返回的是一个list
        item = DoubanajaxItem()
        if datas:
            for data in datas:
                item['ranking'] = data['rank']
                item['movie_name'] = data['title']
                item['score'] = data['score']
                item['score_num'] = data['vote_count']
                yield item

            # 如果datas存在数据则对下一页进行采集
            page_num = re.search(r'start=(\d+)', response.url).group(1)   # group(1)返回匹配到的第一项
            page_num = 'start=' + str(int(page_num)+20)   # response.url为响应请求的url
            next_url = re.sub(r'start=\d+', page_num, response.url)   # sub()函数用于更新start的参数
            yield Request(next_url, headers=self.headers)