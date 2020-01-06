#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     new_text
   Description :
   Author :       ltx
   date：          2019-07-14
-------------------------------------------------
"""
import re
import requests
from fontTools.ttLib import TTFont
from lxml.html import fromstring, tostring
from lxml.html.clean import Cleaner
from requests.exceptions import RequestException


def fetch(url, header, proxy):
    print(url)
    try:
        page_source = requests.get(url=url, headers=header, proxies=proxy).text
        __save_font(page_source)
        return page_source
    except FontSaveException:
        raise FontSaveException
    except RequestException:
        page_source = requests.get(url=url, headers=header, proxies=proxy).text
        __save_font(page_source)
        return page_source


class FontSaveException(Exception):
    pass


def __save_font(page_source):
    try:
        font_url = 'http:' + re.findall(",url\('(.*\.ttf)'", page_source)[0]
        font_res = requests.get(font_url).content
        with open('02.ttf', 'wb') as cf:
            cf.write(font_res)
    except IndexError:
        raise FontSaveException


def __comp(l1, l2):  # 定义一个比较函数，比较两个列表的坐标信息是否相同
    if len(l1) != len(l2):
        return False
    else:
        mark = 1
        for i in range(len(l1)):
            if abs(l1[i][0] - l2[i][0]) < 40 and abs(l1[i][1] - l2[i][1]) < 40:
                pass
            else:
                mark = 0
                break
        return mark


def __get_font(content, fonts):
    result = ''
    if content in fonts:
        result += str(fonts[content])
    else:
        result += content
    return result


def get_font_mapping():
    # 手动确定一组编码和字符的对应关系
    u_list = ['uniEDDF', 'uniED2C', 'uniED7E', 'uniECCA', 'uniEE0B', 'uniEC69', 'uniEDA9', 'uniEDFB', 'uniED48',
              'uniEC94',
              'uniECE6', 'uniEC33', 'uniED73', 'uniEDC5', 'uniED12', 'uniED64', 'uniECB0', 'uniEDF1', 'uniEC4F',
              'uniED8F',
              'uniECDC', 'uniED2E', 'uniEC7A', 'uniECCC', 'uniEC19', 'uniED59', 'uniEDAB', 'uniECF8', 'uniEC44',
              'uniEC96',
              'uniEDD7', 'uniEC34', 'uniED75', 'uniECC2', 'uniED13', 'uniEC60', 'uniEDA1', 'uniEDF2', 'uniED3F',
              'uniED91',
              'uniECDD', 'uniEC2A', 'uniEC7C', 'uniEDBC', 'uniED09', 'uniED5B', 'uniECA7', 'uniECF9', 'uniEC46',
              'uniED86',
              'uniEDD8', 'uniED25', 'uniEC71', 'uniECC3', 'uniEE04', 'uniEC62', 'uniEDA2', 'uniECEF', 'uniED41',
              'uniEC8D',
              'uniEDCE', 'uniEC2C', 'uniED6C', 'uniEDBE', 'uniED0B', 'uniEC57', 'uniECA9', 'uniEDEA', 'uniED36',
              'uniED88',
              'uniECD5', 'uniED27', 'uniEC73', 'uniEDB4', 'uniEE06', 'uniED52', 'uniEC9F', 'uniECF1', 'uniEC3D',
              'uniEC8F',
              'uniEDD0', 'uniED1C', 'uniED6E', 'uniECBB', 'uniEC59', 'uniED9A', 'uniEDEB', 'uniED38', 'uniEC85',
              'uniECD6']
    word_list = ['少', '低', '无', '六', '大', '身', '长', '短', '十', '只', '空', '动', '坏', '八', '远', '排', '实', '电', '有', '冷',
                 '耗',
                 '副', '下', '油', '四', '盘', '外', '九', '泥', '问', '软', '一', '多', '加', '上', '音', '矮', '比', '三', '真', '坐',
                 '自',
                 '养', '和', '过', '来', '档', '控', '手', '公', '着', '高', '级', '雨', '量', '启', '性', '得', '了', '机', '里', '硬',
                 '左',
                 '皮', '不', '很', '内', '的', '响', '光', '五', '地', '近', '灯', '好', '孩', '是', '更', '开', '门', '呢', '七', '路',
                 '保',
                 '小', '右', '中', '二', '味', '当']

    font1 = TTFont('01.ttf')
    be_p1 = []  # 保存38个字符的（x,y）信息
    for uni in u_list:
        p1 = []  # 保存一个字符的(x,y)信息
        p = font1['glyf'][uni].coordinates  # 获取对象的x,y信息，返回的是一个GlyphCoordinates对象，可以当作列表操作，每个元素是（x,y）元组
        # p=font1['glyf'][i].flags #获取0、1值，实际用不到
        for f in p:  # 把GlyphCoordinates对象改成一个列表
            p1.append(f)
        be_p1.append(p1)

    font2 = TTFont('02.ttf')
    uni_list2 = font2.getGlyphOrder()[1:]
    on_p1 = []
    for i in uni_list2:
        pp1 = []
        p = font2['glyf'][i].coordinates
        for f in p:
            pp1.append(f)
        on_p1.append(pp1)

    n2 = 0
    fonts = {}
    for d in on_p1:
        n2 += 1
        n1 = 0
        for a in be_p1:
            n1 += 1
            if __comp(a, d):
                uni_list2[n2 - 1] = uni_list2[n2 - 1].replace(r'uni', "\\u")
                uni_list2[n2 - 1] = eval(repr(uni_list2[n2 - 1]).replace('\\\\', '\\'))
                fonts[uni_list2[n2 - 1]] = word_list[n1 - 1]
    return fonts


def get_content(page_source, fonts, xpath_rule):
    cleaner = Cleaner()
    cleaner.javascript = True
    cleaner.style = True
    content_text = cleaner.clean_html(page_source.decode('utf-8'))
    content_text = fromstring(content_text).xpath(xpath_rule)
    content = ''
    for text in content_text:
        content += __get_font(content=text, fonts=fonts)
    content = content.strip().replace('\n', '')
    return content
