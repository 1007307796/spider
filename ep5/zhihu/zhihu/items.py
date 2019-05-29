# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    name = Field()
    account_status = Field()
    allow_message = Field()
    answer_count = Field()   # 回答数
    articles_count = Field()   # 文章数
    avatar_hue = Field()
    avatar_url = Field()
    avatar_url_template = Field()
    badge = Field()
    business = Field()
    employments = Field()   # 工作信息
    columns_count = Field()
    commercial_question_count = Field()
    cover_url = Field()
    description = Field()
    educations = Field()
    favorite_count = Field()
    favorited_count = Field()
    follower_count = Field()   # 关注他的人的数量
    following_columns_count = Field()
    following_favlists_count = Field()
    following_question_count = Field()
    following_topic_count = Field()
    gender = Field()   # 性别
    headline = Field()
    hosted_live_count = Field()
    is_active = Field()
    is_bind_sina = Field()
    is_blocked = Field()
    is_advertiser = Field()
    is_blocking = Field()
    is_followed = Field()
    is_following = Field()
    is_force_renamed = Field()
    is_privacy_protected = Field()
    locations = Field()
    is_org = Field()
    type = Field()
    url = Field()
    url_token = Field()
    user_type = Field()   # 账户类型
    logs_count = Field()
    marked_answers_count = Field()
    marked_answers_text = Field()
    message_thread_token = Field()
    mutual_followees_count = Field()
    participated_live_count = Field()
    pins_count = Field()
    question_count = Field()   # 提问数量
    show_sina_weibo = Field()
    thank_from_count = Field()
    thank_to_count = Field()
    thanked_count = Field()
    type = Field()
    vote_from_count = Field()
    vote_to_count = Field()
    voteup_count = Field()   # 被赞同的数量
