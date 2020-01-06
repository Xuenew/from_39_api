import requests
import json,re
from multiprocessing import Queue,Process,Pool
import  pika, time
#************************
username = 'xyy'
pwd = 'Xueyiyang'
user_pwd = pika.PlainCredentials(username, pwd)
s_conn = pika.BlockingConnection(
    pika.ConnectionParameters(host='188.131.239.119', port=5672, credentials=user_pwd))
chan = s_conn.channel()
chan_fail = s_conn.channel()
chan_city_tuple = s_conn.channel()
chan.queue_declare(queue='web_tj_id', auto_delete=False, durable=True)
chan_city_tuple.queue_declare(queue='city_dict', auto_delete=False, durable=True)
chan_fail.queue_declare(queue='web_tj_fail_id_page', auto_delete=False, durable=True)#
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
#存进队列
def save_mq(url):
    chan.basic_publish(exchange='', routing_key='web_tj_id', body=url)
    return 0
def save_fail_mq(url):
    chan_fail.basic_publish(exchange='', routing_key='web_tj_fail_id_page', body=url)
    return 0
def save_city_tuple_mq(url):
    chan_city_tuple.basic_publish(exchange='', routing_key='city_dict', body=url)
    return 0
def get_mq():
    while True:
        method_frame, header_frame, body = chan_city_tuple.basic_get(queue='city_dict',auto_ack=True)#
        if not body:
            time.sleep(2)
            s_conn.close()
            return 0
        else:
            # s_conn.close()
            return body
def creat_city_dict_que(que_of_city_dict):
    with open("que_of_tu_jia.txt", "r",encoding="utf-8") as f:
        info = f.read().replace(r"'",'"')
        info = json.loads(info)
        # info = list(f.read())
        # info = type(f.read())
        # print(info)
        # print(info[:10])
        for each in info:
            save_city_tuple_mq(str(each))

# def get_que_info(): #从队列里面取东西
#     que = que_of_city_dict
#     if not que.empty():
#         return que.get()
#     else:
#         return 0

