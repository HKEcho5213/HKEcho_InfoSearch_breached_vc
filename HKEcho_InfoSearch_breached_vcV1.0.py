# -*- coding: utf-8 -*-
import datetime, sys, re, time, schedule
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests, json, urllib3
from chinese_calendar import is_workday
from urllib3.exceptions import InsecureRequestWarning
from Baidu_Translate import baiduTranslate
from urllib3 import disable_warnings
import Breached_vc_Robot
import cloudscraper
import sys

sys.setrecursionlimit(50000)    #python默认递归1000，这里可以设置
disable_warnings(InsecureRequestWarning)  # https问题的报错
urllib3.disable_warnings()
URL = 'https://breached.vc/'
PROXY = '127.0.0.1:10809'
RESULTS = []
Rest_Day_Data = [] #休息日保存列表
flag = 1
cookie_flag = 1
a = 0
b = 0


#判断关键字，及时发送消息
KeyWord = ['china','guangzhou','Macao' , 'Hong Kong' ,'Chinese', 'cn', 'shanghai', 'shenzhen', 'guangdong', '中国', '广州', '上海', '深圳', '广东', '公司', '集团']
#
Already_Send_Data = []


def Breached_Search(url):
    '''
    真正实现功能的函数
    :param url:
    :return:
    '''
    global flag,cookie_flag, PROXY, Already_Send_Data, Rest_Day_Data, a ,b
    Today_Time = time.ctime().split(' ')  # ['Wed', 'Dec', '28', '10:23:13', '2022']
    headers = {
        "User-Agent":UserAgent().random,    #随机UA
        #"Cookie":json.load(open("config/Config.json", "r"))["Breached_Vc_Cookie"],
        "Connection": "close"
    }
    proxies = {
        'http': 'http://'+ PROXY,
        'https': 'http://'+ PROXY
    }
    try:
        scraper = cloudscraper.create_scraper()
        resp = scraper.get(url, headers=headers, proxies=proxies, timeout=20)
        # 站点需要认证：
        if 'Your User-Agent' in resp.text and 'Your IP Address' in resp.text:
            print('\033[0;30;41m----网页认证拦截,程序自动刷新，请稍等----\033[0m')
            time.sleep(0.5)
            Breached_Search(url)
        else:
            # if 'zhirui' not in resp.text:
            #     if cookie_flag == 4:
            #         print('\033[0;30;43m----Cookie已过期，请于配置文件重新替换----\033[0m')
            #         message = '【监测告警】' + '\n\n' + "您的Cookie已过期，请于服务器配置文件中重新替换"
            #         Breached_vc_Robot.Breached_Robot(message)
            #         sys.exit(1)
            #     else:
            #         print('\033[0;30;43m----Cookie貌似过期，程序正在验证，请稍等----\033[0m')
            #         cookie_flag += 1
            #         Breached_Search(url)
            # else:
            html = resp.content.decode("utf-8")
            soup = BeautifulSoup(html, 'lxml')
            tr_tag = soup.find_all(name='tr',attrs={"class":"inline_row"})
            for tr in tr_tag:
                tr_soup = BeautifulSoup(str(tr), 'lxml')
                '''
                时间
                <span title="December 26, 2022, 03:28 PM">10 hours ago</span>
                '''
                time_span_tar = tr_soup.find_all(name='span', attrs={"class":"forum-display__thread-date"})
                # print(time_span_tar)
                if 'title' in str(time_span_tar[0]):
                    time_soup = BeautifulSoup(str(time_span_tar), 'lxml')
                    time_span_tar = time_soup.find_all(name='span', attrs={"title": re.compile(".*?")})
                    time_title_soup = BeautifulSoup(str(time_span_tar), 'lxml')
                    article_time = time_title_soup.span['title']
                else:
                    '''[<span class="forum-display__thread-date"><i class="far fa-clock"></i> December 27, 2022, 09:36 AM</span>]'''
                    time_soup = BeautifulSoup(str(time_span_tar), 'lxml')
                    article_time = time_soup.span.text
                # print(article_time)

                # if (Today_Time[1] in str(article_time)) and (Today_Time[2] in str(article_time)) or (
                #         str(int(Today_Time[2]) - 4) in str(article_time)) and (Today_Time[4] in str(article_time)):
                # Today_Time = time.ctime().split(' ')  # ['Fri', 'Jan', '', '6', '14:28:12', '2023']
                # if (Today_Time[1] in str(article_time)) and (Today_Time[3] in str(article_time)) and (Today_Time[5] in str(article_time)):
                article_demo = article_time.split(' ')
                if len(Today_Time) == 6:
                    #每月1-9号
                    a = 3
                    b = 5
                elif len(Today_Time) == 5:
                    # 每月10-号
                    a = 2
                    b = 4
                if (Today_Time[1] in article_demo[0]) and (Today_Time[a] in article_demo[1]) and (
                        Today_Time[b] in article_demo[2]):
                    ''',通过判断时间，来决定需要的数据，去掉干扰项。'''
                    name_href_span_tar = tr_soup.find_all(name='span',attrs={"class":"subject_new"})
                    '''
                        href与name
                        <span class=" subject_new" id="tid_53640">
                        <a href="Thread-Vapotech-fr-14k-users-2021">Vapotech.fr - [14k users] - 2021</a></span>
                    '''
                    # print(name_href_span_tar)
                    for name_span in name_href_span_tar:
                        a_soup = BeautifulSoup(str(name_span), 'lxml')
                        article_url = URL + a_soup.a['href']
                        article_name = a_soup.string
                        Translate_article_name = baiduTranslate(article_name, flag=0)
                        if '~'  in article_name:
                            '''这里防止事件名称里面有特殊符号'''
                            article = str(flag) + '^' + article_name + '^' +Translate_article_name + '^' + article_url + '^' + article_time
                        else:
                            article = str(flag) + '~' + article_name + '~' +Translate_article_name + '~' + article_url + '~' + article_time
                        for Key in KeyWord:
                            '''
                            匹配关键字，重点监测地区或目标，监测到就及时发送到钉钉
                            '''
                            if re.search(Key, article_name, re.I):
                                if '|' in article_name:
                                    article_name = article_name.replace('|', '_')
                                article_demo = str(1) + '~' + article_name + '~' +Translate_article_name + '~' + article_url + '~' + article_time
                                if article_demo in Already_Send_Data:
                                    pass
                                else:
                                    '''这里还要判断之前是否已经发送过该事件，没有此判断的话会导致多次发送'''
                                    # if isDuringThatTime(startTime='8:50',endTime="18:00"):
                                    #     '''判断时间是否在工作时间'''
                                    #     if len(Rest_Day_Data) != 0:
                                    #         ''''''
                                    #         for Rest_Day_Data_demo in Rest_Day_Data:
                                    #             Send_Dingtalk_Robot_Timely(Rest_Day_Data_demo)
                                    #             print('\033[0;30;42m【休息日关键字数据】已同步至【SXF南方重保威胁情报】\033[0m')
                                    #         Rest_Day_Data.clear()
                                    Send_Dingtalk_Robot_Timely(article_demo)
                                    print('\033[0;30;42m【%s】已同步至【SXF南方重保威胁情报】\033[0m' % article_name)
                                    # else:
                                    #     '''不在工作时间将数据进行保存'''
                                    #     Rest_Day_Data.append(article_Timely)
                                    Already_Send_Data.append(article_demo)
                                break
                        RESULTS.append(article)
                        flag += 1
            print(RESULTS)
    except Exception as err:
        print('\033[0;30;41m----请求异常,程序正在重新请求，请稍等----\033[0m')
        time.sleep(0.5)
        Breached_Search(url)

