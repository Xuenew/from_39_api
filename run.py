from flask import Flask,render_template,redirect,request
from spider_music_get import get_music_all_url
from get_news_info import get_news
from get_listen_read import get_info_listen
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json,re,datetime,pymysql
from random import randint
import time,os
from datetime import timedelta
import time
from spider_wenku import main as s_wenku
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=3) 
basedir = os.path.abspath(os.path.dirname(__file__))
from cai_jian import *
@app.route('/upload')#
def upload_test():
    return render_template('up_image.html')
@app.route('/up_image', methods=['post'])
def up_photo():
    if request.method=="POST":
        print(request.files)
        img = request.files.get('photo')
        # username = request.form.get("name")
        path = basedir+"/static/photo/"
        # file_path = path+img.filename
        img.save(path+"01_old.jpg")
        # print('上传头像成功，上传的用户是：'+username)
        print('上传头像成功，')
        # dst_w = 400
        # dst_h = 400
        # 保存的图片质量
        # save_q = 35
        resizeImg(ori_img=path+"01_old.jpg",dst_img=path+"01.jpg",dst_h=100,dst_w=100,save_q=35)
        resizeImg(ori_img=path+"01_old.jpg",dst_img=path+"02.jpg",dst_h=400,dst_w=400,save_q=35)
    
        return render_template('sanwei.html',val1=time.time())
        # return "ok cg tu pain"
    else:
        print("不是post请求")

@app.route('/wobufu')
def wobufu():
    return "{}----{}".format(["一点","二点","三点","四点","五点","六点"][randint(0,5)],time.strftime('%Y-%m-%d %H:%M:%S'))    
@app.route('/restaurant')
def restaurant():
    return render_template('/restaurant.html')
@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route("/search_music/<name>",methods=['GET'])
def back_song_list(name):
    """
    返回 输入音乐名字的搜索结果 默认 0-19 默认 播放链接是第一个
    :param name:
    :return:
    """
    name=name
    #print(name,"***********************************")
    p=get_music_all_url(music_name=name[5:])
    return p.get_music_song()
@app.route("/search_wenku/<name>",methods=['GET'])
def serch_wenku(name):
    name=name
    #print(name,"***********************************")
    p=s_wenku(string=name)
    return p
@app.route("/index_hot_image")
def back_index_hot_image():
    """
    返回 hot image 滑动的图片list
    :return:
    """
    p=get_music_all_url()
    return json.dumps(p.get_hot_image())
    # return "HI"
@app.route("/get_song/<mid>",methods=['GET'])
def back_song_musicl(mid):
    mid = mid[4:]
    #print(mid,"*******************",type(mid))
    # 测试用的 mid ：004AXFnZ33pU2z
    p=get_music_all_url()
    #print(p.get_music_src(mid))
    return p.get_music_src(mid)
@app.route("/index_new_music_list")
def back_new_music_list():
    p=get_music_all_url()
    return p.get_mudic_new_song_list()
@app.route("/index_hot_key")
def back_hot_key():
    p=get_music_all_url()
    return p.get_hot_key()
@app.route("/music_read/<url>",methods=['GET',"POST"])
def music_read(url):
    #print("right ")
    #print(url)
    # url = url[4:]
    # xx=request.values.get("key")
    url_t =" https://view.inews.qq.com/w/"+url
    p = get_news(url=url_t)
    return json.dumps(p.get_main_con())
@app.route("/get_read_listen/<info>",methods=['GET',"POST"])
def get_read_listen(info):
    info = info[5:]
    #print(info)
    p = get_info_listen(info)
    return p.get_listen()
