#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     qichezhijia_forum_detail
   Description :
   Author :       ltx
   date：          2019-08-22
-------------------------------------------------
"""
import pika
import time
import requests
from lxml import etree
from lxml.html import tostring
import re
from new_text import fetch, get_font_mapping, get_content
from new_text import RequestException, FontSaveException
import csv
from json.decoder import JSONDecodeError
from retrying import retry
import redis
import pymysql
from pymysql import escape_string


@retry(stop_max_attempt_number=5)
def get_mq():
    try:
        while True:
            method_frame, header_frame, body = chan.basic_get(queue='qczj_forum', no_ack=True)
            if not body:
                time.sleep(2)
                s_conn.close()
                break
            qczj_obj = QczjForum()
            qczj_obj.parse_detail(body.decode('utf-8'))
    except:
        pass
        # url = connect.spop('qczj_forum_url')
        # qczj = QczjForum()
        # qczj.parse_detail(url.decode('utf-8'))


@retry(stop_max_attempt_number=5)
def get_proxy():
    try:
        url = 'http://www.ipgou.net/api/index/getip?token=008078f3bbed4aa5932ab0665dcc645d&pid=21&num=1&pl=http&type=json&bl=rn&obl=&jsip=1&areatype=0&pro=&city=&pc=0&rp=0&yys=0'
        resp = requests.get(url)
        data = resp.json()
        ip = data['data'][0]['ip']
        port = data['data'][0]['port']
        proxies = {
            'http': 'http://{}:{}'.format(ip, port),
            'https': 'https://{}:{}'.format(ip, port)
        }
        return proxies
    except RequestException as e:
        pass


def save_csv_data(forum_name, plate_name, article_title, click_count, reply_count, floor, release_time,
                  floor_content_text, floor_content_html, release_user,
                  release_user_url, release_user_register_time, place, like_car_name, page_url):
    sql = """
                    INSERT INTO qichezhijia_forum (forum_name, plate_name, article_title, click_count, reply_count, floor, release_time,
                  floor_content_text, floor_content_html, release_user,
                  release_user_url, release_user_register_time, place, like_car_name, page_url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """
    cursor.execute(sql, [forum_name, plate_name, article_title, click_count, reply_count, floor, release_time,
                         floor_content_text, escape_string(floor_content_html.decode('utf-8')), release_user,
                         release_user_url, release_user_register_time, place, like_car_name, page_url])
    conn.commit()


class QczjForum(object):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'fvlid=15621533546579k9lbkTymq; sessionid=57585632-C405-4A2D-A767-8B715211E3BF%7C%7C2019-07-03+19%3A29%3A15.893%7C%7C0; autoid=ddecfc178fda6ec1d70534459038570d; sessionuid=57585632-C405-4A2D-A767-8B715211E3BF%7C%7C2019-07-03+19%3A29%3A15.893%7C%7C0; __utma=1.1381969456.1563184268.1563184268.1563184268.1; __utmz=1.1563184268.1.1.utmcsr=i.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/31505237; pcpopclub=863e06ca0df94136b24f4c3bd17b1861063f20b6; clubUserShow=104800438|0|110100|aqd53tpa7|0|0|0||2019-07-15 17:52:05|0; autouserid=104800438; cookieCityId=110100; __ah_uuid_ng=u_104800438; sessionuserid=104800438; sessionlogin=6baf4b3434be41868be2155da2e5f29f063f20b6; sessionip=121.69.39.30; area=110106; ahpau=1; sessionvid=16095BB2-27BE-440E-A752-1B9BD09B1F6D; ahpvno=17; pvidchain=6830286,6830286,3274715,6830286,6830286,3274715,6830286,3274715,3274715,3274715; ref=www.baidu.com%7C0%7C0%7C0%7C2019-08-21+17%3A01%3A11.511%7C2019-07-11+13%3A53%3A01.180; ahrlid=1566378067228coD0oJPbFR-1566378320181',
        'Host': 'club.autohome.com.cn',
        'Referer': 'https://club.autohome.com.cn/bbs/forum-c-5198-1.html#pvareaid=2108152',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36,'
    }

    def __init__(self):
        self.proxy = get_proxy()

    def parse_detail(self, url):
        try:
            self.get_detail_data(url)
        except (requests.exceptions.RequestException, FontSaveException):
            self.proxy = get_proxy()
            self.get_detail_data(url)

    def get_detail_data(self, url):
        global floor, release_time, floor_content_text, floor_content_html, release_user, release_user_url, release_user_register_time, place, like_car_name
        page_source = fetch(url=url,
                            header=self.headers,
                            proxy=self.proxy
                            )
        forum_name = '汽车之家论坛'
        fonts = get_font_mapping()
        html = etree.HTML(page_source)
        plate_name = html.xpath('//div[@id="consnav"]/span[2]/a/text()')[0]
        article_title = html.xpath('//div[@id="consnav"]/span[4]/text()')[0]
        article_id = url.split('/')[-1]
        article_id = re.sub('-.\.html', '', article_id)
        if not article_id.isdigit():
            article_id = re.findall('-(.*?)-', url)[-1]
        click_count, reply_count = self.get_click_reply_count(article_id)
        for item in html.xpath('//div[@class="clearfix contstxt outer-section"]'):
            floor = item.xpath('.//div//div/button/text()')[0]
            if floor == '沙发':
                floor = '1楼'
            elif floor == '板凳':
                floor = '2楼'
            elif floor == '地板':
                floor = '3楼'
            # print(floor)
            release_time = item.xpath('.//div/span[2]/text()')[0]
            # print(release_time)
            floor_content_text = get_content(page_source=tostring(item),
                                             fonts=fonts,
                                             xpath_rule='string(//div[@class="w740"])'
                                             )
            # print(floor_content_text)
            floor_content_html = tostring(item)
            release_user = item.xpath('.//li[@class="txtcenter fw"]/a[1]/text()')[0].strip()
            # print(release_user)
            release_user_url = 'https:' + item.xpath('.//li[@class="txtcenter fw"]/a[1]/@href')[0]
            # print(release_user_url)
            try:
                release_user_register_time = item.xpath('.//li[5]/text()')[0]
            except:
                release_user_register_time = ''
            release_user_register_time = re.findall('注册：(.*)', release_user_register_time)[0]
            # print(release_user_register_time)
            place = item.xpath('.//li[6]/a/text()')[0]
            # print(place)
            release_user_id = re.findall('https://i.autohome.com.cn/(.*?)/home.html', release_user_url)[0]
            like_car_name = self.get_like_car_name(release_user_id)
            # print(like_car_name)
            print('-' * 30)
            print(forum_name, plate_name, article_title, click_count, reply_count, floor,
                  release_time,
                  floor_content_text, floor_content_html, release_user,
                  release_user_url, release_user_register_time, place, like_car_name)
            save_csv_data(forum_name, plate_name, article_title, click_count, reply_count, floor,
                          release_time,
                          floor_content_text, floor_content_html, release_user,
                          release_user_url, release_user_register_time, place, like_car_name, url)
        next_url = html.xpath('//a[@class="afpage"]/@href')
        if next_url:
            next_url = 'https://club.autohome.com.cn' + next_url[0]
            self.parse_detail(next_url)
            # print(next_url)

    def get_click_reply_count(self, article_id):
        try:
            url = f'https://clubajax.autohome.com.cn/Detail/LoadX_Mini?topicId={article_id}'
            response = requests.get(url, headers=self.headers, proxies=self.proxy)
            obj = response.json()
            data = obj['topicClicks']
            click_count = data['Views']
            reply_count = data["Replys"]
        except requests.exceptions.RequestException:
            self.proxy = get_proxy()
            url = f'https://clubajax.autohome.com.cn/Detail/LoadX_Mini?topicId={article_id}'
            response = requests.get(url, headers=self.headers, proxies=self.proxy)
            obj = response.json()
            data = obj['topicClicks']
            click_count = data['Views']
            reply_count = data["Replys"]
        return click_count, reply_count

    @retry(stop_max_attempt_number=5)
    def get_like_car_name(self, user_id):
        try:
            url = f'https://club.autohome.com.cn/clubindex2019/seleccarlevelsv2byuserids/?userids={user_id}'
            response = requests.get(url, headers=self.headers, proxies=get_proxy(), timeout=5)
            print(response.text)
            obj = response.json()
            cars = []
            if obj.get('result'):
                datas = obj.get('result')[0]['list']
                for data in datas:
                    car_name = data['seriesName'] + ' ' + data["specName"]
                    cars.append(car_name)
                return ','.join(cars)
            else:
                return ''
        except (requests.exceptions.RequestException, JSONDecodeError):
            self.proxy = get_proxy()
            url = f'https://club.autohome.com.cn/clubindex2019/seleccarlevelsv2byuserids/?userids={user_id}'
            print(url)
            response = requests.get(url, headers=self.headers, proxies=get_proxy(), timeout=5)
            print(response.text)
            obj = response.json()
            cars = []
            if obj.get('result'):
                datas = obj.get('result')[0]['list']
                for data in datas:
                    car_name = data['seriesName'] + ' ' + data["specName"]
                    cars.append(car_name)
                return ','.join(cars)
            else:
                return ''


if __name__ == '__main__':
    username = 'guest'
    pwd = 'guest'
    user_pwd = pika.PlainCredentials(username, pwd)
    s_conn = pika.BlockingConnection(
        pika.ConnectionParameters(host='119.29.217.153', port=5672, credentials=user_pwd))
    chan = s_conn.channel()
    chan.queue_declare(queue='qczj_forum', auto_delete=False, durable=True)
    conn = pymysql.connect(host='39.108.15.78', port=3306, user='root', passwd='Xueyiyang', db='qing_yuan_db',
                           charset='utf8mb4')
    cursor = conn.cursor()
    obj = QczjForum()
    #obj.parse_detail('https://club.autohome.com.cn/bbs/thread/e66ba618f89de84d/82667801-1.html')
    get_mq()
