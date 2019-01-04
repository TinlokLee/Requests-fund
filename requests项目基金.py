#coding=utf-8

# spider.py
import geturl
from multiprocessing import Pool
import requests
import re
import pymongo
import time
from bs4 import BeautifulSoup


# 建立连接，MonogoDB数据库
clients = pymongo.MongoClient('127.0.0.1')
# 指定数据库
db = clients['hexun']
# 返回数据集合1
col1 = db['fund']
# 返回数据集合2
col2 = db['detail']

url = 'http://fund.eastmoney.com/allfund.html'

# 获取第二种布局方法2
def run_detail2(code,name,url):
	soup = getstart.geturl_utf8(url)
	tags = soup.find_all(class_='ui-font-middle ui-color-red ui-num')
	m1 = tags[3].string
	y1 = tags[4].string
	m3 = tags[5].string
	y3 = tags[6].string
	m6 =tags[7].string
	rece = tags[8].string
	detail = {'代码':code,'名称':name,'近1月':m1,'近3月':m3,'近6月':m6,'近1年':y1,'近3年':y3,'成立来':rece}
	#print(detail)
	col2.insert(detail)
	

# 获取第一种布局方法1，报错执行方法2
def run_detail1(code,name,url):

	soup=getstart.geturl_utf8(url)
	tags=soup.select('dd')
	try:
		m1 = (tags[1].find_all('span')[1].string)
		y1 = (tags[2].find_all('span')[1].string)
		m3 = (tags[4].find_all('span')[1].string)
		y3 = (tags[5].find_all('span')[1].string)
		m6 = (tags[7].find_all('span')[1].string)
		rece = (tags[8].find_all('span')[1].string)
		detail = {'代码':code,'名称':name,'近1月':m1,'近3月':m3,'近6月':m6,'近1年':y1,'近3年':y3,'成立来':rece}
		print(detail)
		col2.insert(detail)
	except: 
		run_detail2(code,name,url)


soup = getstart.geturl_gbk(url)
tags = soup.select('.num_right > li')
for tag in tags:
	if tag.a is None:
		continue
	else:
		content = tag.a.text
		code = re.findall(r'\d+',content)[0]
		#print(code)
		name = content.split('）')[1]
		#print(name)
		url = tag.a['href']
		#print(content)
		content_dict = {'code':code,'name':name,'url':url}
		#print (content_dict)
		col1.insert(content_dict)
		time.sleep(0.1)
		run_detail1(code,name,url)




# geturl.py
from bs4 import BeautifulSoup
import requests, random


UA_LIST = [ 
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", 
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", 
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", 
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24" 
]

headers = { 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
    'Accept-Encoding': 'gzip, deflate, sdch', 
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6', 
    'Connection': 'keep-alive',
    'User-Agent': random.choice(UA_LIST) 
}

proxies = [ 'http://118.178.124.33:3128',
            'http://139.129.166.68:3128',
            'http://61.163.39.70:9999',
            'http://61.143.228.162'
            ]

# 封装 requests 和 BeautifulSoup 函数
def geturl_gbk(url):
    '''解码gbk'''
    html = requests.get(url, headers=headers, 
                proxies={'http':random.choice(proxies)}).content.decode('gbk')
	soup = BeautifulSoup(html,'lxml')
	return soup


def geturl_utf8(url):
    '''解码utf8'''
    html = requests.get(url, headers=headers,
                proxies={'http':random.choice(proxies)}).content.decode('utf-8')
	soup = BeautifulSoup(html,'lxml')
	return soup	


#proxies={'http':random.choice(proxies)}       