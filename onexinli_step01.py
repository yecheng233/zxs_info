# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 18:51:27 2017
@author: yecheng@cug.edu.cn
"""

# 导入第三方包
import requests
from bs4 import BeautifulSoup


# 设置伪头
headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
}


#目标链接
urls=['http://www.xinli001.com/zx-p'+str(i+1) for i in range(30)]


#构建空列表,数据存储
user_url=[]  #咨询师主页
name=[]   #姓名
title=[]   #标签
intro=[]   #个签
case_num=[] #已咨询数
ratings=[]  #好评率
price=[]   #语音价格



#爬取需要的信息
for url in urls:
    r=requests.get(url,headers = headers,timeout=3).text
    soup=BeautifulSoup(r,'lxml')
    try:
        
        user_url.extend(i.a['href'] for i in soup.find_all("div",class_="add_expert_list")[0].find_all("div",class_="l"))
        name.extend(i.a.text.strip() for i in soup.find_all("div",class_="add_expert_list")[0].find_all("div",class_="l") )
        title.extend(i.span.text.strip() for i in soup.find_all("div",class_="add_expert_list")[0].find_all("div",class_="l") )
        intro.extend(i.p.text.strip() for i in soup.find_all("div",class_="add_expert_list")[0].find_all("div",class_="text") )
        case_num.extend(i.span.text.strip() for i in soup.find_all("div",class_="add_expert_list")[0].find_all("dd",class_="cb"))
        ratings.extend(i.span.text.strip() for i in soup.find_all("div",class_="add_expert_list")[0].find_all("dd",class_="xl"))
        price.extend(i.text.strip() for i in soup.find_all("div",class_="add_expert_list")[0].find_all("dd",class_="jq"))
    except IndexError:
        pass
    
#输出数据到excel表格
import pandas as pd
zxs_intro=pd.DataFrame([user_url,name,title,intro,case_num,ratings,price]).T
zxs_intro=zxs_intro.rename(columns={0:'咨询师主页',1:'姓名',2:'标签',3:'个签',4:'已咨询数',5:'好评率',6:'语音咨询价格'})
zxs_intro.to_excel(r'C:\Users\Administrator\Desktop\onexinli_zxs.xlsx',sheet_name='zxs_intro')