def get_url_post(index=1,data="",global_city_id=""):#请求url存id进入队列
    url = "https://www.tujia.com/bingo/pc/search/searchUnit"
    global_city_id = global_city_id
    if index==1:#正常开始
        que_info = get_mq()#自己队列里面取城市id 如果没有了返回的是0
        if que_info:
            city_id = eval(que_info)["city_id"]
            global_city_id = city_id
            data = "{\"conditions\":[{\"label\":\"\",\"specialLabel\":null,\"type\":42,\"value\":\"%s\",\"gType\":0,\"percentageUser\":null,\"pingYin\":null,\"hot\":null,\"labelDesc\":null,\"isSelected\":false,\"hotRecommend\":null,\"selected\":false},{\"label\":\"\",\"specialLabel\":null,\"type\":47,\"value\":\"2019-08-08,2019-08-09\",\"gType\":0,\"percentageUser\":null,\"pingYin\":null,\"hot\":null,\"labelDesc\":null,\"isSelected\":false,\"hotRecommend\":null,\"selected\":false}],\"pageIndex\":%s,\"pageSize\":30,\"returnAllConditions\":false,\"returnRedPacketInfo\":false,\"callCenter\":false}\r\n"%(city_id,index)
        else:
            print("city_dict 队列里面没有城市了，")
            return 0
    if index!=1:#如果到了下一页就是用原生的data
        data=data
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "ab0c2336-2ec0-4079-69ed-c05925f34ea9"
    }
    # print(data)
    res = requests.post( url, data=data, headers=headers)
    # print(res.text)
    if json.loads(res.text)["errcode"]==0 :
        if json.loads(res.text)["data"]["units"]:
            for each in json.loads(res.text)["data"]["units"]:#存入队列的步骤
                # print(each["unitId"])
                save_mq(url=str(each["unitId"]))
            index+=1
            city_id = global_city_id
            data = "{\"conditions\":[{\"label\":\"\",\"specialLabel\":null,\"type\":42,\"value\":\"%s\",\"gType\":0,\"percentageUser\":null,\"pingYin\":null,\"hot\":null,\"labelDesc\":null,\"isSelected\":false,\"hotRecommend\":null,\"selected\":false},{\"label\":\"\",\"specialLabel\":null,\"type\":47,\"value\":\"2019-08-08,2019-08-09\",\"gType\":0,\"percentageUser\":null,\"pingYin\":null,\"hot\":null,\"labelDesc\":null,\"isSelected\":false,\"hotRecommend\":null,\"selected\":false}],\"pageIndex\":%s,\"pageSize\":30,\"returnAllConditions\":false,\"returnRedPacketInfo\":false,\"callCenter\":false}\r\n"%(city_id,index)
            print("下一页",data)
            return get_url_post(index=index,data=data,global_city_id=global_city_id)
        else:
            print("已经空了 退出")
            print(data)
            return 0
    else:#
        save_fail_mq(url=str('{}-{}'.format(global_city_id,index)))
        #存入失败的city_id 和 page save_mq_fail
        index += 1
        city_id = global_city_id
        data = "{\"conditions\":[{\"label\":\"\",\"specialLabel\":null,\"type\":42,\"value\":\"%s\",\"gType\":0,\"percentageUser\":null,\"pingYin\":null,\"hot\":null,\"labelDesc\":null,\"isSelected\":false,\"hotRecommend\":null,\"selected\":false},{\"label\":\"\",\"specialLabel\":null,\"type\":47,\"value\":\"2019-08-08,2019-08-09\",\"gType\":0,\"percentageUser\":null,\"pingYin\":null,\"hot\":null,\"labelDesc\":null,\"isSelected\":false,\"hotRecommend\":null,\"selected\":false}],\"pageIndex\":%s,\"pageSize\":30,\"returnAllConditions\":false,\"returnRedPacketInfo\":false,\"callCenter\":false}\r\n" % (
        city_id, index)
        print(json.loads(res.text)["errcode"])
        print("发生错误跳过到下一页", data)
        if index<2000:#就怕万一几千页了一直报错会死循环 超过2000跳出
            return get_url_post(index=index, data=data,global_city_id=global_city_id)
        else:
            print("*************************超过2000页了 跳出*****************************")
            return 0
if __name__ == '__main__':
    # 配置 ip
    # username = 'xyy'
    # pwd = 'Xueyiyang'
    # user_pwd = pika.PlainCredentials(username, pwd)
    # s_conn = pika.BlockingConnection(
    #     pika.ConnectionParameters(host='188.131.239.119', port=5672, credentials=user_pwd))
    # chan = s_conn.channel()
    # chan_fail = s_conn.channel()
    # chan_city_tuple = s_conn.channel()
    # chan.queue_declare(queue='web_tj_id', auto_delete=False, durable=True)
    # chan_city_tuple.queue_declare(queue='city_dict', auto_delete=False, durable=True)
    # chan_fail.queue_declare(queue='web_tj_fail_id_page', auto_delete=False, durable=True)#
    #************
    # que_of_city_dict = Queue()  # 创建对象
    # creat_city_dict_que(que_of_city_dict=que_of_city_dict)#暂时先来十个地区的
    # x = get_mq()
    # print(x)
    # print(type(x))
    # print(eval(x)["city_id"],)
    # get_que_info(que=que_of_city_dict)

    # get_url_post()
    #********************进程池子又tm有问题  不能把
    while 1:
        p = Pool(4)
        for i in range(1,5):
            p.apply_async(get_url_post,)
        p.close()

        p.join()

    # p1 = Process(target=get_url_post,args=())
    # p2 = Process(target=get_url_post,args=())
    # p3 = Process(target=get_url_post,args=())
    #
    # p1.start()
    # p2.start()
    # p3.start()
    #
    # p1.join()
    # p2.join()
    # p3.join()
