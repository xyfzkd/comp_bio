# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DailymeijuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TtmjPlayItem(scrapy.Item):
    play_name = scrapy.Field()
    play_update_time = scrapy.Field()
    play_update_time_day = scrapy.Field()
    play_season = scrapy.Field()
    update_time = scrapy.Field()


class TtmjVideoItem(scrapy.Item):
    video_title_ch = scrapy.Field()
    video_title_en = scrapy.Field()
    video_title_total = scrapy.Field()
    video_season = scrapy.Field()
    video_episode = scrapy.Field()
    video_season_episode = scrapy.Field()
    video_clarity = scrapy.Field()
    video_size = scrapy.Field()
    video_has_subscribe = scrapy.Field()
    video_publish_time = scrapy.Field()
    video_create_time = scrapy.Field()
    video_download_magnet = scrapy.Field()
    video_download_ed2k = scrapy.Field()
    video_download_baidu = scrapy.Field()
    video_download_bt = scrapy.Field()
