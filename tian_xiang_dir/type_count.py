#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     type_count
   Description :
   Author :       ltx
   date：          2019-07-24
-------------------------------------------------
"""
import requests
from collections import Counter
import json
import pika
import time

cat_names = []
scat_names = []
cat_ids = []


def save_mq(data):
    s_chan.basic_publish(exchange='', routing_key='book_ret', body=data)


def get_proxy():
    url = 'http://www.ipgou.net/api/index/getip?token=008078f3bbed4aa5932ab0665dcc645d&pid=137&num=1&pl=http&type=json&bl=rn&obl=&jsip=1&areatype=0&pro=&city=&pc=0&rp=0&yys=0'
    resp = requests.get(url)
    data = resp.json()
    ip = data['data'][0]['ip']
    port = data['data'][0]['port']
    proxies = {
        'http': '{}:{}'.format(ip, port),
        'https': '{}:{}'.format(ip, port)
    }
    return proxies


def get_mq():
    while True:
        method_frame, header_frame, body = chan.basic_get(queue='book', no_ack=True)
        if not body:
            time.sleep(2)
            s_conn.close()
            break
        c.get_response(body.decode('utf-8'))


class TypeCount(object):
    def __init__(self):
        self.proxy = get_proxy()

    def get_response(self, book_id):
        print(book_id)
        url = 'https://taodaxiang.com/category/index/get'
        headers = {
            'Origin': 'https://taodaxiang.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://taodaxiang.com/category',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data = 'ids%5B%5D=' + str(book_id)
        try:
            ret = {}
            response = requests.post(url, headers=headers, data=data, proxies=self.proxy).json()
            cat_id = response[0]['cat_id']
            cat_name = response[0]['cat_name']
            scat_name = response[0]['scat_name']
            ret['cat_id'] = cat_id
            ret['cat_name'] = cat_name
            ret['scat_name'] = scat_name
            s_ret = json.dumps(ret)
            save_mq(s_ret)
        except Exception as e:
            print('代理失效，更换IP', e)
            self.proxy = get_proxy()
            ret = {}
            response = requests.post(url, headers=headers, data=data, proxies=self.proxy).json()
            cat_id = response[0]['cat_id']
            cat_name = response[0]['cat_name']
            scat_name = response[0]['scat_name']
            ret['cat_id'] = cat_id
            ret['cat_name'] = cat_name
            ret['scat_name'] = scat_name
            s_ret = json.dumps(ret)
            save_mq(s_ret)


if __name__ == '__main__':
    username = 'guest'
    pwd = 'guest'
    user_pwd = pika.PlainCredentials(username, pwd)
    s_conn = pika.BlockingConnection(
        pika.ConnectionParameters(host='119.29.217.153', port=5672, credentials=user_pwd))
    chan = s_conn.channel()
    chan.queue_declare(queue='book', auto_delete=False, durable=True)
    s_chan = s_conn.channel()
    s_chan.queue_declare(queue='book_ret', auto_delete=False, durable=True)
    c = TypeCount()
    get_mq()
    # with open('delete.log', 'r') as f:
    #     book_ids = f.readlines()
    # for line in set(book_ids):
    #     book_id = line.split(':')[1].strip()
    #     save_mq(book_id)
    # c.get_response(book_id)
    # print(len(cat_ids), '---', len(cat_names), '---', len(scat_names))
    # cat_id_cnt = Counter(cat_ids)
    # cat_name_cnt = Counter(cat_names)
    # scat_name_cnt = Counter(scat_names)
    # print('cat_id_cnt: ')
    # print(cat_id_cnt)
    # print('cat_name_cnt: ')
    # print(cat_name_cnt)
    # print('scat_name_cnt: ')
    # print(scat_name_cnt)
