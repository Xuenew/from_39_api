import requests,json,time,random,re,datetime
def get_ip_proxy():
    # ip代理接口
    ip_str = requests.post(
        url='http://api.qingapi.cn/get_ip/get_ip',
        data={
            "appkey": "bcf790a19e158355519659c0f83c2c6c"})
    ip_str = json.loads(ip_str.text).get('data')
    ip_list = ip_str.split('|')
    #return ip_list
    ips = ip_list
    for ip in ips:
        proxies ={
            'http': 'http://ip_proxy:ip_proxy@'+ip,
            'https': 'https://ip_proxy:ip_proxy@'+ip
        }
        url = 'http://api.ipify.org?format=json'
        try:
            res = requests.get(url, proxies=proxies, timeout=5)
            #print(res.text)
            return proxies
        except:
            #print('失败IP', ip)
            pass
        return get_ip_proxy()
# 存进队列
def save_mq(url):
    chan_web_tj_id_fail.basic_publish(exchange='', routing_key='web_tj_id_fail', body=url)
    return "ok"
def get_mq():
    while True:
        method_frame, header_frame, body = chan_web_tj_id.basic_get(queue='web_tj_id',no_ack=True)#
        if not body:
            time.sleep(2)
            s_conn.close()
            break
        else:
            #print(body)
            return str(body)
    return 0
class get_tu_jia():
    # 注意不能返回接口
    def __init__(self):
        self.seed_url = 'https://www.tujia.com'
        self.task_uid = 270346
        self.clue_uid = 1183
        self.company_id = 300
		
        self.task_uid2 = 270300
        self.clue_uid2 = 1183
        self.company_id2 = 300
		
        self.task_uid3 = 270300
        self.clue_uid3 = 327800
        self.company_id3 = 300
        self.clue_name = '途家-全球公寓民宿预订平台'
    def get_url_start(self):
        url = "https://www.tujia.com/bingo/pc/unit/v2/getunit?_apitsp=1565075191689"
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://www.tujia.com',
            'Referer': 'https://www.tujia.com/detail/459963.htm?code=MobileClientShare&mref=share&id=459963&uid=459963&tjmcode=6&srcLocalSite=goSite&tujia_code=MobileClientShare&refurl=&istjsite=true',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
        for num in range(459728,9963,-1):
        # num = 959963  #459963
            num = get_mq()
            data = '{"unitId": "%s", "preview": false, "unitGuId": null}'%num
            res = requests.post(url=url,headers=headers,data=data,proxies=get_ip_proxy())
            print(res.text)
            if json.loads(res.text)["errcode"]==0:
                self.get_detail(res=res.text)
            elif json.loads(res.text)["errmsg"]=="房屋已下线":
                # print("房屋已下线")
                pass
            else:
                save_mq(url=str(num))
    def get_detail(self,res):
        response = json.loads(res)
        for each in response["data"]["unit"]["picUrlList"]:
            #有三个不同的任务是同一个app
            #其三
            try:
                src = each["url"]
                data = {
                    "pid": str(time.time()).split('.')[0] + str(random.randint(10000, 99999)),
                    "task_id": self.task_uid3,
                    "clue_id": self.clue_uid3,
                    "clue_name": self.clue_name,
                    "company_id": self.company_id3,
                    "url": "https://pwa.tujia.com/h5/appw/discoverychannel/articledetails?articleid=" + str(
                        response["data"]["unit"]["unitId"]),
                    "pic_url": src,
                    "client_date": "",
                    "url_article_title": response["data"]["unit"]["unitName"],
                    "url_article": "",
                    "is_cover": 0,
                }
                aa = {'resource': data}
                # print(aa)
                # 转换为json数据类型进行打包
                d = json.dumps(aa)
                url = 'http://shijue.qingapi.cn/task_python/start'
                r = requests.post(url, data={"data": d})
                print(r.text)
                # self.send_message(self.project_name, data, src)
            except:
                pass
            #其二
            try:
                src = each["url"]
                data = {
                    "pid": str(time.time()).split('.')[0] + str(random.randint(10000, 99999)),
                    "task_id": self.task_uid2,
                    "clue_id": self.clue_uid2,
                    "clue_name": self.clue_name,
                    "company_id": self.company_id2,
                    "url": "https://pwa.tujia.com/h5/appw/discoverychannel/articledetails?articleid=" + str(
                        response["data"]["unit"]["unitId"]),
                    "pic_url": src,
                    "client_date": "",
                    "url_article_title": response["data"]["unit"]["unitName"],
                    "url_article": "",
                    "is_cover": 0,
                }
                aa = {'resource': data}
                # print(aa)
                # 转换为json数据类型进行打包
                d = json.dumps(aa)
                url = 'http://shijue.qingapi.cn/task_python/start'
                r = requests.post(url, data={"data": d})
                print(r.text)
                # self.send_message(self.project_name, data, src)
            except:
                pass
            #其一
            try:
                src = each["url"]
                data = {
                    "pid": str(time.time()).split('.')[0] + str(random.randint(10000, 99999)),
                    "task_id": self.task_uid,
                    "clue_id": self.clue_uid,
                    "clue_name": self.clue_name,
                    "company_id": self.company_id,
                    "url": "https://pwa.tujia.com/h5/appw/discoverychannel/articledetails?articleid=" + str(
                        response["data"]["unit"]["unitId"]),
                    "pic_url": src,
                    "client_date": "",
                    "url_article_title": response["data"]["unit"]["unitName"],
                    "url_article": "",
                    "is_cover": 0,
                }
                aa = {'resource': data}
                # print(aa)
                # 转换为json数据类型进行打包
                d = json.dumps(aa)
                url = 'http://shijue.qingapi.cn/task_python/start'
                r = requests.post(url, data={"data": d})
                print(r.text)
                # self.send_message(self.project_name, data, src)
            except:
                pass
if __name__ == '__main__':
    import  pika, time
    # 配置 ip
    username = 'xyy'
    pwd = 'Xueyiyang'
    user_pwd = pika.PlainCredentials(username, pwd)
    s_conn = pika.BlockingConnection(
        pika.ConnectionParameters(host='188.131.239.119', port=5672, credentials=user_pwd))
    chan_web_tj_id = s_conn.channel()
    chan_web_tj_id_fail = s_conn.channel()
    chan_web_tj_id.queue_declare(queue='web_tj_id', auto_delete=False, durable=True)
    chan_web_tj_id_fail.queue_declare(queue='web_tj_id_fail', auto_delete=False, durable=True)
    p = get_tu_jia()
    p.get_url_start()
