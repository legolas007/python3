import os
import time
import threading
import multiprocessing
from mongodb_queue import MogoQueue
import requests
from bs4 import BeautifulSoup
import os
import random

os.chdir(r'D:\python project\mzitu多进程，多线程')
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
url = 'http://www.xicidaili.com/nn/1'
s = requests.get(url, headers=headers)
soup = BeautifulSoup(s.text, 'lxml')
ips = soup.select('#ip_list tr')
fp = open('host.txt', 'w')
for i in ips:
    try:
        ipp = i.select('td')
        ip = ipp[1].text
        host = ipp[2].text
        fp.write(ip)
        fp.write('\t')
        fp.write(host)
        fp.write('\n')
    except Exception as e:
        print('no ip !')
fp.close()
# 代理ip
os.chdir(r'D:\python project\mzitu多进程，多线程')
url = 'https://www.baidu.com'
fp = open('host.txt', 'r')
ips = fp.readlines()
proxys = []
f_proxys = []
for p in ips:
    ip = p.strip('\n').split('\t')
    proxy = 'http:\\' + ip[0] + ':' + ip[1]
    proxies = {'proxy': proxy}
    f_proxys.append(proxies)
for pro in f_proxys:
    s = requests.get(url, proxies=pro)
    if s.status_code == 200:
        proxys.append(pro)
        print(pro)

SLEEP_TIME = 1

def mzitu_crawler(max_threads=10):
    crawl_queue = MogoQueue('meinvxiezhenji', 'crawl_queue') ##这个是我们获取URL的队列
    img_queue = MogoQueue('meinvxiezhenji', 'img_queue') ##这个是图片实际URL的队列
    def pageurl_crawler():
        while True:
            try:
                url = crawl_queue.pop()
                print(url)
            except KeyError:
                print('队列没有数据')
                break
            else:
                img_urls = []
                req = requests.get(url, headers=headers,proxies=random.choice(proxys)).text
                title = crawl_queue.pop_title(url)
                path = str(title).replace('?', '') ##测试过程中发现一个标题有问号
                mkdir(path)
                os.chdir('D:\mzitu\\' + path)
                max_span = BeautifulSoup(req, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
                for page in range(1, int(max_span) + 1):
                    page_url = url + '/' + str(page)
                    img_url = BeautifulSoup(requests.get(page_url, headers=headers,proxies=random.choice(proxys)).text, 'lxml').find('div', class_='main-image').find('img')['src']
                    img_urls.append(img_url)
                    save(img_url)
                crawl_queue.complete(url) ##设置为完成状态
                img_queue.push_imgurl(title, img_urls)
                print('插入数据库成功')

    def save(img_url):
        name = img_url[-9:-4]
        print(u'开始保存：', img_url)
        img = requests.get(img_url, headers=headers,proxies=random.choice(proxys))
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(path):
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\mzitu", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("D:\mzitu", path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    threads = []
    while threads or crawl_queue:
        """
        这儿crawl_queue用上了，就是我们__bool__函数的作用，为真则代表我们MongoDB队列里面还有数据
        threads 或者 crawl_queue为真都代表我们还没下载完成，程序就会继续执行
        """
        for thread in threads:
            if not thread.is_alive(): ##is_alive是判断是否为空,不是空则在队列中删掉
                threads.remove(thread)
        while len(threads) < max_threads or crawl_queue.peek(): ##线程池中的线程少于max_threads 或者 crawl_qeue时
            thread = threading.Thread(target=pageurl_crawler) ##创建线程
            thread.setDaemon(True) ##设置守护线程
            thread.start() ##启动线程
            threads.append(thread) ##添加进线程队列
        time.sleep(SLEEP_TIME)

def process_crawler():
    process = []
    num_cpus = multiprocessing.cpu_count()
    print('将会启动进程数为：', num_cpus)
    for i in range(num_cpus):
        p = multiprocessing.Process(target=mzitu_crawler) ##创建进程
        p.start() ##启动进程
        process.append(p) ##添加进进程队列
    for p in process:
        p.join() ##等待进程队列里面的进程结束

if __name__ == "__main__":
    process_crawler()