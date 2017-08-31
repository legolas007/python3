
import requests
from bs4 import BeautifulSoup
import os
import time

cookie = 'd_c0="ADACZvaFTAuPTk6_B7Oa9-lGyhXYHdOzTWk=|1486893952"; _zap=dc0118e7-4538-4c73-980f-243e67e071bb; r_cap_id="YjY5ZGEwZGRiNDFjNDAwZjg5YzZkMTU2ZmVlYTZkZDA=|1499409651|b11d79de017910aff6a53f827d1942fec965cb1a"; cap_id="MjI2YTg4MWMwNWI3NDMwN2FiM2FkZmEyMjEyOWFhOTk=|1499409651|eb7d4b5fd1aba8afdc4e6eda3bc69b730a97841f"; z_c0=Mi4wQUZCQUZRMXp1QWtBTUFKbTlvVk1DeGNBQUFCaEFsVk4tcm1HV1FBOHpRZ1NrVEE4azNWM1FTYVBNZlRfVm5EOHN3|1499409658|db4be12cef042f4cefce8225f946d3ae3ef1efd5; _xsrf=2|fdfe722a|c2c773ab580213415facc5fdd290a8f3|1500736457; q_c1=5811cb06b8284bdf9682e935eb558f3f|1501034874000|1486893952000; aliyungf_tc=AQAAACTAb2gZlgAA1pWePZ4hEnAze66f; __utma=51854390.160129264.1490629456.1501039785.1501045634.47; __utmc=51854390; __utmz=51854390.1501045634.47.19.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/29470294; __utmv=51854390.100-1|2=registration_date=20160404=1^3=entry_date=20160404=1; _xsrf=2a911554-323f-4b53-af68-3045677dcb7a; XSRF-TOKEN=2|9dbc7948|afdd4079ac894c7cb08f4b7bfb914d2aa88f5429fb8a4165ae8c4d7dab8b4e2cfede4e29|1501060607'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.7 Safari/537.36',
           'Cookie': cookie,
           'Connection': 'keep-alive'
           }


def getHtmlText(url):
    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text#返回网页信息
    except:
        exit('登陆失败')

def savePictures():
    urls = input('输入问题链接：')#https://www.zhihu.com/question/49364343
    html_text = getHtmlText(urls)
    soup = BeautifulSoup(html_text,'lxml')#lxml解析网页

    #question和author，打开网页，看所在标签
    question = soup.h1.string.strip()#h1标签文本内容string或text
    for item in range(2):
        info = soup.find_all(name='div', attrs="RichContent-inner")[item]  # 一个question下会显示两位排名靠前的回答
        if item == 1:
            item = 3
        elif item == 0:
            item = 1
        author = str(soup.find_all(name='a', attrs='UserLink-link')[item].text)
        x = info.find_all(name='noscript')  # 这就是所有图片链接所在的标签列表
        links = []
        for i in x:
            link = i.img.attrs['src']  # src属性图片链接
            links.append(link)
        try:
            filename = question + ' - ' + author
            if not os.path.exists(filename):
                os.mkdir(filename)
            for i in range(len(links)):
                img_source = requests.get(links[i]).content  # 获取图片，content主要是获取图片文件bytes二进制信息
                img_path = filename + '/' + str(i) + '.jpg' #+ links[i].split('.')[-1]#(https://pic2.zhimg.com/v2-b9555096455b3f93290e4a538f731311_b.jpg )
                with open(img_path, 'wb') as f:  # 写入图片
                    f.write(img_source)
                    print(links[i], '保存成功')
        except:
            print('error')

start = time.time()
savePictures()
end = time.time()

print('总耗时: ',end-start,'秒')