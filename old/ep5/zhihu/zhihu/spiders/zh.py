# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Spider,Request

from ..items import ZhihuItem


class ZhSpider(scrapy.Spider):
    name = 'zh'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 初始用户
    start_user = "excited-vczh"
    # 用户信息页的模板
    user_url = "https://www.zhihu.com/api/v4/members/{user}?include={include}"
    # 这里的花阔号是为了让format渲染相应的信息
    # 查询参数字典化
    user_query = "locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count," \
                 "following_count,cover_url,following_topic_count,following_question_count,following_favlists_count," \
                 "following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count," \
                 "columns_count,commercial_question_count,favorite_count,favorited_count,logs_count," \
                 "marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active," \
                 "is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name," \
                 "show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count," \
                 "vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description," \
                 "hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage," \
                 "badge[?(type=best_answerer)].topics "
    # 关注列表url，offset和limit为翻页的参数
    follows_url = "https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={" \
                  "limit} "
    # 查询的参数
    follows_query = "data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following" \
                    "%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics "
    # 粉丝列表url
    followers_url = "https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={" \
                    "limit} "
    # 查询参数
    followers_query = "data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed" \
                      "%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics "

    def start_requests(self):
        """
            url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count' \
            '%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(' \
            'type%3Dbest_answerer)%5D.topics&offset=0&limit=20 '
            yield Request(url, callback=self.parse)   # 在响应了请求后执行回调函数
            重写start_requests方法，分别请求以上三个列表的信息
        """
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
        # 用format函数自动生成不同用户对应三个列表信息
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
                      callback=self.parse_follows)
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20),
                      callback=self.parse_followers)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = ZhihuItem()   # 实例化item
        for field in item.fields:   # 访问items的fields字典
            if field in result.keys():   # 如果此字段存在于items模板里 keys()为获取所有获取到的值
                item[field] = result.get(field)   # 存入数据 get方法获取字段的值
        yield item
        # 回调函数给下一个用户信息页面
        yield Request(
            self.follows_url.format(user=result.get("url_token"), include=self.follows_query, offset=0, limit=20),
            callback=self.parse_follows)
        yield Request(
            self.followers_url.format(user=result.get("url_token"), include=self.followers_query, offset=0, limit=20),
            callback=self.parse_followers)

    def parse_follows(self, response):   # 解析用户关注列表
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get("url_token"), include=self.user_query), callback=self.parse_user)

        # 判断page里是否存在is_end参数（是否为最后一页）
        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            # 获取下一页的地址然后通过yield继续返回Request请求，继续请求自己再次获取下页中的信息
            yield Request(next_page, self.parse_follows)

    def parse_followers(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get("url_token"), include=self.user_query),
                              callback=self.parse_user)
        # 这里判断page是否存在并且判断page里的参数is_end判断是否为False，如果为False表示不是最后一页，否则则是最后一页
        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            # 获取下一页的地址然后通过yield继续返回Request请求，继续请求自己再次获取下页中的信息
            yield Request(next_page, self.parse_followers)