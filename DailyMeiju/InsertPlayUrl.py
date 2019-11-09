# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/2/18 11:32 PM'

import pymongo

def insert_data(data_list):
    client = pymongo.MongoClient("mongodb://xx.xx.xx.xx/", 27100)

    for item in data_list:
        insert_db(client, item)

    close_db(client)



def connect_to_db():
    print("*-*-*-*-*--- connect_to_db ---*-*-*-*-*")



def close_db(client):
    print("*-*-*-*-*--- close_db ---*-*-*-*-*")
    client.close()

def insert_db(client, data):
    print("*-*-*-*-*--- insert_db ---*-*-*-*-*")
    print(data)
    collection = client["Meiju"]["TtmjPlayUrl"]
    find_result = collection.find_one({"play_name": data['play_name']})
    if find_result is not None:
        collection.remove({'play_name': data['play_name']})
    collection.insert(data)


def create_data(play_url):
    result = dict()
    play_name = play_url.split("/")[-1][:-5]
    print(play_name)
    print(play_url)
    result["play_name"] = play_name
    result["play_url"] = play_url
    return result


if __name__ == '__main__':
    data_list = list()
    data_list.append(create_data("http://www.ttmeiju.vip/meiju/SEAL.Team.html"))
    data_list.append(create_data("http://www.ttmeiju.vip/meiju/The.Blacklist.html"))
    data_list.append(create_data("http://www.ttmeiju.vip/meiju/The.Flash.html"))
    data_list.append(create_data("http://www.ttmeiju.vip/meiju/The.Big.Bang.Theory.html"))
    data_list.append(create_data("http://www.ttmeiju.vip/meiju/Young.Sheldon.html"))
    data_list.append(create_data("http://www.ttmeiju.vip/meiju/House.of.Cards/6.html"))
    insert_data(data_list)