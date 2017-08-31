from mongodb_queue import MogoQueue
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
import requests
from bs4 import BeautifulSoup
import os

import re
import lxml
import random
os.chdir(r'D:\python project\mzitu多进程，多线程')
headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
url = 'http://www.xicidaili.com/nn/1'
s = requests.get(url,headers = headers)
soup = BeautifulSoup(s.text,'lxml')
ips = soup.select('#ip_list tr')
fp = open('host.txt','w')
for i in ips:
    try:
        ipp = i.select('td')
        ip = ipp[1].text
        host = ipp[2].text
        fp.write(ip)
        fp.write('\t')
        fp.write(host)
        fp.write('\n')
    except Exception as e :
        print ('no ip !')
fp.close()
#代理ip
os.chdir(r'D:\python project\mzitu多进程，多线程')
url = 'https://www.baidu.com'
fp = open('host.txt','r')
ips = fp.readlines()
proxys = []
f_proxys = []
for p in ips:
    ip =p.strip('\n').split('\t')
    proxy = 'http:\\' +  ip[0] + ':' + ip[1]
    proxies = {'proxy':proxy}
    f_proxys.append(proxies)
for pro in f_proxys:
    s = requests.get(url,proxies = pro)
    if s.status_code == 200:
        proxys.append(pro)
        print(pro)

spider_queue = MogoQueue('meinvxiezhenji', 'crawl_queue')
def start(url):
    response = requests.get(url, headers=headers,proxies=random.choice(proxys))
    Soup = BeautifulSoup(response.text, 'lxml')
    all_a = Soup.find('div', class_='all').find_all('a')
    for a in all_a:
        title = a.get_text()
        url = a['href']
        spider_queue.push(url, title)
    """上面这个调用就是把URL写入MongoDB的队列了"""

if __name__ == "__main__":
    start('http://www.mzitu.com/all')

