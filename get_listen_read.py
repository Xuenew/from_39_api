#Author:xue yi yang
import requests
import time
import hashlib
import base64
class get_info_listen():
    URL = "http://api.xfyun.cn/v1/service/v1/tts"
    AUE = "raw"
    APPID = "5c3eaa76"
    API_KEY = "7d523f299b1cac17073b78bf5cc42b95"
    def __init__(self,info):
        self.info = info

    def getHeader(self):
        curTime = str(int(time.time()))
        # ttp=ssml
        param = "{\"aue\":\"" + self.AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\",\"text_type\":\"text\"}"
   #     print("param:{}".format(param))

        paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
  #      print("x_param:{}".format(paramBase64))

        m2 = hashlib.md5()
        m2.update((self.API_KEY + curTime + paramBase64).encode('utf-8'))

        checkSum = m2.hexdigest()
 #       print('checkSum:{}'.format(checkSum))

        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.APPID,
            'X-CheckSum': checkSum,
            'X-Real-Ip': '39.108.15.78',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        # print(header)
        return header

    def get_listen(self):
        if len(self.info)<=324:
            r = requests.post(self.URL, headers=self.getHeader(), data={'text':self.info})
#            print(r.content)
            return r.content
        elif len(self.info)>324:
            infomation = self.info[:325]
            r = requests.post(self.URL, headers=self.getHeader(), data={'text':self.info})
#            print(r.content)
            return r.content
#if __name__ == '__main__':
 #    p = get_info_listen("你好 世界")
  #   p.get_listen()
