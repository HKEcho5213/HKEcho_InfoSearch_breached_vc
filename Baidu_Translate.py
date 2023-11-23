# -*- coding: utf-8 -*-
# /usr/bin/env python
# coding=utf8

import json
import http.client  # 修改引用的模块
import hashlib  # 修改引用的模块
import urllib
from urllib import parse
import random

def baiduTranslate(translate_text, flag=1):
    '''
    flag=1 输入的句子翻译成英文
    flag=0 输入的句子翻译成中文
    '''
    appid = 'xxxxxxxxxxxxxxxxxxxxx'  # 填写你的appid
    secretKey = 'xxxxxxxxxxxxxxxxxxx'  # 填写你的密钥
    httpClient = None
    myurl = '/api/trans/vip/translate'  # 通用翻译API HTTP地址
    fromLang = 'auto'  # 原文语种

    if flag:
        toLang = 'en'  # 译文语种
    else:
        toLang = 'zh'  # 译文语种

    salt = random.randint(3276, 65536)

    sign = appid + translate_text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(translate_text) + '&from=' + fromLang + \
            '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        # return result
        return result['trans_result'][0]['dst']

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

