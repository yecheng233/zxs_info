"""
Created on Fri Dec  1 16:41:51 2017

@author: yecheng@cug.edu.cn
"""

#处理异步加载的问题

#加上时间,方便再最后查看代码执行时间
from time import clock
start=clock()


import requests
from bs4 import BeautifulSoup
import json

headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
}

zxs_url=[]
urls=['http://www.xinli001.com/zx-p'+str(i+1) for i in range(30)]
for url in urls:
    lr=requests.get(url,headers=headers)
    lsoup=BeautifulSoup(lr.text,'lxml')
    zxs_url.extend(i.a['href'] for i in lsoup.find_all("div",class_="add_expert_list")[0].find_all("div",class_="l"))

#本次抓取的内容空表,字段名
zxs_id=[]     #咨询师的id，作为key
lf_name=[]    #来访者的昵称
time=[]       #评论的日期
lf_comments=[]  #评论内容

for url in zxs_url:
    urr=requests.get(url=url.replace('http://www.xinli001.com/expert','https://www.xinli001.com/expert/detail'),params={"tab":'comment'},headers=headers)
    print(url)
    ursoup=BeautifulSoup(urr.text,'lxml')
    if ursoup.html.get('lang') != 'en':
        continue
    else:
        M=len([i.h5.text.strip() for i in ursoup.find_all('div',class_='thanks-note')])
        print(M)
        try:
            id=(url[31:]+'-')*M
            print(id)
            zxs_id.extend(id.split('-')[:-1])
            zxs_info=ursoup.find('div',class_='tab-content on')
            lf_name.extend(i.h5.text.strip() for i in zxs_info.find_all("div",class_="thanks-note"))
            time.extend(i.span.text.strip() for i in zxs_info.find_all("div",class_="thanks-note"))
            lf_comments.extend(i.text.strip() for i in zxs_info.find_all("div",class_="txt"))
        except:
            pass
          
print("判断网页的新旧")
           
zxs=[]

for url in zxs_url:
    ur=requests.get(url,headers=headers)
    usoup=BeautifulSoup(ur.text,"lxml")
    if usoup.html.get('lang') != 'en':
        continue
    else:
        zxs.append(url)


       
for z_url in zxs:
    print(z_url)
    for page in range(200):    
        r=requests.get(z_url.replace('http://www.xinli001.com/expert','https://www.xinli001.com/expert/detail'),params={'tab':'comment','page':str(page+1),'type':'comment'},headers=headers)
        dr=json.loads(r.text) 
        if len(dr['data']['list'])==0:
            break
        else:
#    #每页评论的数量
            soup=BeautifulSoup(dr['data']['list'],'lxml') 
            N=len([i.text.strip() for i in soup.find_all('div',class_='txt')])
            try:
                id=(z_url[31:]+'-')*N
                zxs_id.extend(id.split('-')[:-1])
                lf_name.extend(i.text.strip() for i in soup.find_all('h5',class_="name"))
                time.extend(i.text.strip() for i in soup.find_all('span',class_='time'))
                lf_comments.extend(i.text.strip() for i in soup.find_all('div',class_='txt'))  
            except:
                pass
 


#输出到excel文件中             
import pandas as pd
comments_info=pd.DataFrame([zxs_id,lf_name,time,lf_comments]).T
comments_info=comments_info.rename(columns={0:'咨询师id',1:'来访者昵称',2:'创建时间',3:'评论内容'})
comments_info.to_excel(r'C:\Users\Administrator\Desktop\onexinli_lf.xlsx',sheet_name='lf_comments')



end=clock()
print(end-start)
