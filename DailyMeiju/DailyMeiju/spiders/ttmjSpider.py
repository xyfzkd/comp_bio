# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
from scrapy import Request
from bs4 import BeautifulSoup
from ..items import TtmjVideoItem, TtmjPlayItem
from ..pipelines import DailymeijuPipeline


class TtmjspiderSpider(scrapy.Spider):
    name = 'ttmjSpider'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def start_requests(self):
        print("start_requests")
        print(DailymeijuPipeline.play_url_list)
        if DailymeijuPipeline.play_url_list is not None and len(DailymeijuPipeline.play_url_list) != 0:
            for item in DailymeijuPipeline.play_url_list:
                start_url = item['play_url']
                play_name = item["play_name"]
        # start_url = "http://www.ttmeiju.vip/meiju/Supergirl.html"
                yield Request(url=start_url, callback=self.parse_page, dont_filter=True, meta={"play_name": play_name})

    def parse_page(self, response):
        cur_time_string = datetime.datetime.now().strftime('%Y-%m-%d')
        content = response.body
        soup = BeautifulSoup(content, "html.parser")
        play_name = response.meta["play_name"]
        cur_season_h3_list = soup.find_all(name="h3", attrs={"class":"curseason"})
        if len(cur_season_h3_list) != 0:
            cur_season_text = re.findall("\d",cur_season_h3_list[0].text.strip())[0]
            print("seasoin: " + cur_season_text)

        seedlink_div_list = soup.find_all(name="div", attrs={"class": "seedlink"})
        play_state = dict()
        play_update_time = str()
        play_update_time_day = str()
        if len(seedlink_div_list) != 0:
            span_list = seedlink_div_list[0].find_all(name="span")
            for index, span_item in enumerate(span_list):
                if index <= 5:
                    split_list = span_item.text.split("：")
                    play_state[split_list[0]] = split_list[1]
                    if index == 3:
                        play_update_time = split_list[1]
        play_update_time_day = play_update_time[:10]

        play_info_last_status = DailymeijuPipeline.play_info_state
        if play_name not in play_info_last_status.keys():
            play_last_update_time = "2019-01-01"
        else:
            play_last_update_time = play_info_last_status[play_name]["update_time"]
        play_last_update_day = datetime.datetime.strptime(play_last_update_time, "%Y-%m-%d")

            # page_update_time = "null " if re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}" ,seedlink_div_list[0].text) == 0 else re.findall( "\d{4}-\d{2}-\d{2} \d{2}:\d{2}",seedlink_div_list[0].text)[0]
            # print("page_update_time: " + page_update_time)
            # print("---")
        tbody_list = soup.find_all(name="tbody", attrs={"id":"seedlist"})
        if len(tbody_list) != 0:
            tr_list = tbody_list[0].find_all(name="tr")
            for item in tr_list:
                td_list = item.find_all(name="td")
                item_time = td_list[-1].text.strip()
                item_time_cur = datetime.datetime.strptime(item_time, "%Y-%m-%d")
                diff_day = (item_time_cur - play_last_update_day).days
                if diff_day >= 0 or play_last_update_day is "":
                    item_name = td_list[1].text.strip()
                    name_list = item_name.split(" ")
                    title_ch = name_list[0]
                    s_and_e_list = re.findall("S\d{2}E\d{2}", item_name)
                    video_clarity = re.findall("\d{3,4}p", item_name)
                    video_season_episode = s_and_e_list[0]
                    video_season = video_season_episode[1:3]
                    video_episode = video_season_episode[4:6]

                    item_download_td = td_list[2]
                    item_download_url = item_download_td.find_all(name="a")
                    item_download_ed2k = str()
                    item_download_magnet = str()
                    item_download_bt = str()
                    item_download_baidu = str()
                    for download_item in item_download_url:
                        if "magnet:" in download_item['href']:
                            item_download_magnet = download_item['href']
                        if "ed2k:" in download_item['href']:
                            item_download_ed2k = download_item['href']
                        if ".torrent" in download_item['href']:
                            item_download_bt = download_item['href']
                        if "pan.baidu" in download_item['href']:
                            item_download_baidu = download_item['href']

                    item_size = td_list[-4].text.strip()
                    item_subscribe = td_list[-3].text.strip()

                    videoItem = TtmjVideoItem()
                    videoItem["video_title_ch"] = title_ch
                    videoItem["video_title_total"] = item_name
                    videoItem["video_season"] = video_season
                    videoItem["video_episode"] = video_episode
                    videoItem["video_season_episode"] = video_season_episode
                    videoItem["video_clarity"] = video_clarity
                    videoItem["video_size"] = item_size
                    videoItem["video_has_subscribe"] = item_subscribe
                    videoItem["video_publish_time"] = item_time
                    videoItem["video_create_time"] = cur_time_string
                    videoItem["video_download_magnet"] = item_download_magnet
                    videoItem["video_download_ed2k"] = item_download_ed2k
                    videoItem["video_download_baidu"] = item_download_baidu
                    videoItem["video_download_bt"] = item_download_bt
                    videoItem["video_title_en"] = play_name

                    yield videoItem

                    # print("%s \n%s , %s , %s\nMAG : %s\ned2k: %s\nbaid: %s\ntor : %s" % (item_name, item_size, item_subscribe, item_time, item_download_magnet, item_download_ed2k, item_download_bt, item_download_baidu))

        playInfoItem = TtmjPlayItem()
        playInfoItem['play_name'] = play_name
        playInfoItem['play_update_time'] = play_update_time
        playInfoItem['play_update_time_day'] = play_update_time_day
        playInfoItem['update_time'] = cur_time_string
        playInfoItem['play_season'] = cur_season_text
        yield playInfoItem


