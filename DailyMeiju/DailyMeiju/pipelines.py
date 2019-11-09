# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .emailUtil import EmailHelper
from .spiders import ttmjSpider
from .items import TtmjPlayItem, TtmjVideoItem

class DailymeijuPipeline(object):
    play_info_state = dict()
    play_url_list = list()
    need_to_send_list = list()

    # @staticmethod
    # def get_play_info_state():
    #     return play_info_state

    def open_spider(self, spider):
        print("open spider")
        if isinstance(spider, ttmjSpider.TtmjspiderSpider):
            print("success")
            self.client = pymongo.MongoClient("mongodb://xx.xx.xx.xx/", 27100)
            self.db = self.client["Meiju"]
            self.ttmj_play_url = self.db["TtmjPlayUrl"]
            self.ttmj_play_info = self.db["TtmjPlayInfo"]
            self.ttmy_video_collection = self.db["TtmjPlayItem"]
            play_state_result = self.ttmj_play_info.find()
            for item in play_state_result:
                self.play_info_state[item["play_name"]] = item
            print(self.play_info_state)
            play_url_result = self.ttmj_play_url.find()
            for item in play_url_result:
                # self.play_url_list["play_name"] = item["play_url"]
                self.play_url_list.append(item)
                print("open_spider----")
                print(item)


    def close_spider(self, spider):
        self.client.close()
        emailHelper = EmailHelper()
        if len(self.need_to_send_list) != 0:
            emailHelper.sendEmailWithAttr(self.need_to_send_list)

    def process_item(self, item, spider):
        if isinstance(item, TtmjPlayItem):
            find_result = self.ttmj_play_info.find_one({"play_name": item['play_name']})
            if find_result is not None:
                self.ttmj_play_info.remove({'play_name': item['play_name']})
            print("insert---  ttmj_play_info  -: ")
            self.ttmj_play_info.insert(dict(item))
        if isinstance(item, TtmjVideoItem):
            find_result = self.ttmy_video_collection.find_one({"video_title_total": item['video_title_total']})
            if find_result is not None:
                self.ttmy_video_collection.remove({'video_title_total': item['video_title_total']})
            print("insert---  ttmy_video_collection  -: ")
            self.ttmy_video_collection.insert(dict(item))
            self.need_to_send_list.append(item)
        return item