#***************以下是二飘的借贷平台
#下拉刷新欠款和代还 xia_la_refresh
@app.route("/xia_la_refresh/<info>",methods=['GET',"POST"])
def xia_la_refresh(info):
    conn = pymysql.connect(host='39.108.15.78', port=3306, user='root', passwd='Xueyiyang', db='yang_ying_jie_dai',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute("select jie_kuan_jing_e from yong_hu_jie_tiao_tb where jie_kuan_ren_id=%s" % info)
    all_qian_kuan = cur.fetchall()
    #print(all_qian_kuan,"*-*-*--*欠款-*-*-*-*-*-")
    cur.execute("select jie_kuan_jing_e from yong_hu_jie_tiao_tb where zhai_zhu_ren_id=%s" % info)
    all_qian_wo_de_kuan = cur.fetchall()
    #print(all_qian_wo_de_kuan, "*-*-*--*借我钱的款-*-*-*-*-*-")
    # for num
    dai_huan = 0
    dai_shou = 0
    for num in all_qian_kuan:
        dai_huan  = dai_huan + int(num[0])
    for num in all_qian_wo_de_kuan:
        dai_huan  = dai_huan + int(num[0])
    data = json.dumps(
        {"res": "下拉刷新欠款，", "suc": "成功", "std": "1", "data": {"user_id": "", "user_info": {"dai_huan":dai_huan,"dai_shou":dai_shou}}})
    #print(data)
    return data
#刷新 我借别人的欠条 me_borrow 找 欠款人id
@app.route("/me_borrow/<info>",methods=['GET',"POST"])
def me_borrow(info):
    #print(info)
    conn = pymysql.connect(host='39.108.15.78', port=3306, user='root', passwd='Xueyiyang', db='yang_ying_jie_dai',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute("select * from yong_hu_jie_tiao_tb where jie_kuan_ren_id=%s" % info)
    all_info = cur.fetchall()
    data = json.dumps(
        {"res": "返回所有我借钱的欠条", "suc": "成功", "std": "1", "data": {"user_id": "", "user_info": all_info}})
    return data
#刷新 借我钱的欠条borrow_me 找 债主id
@app.route("/borrow_me/<info>",methods=['GET',"POST"])
def borrow_me(info):
    #print(info)
    conn = pymysql.connect(host='39.108.15.78', port=3306, user='root', passwd='Xueyiyang', db='yang_ying_jie_dai',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute("select * from yong_hu_jie_tiao_tb where zhai_zhu_ren_id=%s" % info)
    all_info = cur.fetchall()
    data = json.dumps(
        {"res": "返回所有欠我钱的欠条", "suc": "成功", "std": "1", "data": {"user_id": "", "user_info": all_info}})
    return data
#产生借条信息 以及准备确认
@app.route("/shen_qing_jie_tiao/<info>",methods=['GET',"POST"])
def shen_qing_jie_tiao(info):
    shu_ju = info.split(".")#{jk_name: "132", jk_money: "123", back_date: "123", jk_reason: "123"}
    # #print(info)
    forme_data = {"jk_name":shu_ju[0] , "jk_money": shu_ju[1] , "back_date": shu_ju[2] , "jk_reason": shu_ju[3],"zhai_zhu_phone":shu_ju[4],"jie_kuan_ren_id":shu_ju[5] }
    #print(forme_data)#获取返回来的借款信息 表里面 欠款人是债主的意思
    conn = pymysql.connect(host='39.108.15.78', port=3306, user='root', passwd='Xueyiyang', db='yang_ying_jie_dai',
                           charset='utf8')
    cur = conn.cursor()
    for k in forme_data:
        if forme_data[k]:
            pass
        else:
            forme_data[k] = ""
    jk_ri_qi = datetime.date.today()
    key_excut="insert into yong_hu_jie_tiao_tb(zhai_zhu_ren_id,jie_kuan_ren_name,jie_kuan_jing_e,jie_kuan_ri_qi,gui_huan_ri_qi,jie_kuan_yuan_yin,shi_fou_que_ren,jie_kuan_ren_id) values(%s,%s,%s,%s,%s,%s,%s,%s)" % (
        "'" + forme_data["zhai_zhu_phone"] + "'", "'" + forme_data["jk_name"] + "'", "'" + forme_data["jk_money"] + "'",
        "'" + str(jk_ri_qi) + "'", "'" + forme_data["back_date"] + "'", "'" + forme_data["jk_reason"] + "'",
        "'" + "NO" + "'", "'" + forme_data["jie_kuan_ren_id"] + "'")
    # #print(key_excut,"999999999999999999999999999")
    cur.execute(key_excut)
    conn.commit()
    #print("ti jiao cheng gong")
    data = json.dumps(
        {"res": "借条已经成立，并且给对方发送了短信", "suc": "成功", "std": "1", "data": {"user_id": "", "user_info": key_excut}})
    client = AcsClient('LTAIkhQicIDwuAPU', 'TatinbuNNC4MMD9lCLBQPUs1i3WVgF', 'cn-hangzhou')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', "{}".format(forme_data["zhai_zhu_phone"]))
    request.add_query_param('SignName', "友借友还")
    request.add_query_param('TemplateCode', "SMS_165414732")
    request.add_query_param('TemplateParam', "{\"code\":\"%s\"}"%forme_data["jie_kuan_ren_id"][-4:])

    response = client.do_action(request)
    # python2:  print(response)
    # print(str(response, encoding='utf-8'))
    return data
#返回好友列表
@app.route("/get_user_friends_info/<info>",methods=['GET',"POST"])
def get_user_friends_info(info):
    #print(info)
    #先去表里面找到好友
    conn = pymysql.connect(host='39.108.15.78', port=3306, user='root', passwd='Xueyiyang', db='yang_ying_jie_dai',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute("select ID from yong_hu_tb where Name=%s" % info)
    user_id = cur.fetchall()[0][0]
    cur.execute("select tian_jia_hao_you_id from yong_hu_guan_xi_tb where self_id=%s" % user_id)
    friends_id_list = cur.fetchall()
    #print(friends_id_list,"朋友列表")
    tup = []#朋友的id的列表最后转化成元组 元组不可修改
    for num in friends_id_list:
        tup.append(int(num[0]))
    vlu = list(tup)
    if len(vlu)>=1:
        #print(str(vlu),"变成列表")
        #print(re.findall(r'\[(.*)\]',str(vlu))[0])
        excut = "select * from yong_hu_tb where ID in ({})".format(re.findall(r'\[(.*)\]',str(vlu))[0])
        #print(excut)
        cur.execute(excut)
        all_good_frends = cur.fetchall()#搜索所有相关好友
        data = json.dumps({"res": "找到所有好友列表", "suc": "成功", "std": "1", "data": {"user_id": "","user_info":all_good_frends}})
        return data
    elif len(vlu)==0:
        data = json.dumps(
            {"res": "未找到所有好友列表", "suc": "成功", "std": "0", "data": {"user_id": "", "user_info": {}}})
        return data

#输入好友id添加好友
@app.route("/tian_jia_hao_you_id/<info>",methods=['GET',"POST"])
def tian_jia_hao_you_id(info):
    #print(info)
    shu_ju = info.split(".")
    #print(shu_ju)
    info_frends_id = shu_ju[0]
    info_self_id = shu_ju[1]
    conn = pymysql.connect(host='39.108.15.78', port=3306, user='root', passwd='Xueyiyang', db='yang_ying_jie_dai',
                           charset='utf8')
    cur = conn.cursor()
    cur.execute("select * from yong_hu_tb where Name=%s" % info_frends_id)
    ##print(cur.fetchall(), "查询 name字段 看返回值")
    get_cur_all = cur.fetchall()
    #print(len(get_cur_all),"chang du ")
    if len(get_cur_all) >= 1:
        #print("jing xing dao 111111")
        cur.execute("select * from yong_hu_tb where Name=%s" % info_frends_id)
        frends_id = cur.fetchall()[0][0]
        cur.execute("select * from yong_hu_tb where Name=%s" % info_self_id)
        self_id = cur.fetchall()[0][0]
        cur.execute(
            "insert into yong_hu_guan_xi_tb(tian_jia_hao_you_id,self_id) values(%s,%s)" %(frends_id,self_id)
        )
        conn.commit()
        cur.execute("select * from yong_hu_tb where Name=%s" %info_frends_id)
        all_good_frends = cur.fetchall()
        #print(all_good_frends,"我的好友的全部信息，")
        data = json.dumps({"res": "找到用户,并且您已经成功添加对方为好友", "suc": "成功", "std": "1", "data": {"user_id": info_self_id,"user_info":all_good_frends}})
        cur.close()
        conn.close()
        return data
    elif len(get_cur_all) == 0:
        data = json.dumps({"res": "没有找到此用户", "suc": "成功", "std": "0", "data": {}})
        cur.close()
        conn.close()
        return data
#登陆获取手机号注册 验证手机号
@app.route("/get_phone_number/<info>",methods=['GET',"POST"])
def get_phone_number(info):
    # info = info[5:]
    #print(info)
    if len(info)!=11:
        data = json.dumps({"res":"请输入正确的号码","suc":"错误","std":"0","data":{}})
        return data
    for num in info:
        if str(num) not in ["0","1","2","3","4","5","6","7","8","9",]:
            data = json.dumps({"res":"请输入正确的号码","suc":"错误","std":"0","data":{}})
            return data
        #下面是进行user_id的生成 先暂时就电话号码
        #
        # user_id =
    conn = pymysql.connect(host='39.108.15.78', port=3306, user='root', passwd='Xueyiyang', db='yang_ying_jie_dai', charset='utf8')
    cur = conn.cursor()
    cur.execute("select * from yong_hu_tb where Name=%s"%info)
    #print(cur.fetchall(),"查询 name字段 看返回值")
    if len(cur.fetchall())>=1:
        data = json.dumps({"res": "已经存在的用户", "suc": "成功", "std": "1", "data": {"user_id": info}})
        return data
    elif len(cur.fetchall())==0:
        cur.execute(
            "insert into yong_hu_tb(Name) values(%s)"%info
        )
        conn.commit()
        cur.close()
        conn.close()
        data = json.dumps({"res": "登陆号码输入正确", "suc": "成功", "std": "1","data":{"user_id":info}})
        return data
#一下是python的搭建library
#get python else html
@app.route("/<info>",methods=['GET',"POST"])
def get_python_else_html(info):
    return render_template("/python_html/{}".format(info))
#get python index
@app.route("/python",methods=['GET',"POST"])
def get_python_doc():
   # return render_template("/python_html/index.html")
    return redirect("https://www.324xyy.top/static/python_html/index.html")
if __name__ == '__main__':
    #from werkzeug.contrib.fixers import ProxyFix
    #app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='0.0.0.0',port=5000,debug=True)
    #app.run()