def pd_toexcel():
    Filename_Out_Path = 'outputs/' + 'breached.vc-%s.xlsx' % str(datetime.date.today())
    '''
    导出结果至xlsx文件
    :return:
    '''
    print('\033[0;30;44m----数据正在导出----\033[0m')
    excel_list = []
    First_line = ('序号', '原-事件名', '翻译-事件名','链接', '时间',)
    excel_list.insert(0, First_line)
    for reslist in RESULTS :
        if reslist.count('^') == 3:
            '''这里防止事件名称里面有特殊符号'''
            chr_list = reslist.split('^')
        else:
            chr_list = reslist.split('~')
        excel_list.append(tuple(chr_list))
    df = pd.DataFrame(excel_list[1:], columns=excel_list[0])
    df.to_excel(Filename_Out_Path, index=False)
    print('\033[0;30;42m----数据已爬取完成已导出至/outputs目录----\033[0m')

def Send_Dingtalk_Robot_Timely(article):
    table_head = '\n序号|原-事件名|翻译-事件名|链接|时间\n'
    if article.count('^') == 4:
        '''这里防止事件名称里面有特殊符号'''
        chr_list = article.split('^')
    else:
        chr_list = article.split('~')
    table_body = '|'.join(chr_list) + '\n'
    # 制作列表分隔符
    table_split = '-|' * 5 + "\n"
    # 拼接成table变量
    table = '关键字监测情况如下：\n' + table_head + table_split + table_body
    Breached_vc_Robot.Breached_Robot(table)

