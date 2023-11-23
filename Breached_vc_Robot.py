# -*- coding: utf-8 -*-
import json, requests, time
import hmac
import hashlib
import base64
import urllib.parse

secret = str(json.load(open("config/Config.json", "r"))["Robot_Secret"])
oapi_url = str(json.load(open("config/Config.json", "r"))["Robot_Oapi_Url"])
def Breached_Robot(Send_Datas):
    global secret, oapi_url
    timestamp = str(round(time.time() * 1000))
    secret = secret
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    Robot_Url = oapi_url + '&timestamp=%s&sign=%s'%(timestamp,sign)
    # isAtAll：是否@所有人，建议非必要别选，不然测试的时候很尴尬
    dict = {
        "msgtype": "markdown",
        "markdown": {"title": "Breached.vc数据泄露小助手",
                        "text": ""
                        },
        "at": {
            "isAtAll": True
        }
    }
    #把文案内容写入请求格式中
    dict["markdown"]["text"] = Send_Datas
    send_request(Robot_Url,dict)
def send_request(url, datas):
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    sendData = json.dumps(datas)
    sendDatas = sendData.encode("utf-8")
    request = requests.post(url=url, data=sendDatas, headers=header)
    opener = request.text
    # 输出响应结果
    # print(opener)

