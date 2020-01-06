#Author:xue yi yang
import requests,json,time,random
def get_tupian(page,after):
    page=page
    after=after
    seed_url = 'https://page.appdao.com'
    task_uid = 261474
    clue_uid = 385585
    company_id = 218740
    clue_name = '壁纸精灵'
    url = "https://page.appdao.com/forward?link=9000459&style=051071101205&item=249348&page={}&limit=25&after={}&screen_w=750&screen_h=1334&ir=0&app=1P_CoolWallpapers&v=1.2&lang=zh-Hans-CN&it=1554775676.992411&ots=1&jb=0&as=0&mobclix=0&deviceid=replaceudid&macaddr=&idv=DE3CD818-930C-4945-9001-F53E18AC1248&idvs=&ida=76251974-4C2C-4A82-A8BB-17D6D8AD6EB0&phonetype=iphone&model=iphone7%2C2&osn=iOS&osv=11.4.1&tz=8".format(page,after)
    res = requests.get(url=url,verify=False)
    print(json.loads(res.text)["after"])
    if json.loads(res.text)["after"]!=after:
        page+=1
        print("page = --->",page)
        for each in json.loads(res.text)["data"]:
            res_url=res.url
            title=""
            if title in each:
                title = each["title"]
            if "pictures" in each:
                for img in each["pictures"]:
                    src = img["low"]["url"]
                    data = {
                        "pid": str(time.time()).split('.')[0] + str(random.randint(10000, 99999)),
                        "task_id": task_uid,
                        "clue_id": clue_uid,
                        "clue_name": clue_name,
                        "company_id": company_id,
                        "url": res_url,
                        "pic_url": src,
                        "client_date": "",
                        "url_article_title": title,
                        "url_article":"" ,
                        "is_cover": 0,
                    }
                    aa = {'resource': data}
                    d = json.dumps(aa)
                    #print(d)
                    url = 'http://shijue.qingapi.cn/task_python/start'
                    r = requests.post(url, data={"data": d})
                    print(r.text)
        return get_tupian(page,json.loads(res.text)["after"])
    else:
        print("相等 并且跑了---》",page)
        return print("相等 并且跑了---》",page)
if __name__ == '__main__':
    get_tupian(1,"")