def Send_Dingtalk_Robot_Oneday():
    Filename_Out_Path = 'outputs/' + 'breached.vc-%s.xlsx' % str(datetime.date.today())
    table_body = ''
    # 数据文件
    excel_file = Filename_Out_Path
    excel = pd.read_excel(excel_file)  # 读取Excel表格
    excel_table_head = list(excel.columns.values)  # 读取表头
    table_head = '|'.join(excel_table_head) + "\n"  # 拼接表头
    # 获取表格主体
    excel_table_body = list(excel.iloc[0:].values)
    new_table_body = []
    # 将每一个列表项转换为字符串
    for i in excel_table_body:
        row = []
        for j in i:  # 对这一行的遍历
            row.append(str(j))  # 转换为字符串并加入row列表
        new_table_body.append(row)  # 再将row加入new_table_body
    for i in new_table_body:
        if '|' in str(i[1]):
            i[1] = i[1].replace('|', '_')
            table_demo = '|'.join(i)
        else:
            table_demo = '|'.join(i)
        table_body = table_body + table_demo + '\n'
    # 制作列表分隔符
    table_split = '-|' * len(excel_table_head) + "\n"
    # 拼接成table变量
    table = '今日整体监测情况如下：\n' + table_head + table_split + table_body
    Breached_vc_Robot.Breached_Robot(table)
    print('\033[0;30;42m【今日整体监测情况】已同步至【SXF南方重保威胁情报】\033[0m')

def isDuringThatTime(startTime, endTime):
    '''这个函数用于节假日、还有晚上不发送消息到钉钉'''
    now_time = datetime.datetime.now()
    # if is_workday(now_time.date()): #为工作日，返回True
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + startTime, '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + endTime, '%Y-%m-%d%H:%M')
    if start_time < now_time < end_time:    #判断是否在工作日的时间段工作
        return True
    return False
    # else:   #为休息日，返回False
    #     return False

def main():
    global flag
    print('\033[0;30;44m----数据爬取中----\033[0m')
    RESULTS.clear()
    flag = 1
    for page in range(1,3):
        ''' BreachForums-->Leaks-->Databases'''
        url = URL + 'Forum-Databases?page=%s&sortby=started'%str(page)
        Breached_Search(url)
        time.sleep(0.5)
        ''' BreachForums-->Marketplace-->Sellers Place'''
        url = URL + 'Forum-Sellers-Place?page=%s&sortby=started'%str(page)
        Breached_Search(url)
        time.sleep(0.5)
        ''' BreachForums-->Marketplace-->Sellers Place-->Leaks Market'''
        url = URL + 'Forum-Leaks-Market?page=%s&sortby=started' % str(page)
        Breached_Search(url)
        time.sleep(0.5)
        ''' BreachForums-->Leaks-->Other Leaks'''
        url = URL + 'Forum-Other-Leaks?page=%s&sortby=started' % str(page)
        Breached_Search(url)
        time.sleep(0.5)
    print('\033[0;30;44m----数据爬取完成----\033[0m')
    if RESULTS:
        pd_toexcel()

schedule.every(15).minutes.do(lambda: main())
schedule.every().day.at("16:00").do(lambda: Send_Dingtalk_Robot_Oneday())  #每天下午发一遍全量的数据到钉钉
if __name__ == '__main__':
    main()
    while True:
        schedule.run_pending()
