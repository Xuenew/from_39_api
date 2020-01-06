#Author:xue yi yang
import requests
import re
import json
class get_news():

    def __init__(self,url=""):
        self.url=url
        self.headers = {
            "user-agent": "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        }


    def get_image(self):
        pass

    def get_image_span(self):
        pass

    def get_main_con(self):
        data = {}
        # art_des = []
        img_list = [] #图片列表
        img_span_des = [] #图片解释列表
        r = requests.get(url=self.url,headers=self.headers).text
        # x = re.match(r'"content":[[](.*)[]]',str(r))
        # print(json.dumps(r))
        result = re.findall('content\":[[](.*)[]],\"image_count', str(r))
        title_res = re.findall('title\":(.*),\"advertise', str(r))
        dic_list = result[0].split("},")
        # print("**********",len(xxx))
        # print("**********",type(json.loads(xxx[0]+"}",encoding='UTF-8')))
        # dic_list[-1] + "}"
        # print(type(dic_list))
        #最后一个是文本
        # print(dic_list[-1])
        final_art = json.loads(dic_list[-1], encoding='UTF-8')["desc"].split("\n")# list
        data["art_des"] = final_art
        #出错了好久 原来是分割的时候 去掉了｝符号 每一个都去掉了
        for lis_i in dic_list[:-1]:
            # print(lis_i)
            lis_i = json.loads(lis_i+"}" , encoding='UTF-8')
            # print(type(lis_i))
            if lis_i["type"] == "img_url":
 #               print("img")
                img_list.append(lis_i["img_url"])
                img_span_des.append(lis_i["desc"])
            elif lis_i["type"] == "cnt_article":
#                print("art")
                pass
        data["img_url_list"] = img_list
        data["img_url_list_desc"] = img_span_des
        data["title"] = json.loads(title_res[0],encoding="utf-8")
        # data["art_des"] = final_art
        # print(data)
        # final_art = json.loads(dic_list[3],encoding='UTF-8')["desc"].split("\n")
        # print(final_art[:3])
        # print(title_res[0])
        # print(json.loads(title_res[0],encoding="utf-8"))

        return  data
# if __name__ == '__main__':
#     url = "https://view.inews.qq.com/w/WXN2019011600232302"
# # border-width: 4rpx 4rpx 4rpx 4rpx;
#     p = get_news(url=url)
#     p.get_main_con()
