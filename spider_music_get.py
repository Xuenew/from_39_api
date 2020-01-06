# Author:xue yi yang
import requests
import json
# from lxml import etree
import lxml.html
class get_music_all_url():
    """
    首页 网页版 返回数据链接
    https://u.y.qq.com/cgi-bin/musicu.fcg?-=recom27554676684513946&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%7D%2C%22category%22%3A%7B%22method%22%3A%22get_hot_category%22%2C%22param%22%3A%7B%22qq%22%3A%22%22%7D%2C%22module%22%3A%22music.web_category_svr%22%7D%2C%22recomPlaylist%22%3A%7B%22method%22%3A%22get_hot_recommend%22%2C%22param%22%3A%7B%22async%22%3A1%2C%22cmd%22%3A2%7D%2C%22module%22%3A%22playlist.HotRecommendServer%22%7D%2C%22playlist%22%3A%7B%22method%22%3A%22get_playlist_by_category%22%2C%22param%22%3A%7B%22id%22%3A8%2C%22curPage%22%3A1%2C%22size%22%3A40%2C%22order%22%3A5%2C%22titleid%22%3A8%7D%2C%22module%22%3A%22playlist.PlayListPlazaServer%22%7D%2C%22new_song%22%3A%7B%22module%22%3A%22QQMusic.MusichallServer%22%2C%22method%22%3A%22GetNewSong%22%2C%22param%22%3A%7B%22type%22%3A0%7D%7D%2C%22new_album%22%3A%7B%22module%22%3A%22music.web_album_library%22%2C%22method%22%3A%22get_album_by_tags%22%2C%22param%22%3A%7B%22area%22%3A1%2C%22company%22%3A-1%2C%22genre%22%3A-1%2C%22type%22%3A-1%2C%22year%22%3A-1%2C%22sort%22%3A2%2C%22get_tags%22%3A1%2C%22sin%22%3A0%2C%22num%22%3A40%2C%22click_albumid%22%3A0%7D%7D%2C%22toplist%22%3A%7B%22module%22%3A%22music.web_toplist_svr%22%2C%22method%22%3A%22get_toplist_index%22%2C%22param%22%3A%7B%7D%7D%2C%22focus%22%3A%7B%22module%22%3A%22QQMusic.MusichallServer%22%2C%22method%22%3A%22GetFocus%22%2C%22param%22%3A%7B%7D%7D%7D
    并不清楚是否每天更改
    热点词汇 链接
    https://c.y.qq.com/splcloud/fcgi-bin/gethotkey.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0
    新碟首发 链接 albummid = 首页 网页版返回的数据
    https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg?albummid=002zt7Im2HVifc&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0
    上面这个链接获得 一个数据 里面有可以的 mid  通过类得到
    """
    def __init__(self,music_name="",music_list_id=0):
        self.music_name = music_name
        self.music_list_id=music_list_id
        if music_name !="":
            self.init_get_json()#获得 self.json_get 一个大大的字典
            # self.music_song_id=self.json_get["data"]["song"]["list"][self.music_list_id]["singer"][0]["mid"]
            self.music_song_id=self.json_get["data"]["song"]["list"][self.music_list_id]["mid"]#手机版的 song_id和歌词页一样
            self.music_mv_id=self.json_get["data"]["song"]["list"][self.music_list_id]["mv"]["vid"]
            self.music_lyrics_id=self.json_get["data"]["song"]["list"][self.music_list_id]["mid"]#歌词暂时先获取ID 在写函数

    # @classmethod
    def get_music_song(self,):
        cookies = {
        }
        header = {
            # "referer": "https://i.y.qq.com/v8/playsong.html?ADTAG=newyqq.song&songmid=003sYHuC3aBd4r"
            "user-agent": "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            # "upgrade-insecure-requests": "1",
            # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "accept-encoding": "gzip, deflate, br",
            # "accept-language": "zh-CN,zh;q=0.9",
        }
        data = {
            # "ADTAG": "newyqq.song",
            # "songmid": "003sYHuC3aBd4r"
        }
        song_id = self.json_get["data"]["song"]["list"][self.music_list_id]["mid"]#对应的 歌曲id
        url = "https://i.y.qq.com/v8/playsong.html?ADTAG=newyqq.song&songmid={}#webchat_redirect".format(song_id)
        # ssrequest = requests.session()
        # requests.utils.add_dict_to_cookiejar(ssrequest.cookies)
        # respones = ssrequest.get(url=url,headers=header,data=data).text
        respones = requests.get(url=url, headers=header, data=data).text
        etree = lxml.html.etree
        selector = etree.HTML(respones)
        xx = selector.xpath("//audio[@id='h5audio_media']/@src")
        # xx=selector.xpath("//body")
    #    print(xx)
        # with open("ceshi.html","w") as f:
        #     f.write(respones)
        name=self.json_get["data"]["song"]["list"][self.music_list_id]["title"]
        author=self.json_get["data"]["song"]["list"][self.music_list_id]["singer"][0]["name"]
        poster= selector.xpath("//img[@class='album_cover__img js_album_cover']/@src")
   #     print({"src":xx,"name":name,"author":author,"poster":poster   })
        return json.dumps({"src":xx,"name":name,"author":author,"poster":poster,"list":self.json_get["data"]["song"]["list"] })
    @staticmethod
    def get_music_src(song_id):
        header = {
            # "referer": "https://i.y.qq.com/v8/playsong.html?ADTAG=newyqq.song&songmid=003sYHuC3aBd4r"
            "user-agent": "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            # "upgrade-insecure-requests": "1",
            # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "accept-encoding": "gzip, deflate, br",
            # "accept-language": "zh-CN,zh;q=0.9",
        }
        url = "https://i.y.qq.com/v8/playsong.html?ADTAG=newyqq.song&songmid={}#webchat_redirect".format(song_id)
        respones = requests.get(url=url, headers=header, ).text
        etree = lxml.html.etree
        selector = etree.HTML(respones)
        xx = selector.xpath("//audio[@id='h5audio_media']/@src")
        pic = selector.xpath("//img[@class='album_cover__img js_album_cover']/@src")
        # / html / body / article / section[2] / div / img
    #    print(pic)
     #   print(xx)
        return json.dumps({"src":xx,"pic_url":pic})
    @classmethod
    def get_mudic_new_song_list(cls):
        """
        返回一个字典 图片路径 author 以及以后加上歌词 { img: , author: ,}
        :return:
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
            # "user-agent": "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"

            , "Referer": "https://y.qq.com/",
        }
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg?-=recom719315609113707&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%7D%2C%22category%22%3A%7B%22method%22%3A%22get_hot_category%22%2C%22param%22%3A%7B%22qq%22%3A%22%22%7D%2C%22module%22%3A%22music.web_category_svr%22%7D%2C%22recomPlaylist%22%3A%7B%22method%22%3A%22get_hot_recommend%22%2C%22param%22%3A%7B%22async%22%3A1%2C%22cmd%22%3A2%7D%2C%22module%22%3A%22playlist.HotRecommendServer%22%7D%2C%22playlist%22%3A%7B%22method%22%3A%22get_playlist_by_category%22%2C%22param%22%3A%7B%22id%22%3A8%2C%22curPage%22%3A1%2C%22size%22%3A40%2C%22order%22%3A5%2C%22titleid%22%3A8%7D%2C%22module%22%3A%22playlist.PlayListPlazaServer%22%7D%2C%22new_song%22%3A%7B%22module%22%3A%22QQMusic.MusichallServer%22%2C%22method%22%3A%22GetNewSong%22%2C%22param%22%3A%7B%22type%22%3A0%7D%7D%2C%22new_album%22%3A%7B%22module%22%3A%22music.web_album_library%22%2C%22method%22%3A%22get_album_by_tags%22%2C%22param%22%3A%7B%22area%22%3A1%2C%22company%22%3A-1%2C%22genre%22%3A-1%2C%22type%22%3A-1%2C%22year%22%3A-1%2C%22sort%22%3A2%2C%22get_tags%22%3A1%2C%22sin%22%3A0%2C%22num%22%3A40%2C%22click_albumid%22%3A0%7D%7D%2C%22toplist%22%3A%7B%22module%22%3A%22music.web_toplist_svr%22%2C%22method%22%3A%22get_toplist_index%22%2C%22param%22%3A%7B%7D%7D%2C%22focus%22%3A%7B%22module%22%3A%22QQMusic.MusichallServer%22%2C%22method%22%3A%22GetFocus%22%2C%22param%22%3A%7B%7D%7D%7D"
        respones = requests.get(url=url, headers=headers).content
        # print(json.loads(respones)["new_song"]["data"]["song_list"][0]["mid"])#歌曲mid phone
        # print(json.loads(respones)["new_song"]["data"]["song_list"][0]["title"])#歌曲 name
        # print(json.loads(respones)["new_song"]["data"]["song_list"][0]["singer"])#歌曲 author []
        dict_new_song = json.loads(respones)["new_song"]["data"]["song_list"][:30]
        back_list = []
        # get_music_all_url.get_new_song_list_pic("ss")
        for i in dict_new_song:
            back_list.append({"pic_url":get_music_all_url.get_new_song_list_pic(i["mid"]),
                              "music_name":i["title"],"music_author":[j["name"] for j in i["singer"]   ]
                              ,"music_lyric":"","song_id":i["mid"]})
      #  print(back_list)
        return json.dumps(back_list)
    @classmethod
    def get_new_song_list_pic(cls,mid):
        header = {
            "user-agent": "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        }
        url = "https://i.y.qq.com/v8/playsong.html?ADTAG=newyqq.song&songmid={}#webchat_redirect".format(mid)
        respones = requests.get(url=url, headers=header, ).text
        etree = lxml.html.etree
        selector = etree.HTML(respones)
        pic = selector.xpath("//img[@class='album_cover__img js_album_cover']/@src")
        # print(pic)
        img_url = "http:"+ pic[0]
        return img_url
    def init_get_json(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
            # "user-agent": "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"

            , "Referer": "https://y.qq.com/",
        }
        url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=yqq.yqq.yqq&searchid=24984885683536913&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w={}&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(self.music_name)
        respones = requests.get(url=url,headers=headers).content
        # print(json.loads(respones)["data"]["song"]["list"][0]["singer"][0]["mid"])#歌曲mid
        # print(json.loads(respones)["data"]["song"]["list"][0]["mv"]["vid"])#歌曲 mv mid
        # print(json.loads(respones)["data"]["song"]["list"][0]["singer"][0]["name"])#歌曲作者
        # print(json.loads(respones)["data"]["song"]["list"][0]["mid"])#歌曲歌词页mid
        # print(json.loads(respones)["data"]["song"]["list"][0]["title"])#歌曲名字
        self.json_get = json.loads(respones)
        return self.json_get
#返回的是 搜索的结果列表 0-19
    def get_search_list(self):#返回一个列表 用于列出view 小程序的view
        return json.dumps(self.json_get["data"]["song"]["list"])
#返回的是 一个列表包含hot image [0]["picUrl"] 0-4
    def get_hot_image(self):
        url = "https://c.y.qq.com/musichall/fcgi-bin/fcg_yqqhomepagerecommend.fcg?g_tk=5381&uin=0&format=json&inCharset=utf-8&outCharset=utf-8&notice=0&platform=h5&needNewCode=1&_=1546562309090"
        headers = {
            # "referer": "https://i.y.qq.com/v8/playsong.html?ADTAG=newyqq.song&songmid=003sYHuC3aBd4r"
            "user-agent": "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            # "upgrade-insecure-requests": "1",
            # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "accept-encoding": "gzip, deflate, br",
            # "accept-language": "zh-CN,zh;q=0.9",
        }
        response = requests.get(headers=headers,url=url).text
        # response = requests.get(headers=headers,url=url).content
        # etree = lxml.html.etree
        # selector = etree.HTML(response)
        # xx = selector.xpath("//body")
        # with open("test.html","wb") as f:
        #     f.write(response)
        # print(json.loads(response)["data"]["slider"][0]["picUrl"])
        return json.loads(response)["data"]["slider"] #返回一个字典 loads 是加载json字符变成字典
    @staticmethod
    def get_hot_key():
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
            # "user-agent": "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"

            , "Referer": "https://y.qq.com/",
        }
        url = "https://c.y.qq.com/splcloud/fcgi-bin/gethotkey.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0"
        respones = requests.get(url=url, headers=headers).content
        # print(json.loads(respones)["data"]["hotkey"])
        key_list = json.loads(respones)["data"]["hotkey"]
        key_word = []
        for i in key_list:
            key_word.append(i["k"])
        # print(key_word)
        return json.dumps(key_word[:7])
if __name__ == '__main__':
    p=get_music_all_url(music_name="遥远的她")
    # p.get_music_song()
    # p.get_hot_image()
    # p.get_music_src("004X9VIj0TZ62M")
    # p.get_mudic_new_song_list()
    # p.get_mudic_new_song_list()
    p.get_hot_key()
