import os
import requests
from lxml import html

cookie = 'd_c0="ADACZvaFTAuPTk6_B7Oa9-lGyhXYHdOzTWk=|1486893952"; _zap=dc0118e7-4538-4c73-980f-243e67e071bb; r_cap_id="YjY5ZGEwZGRiNDFjNDAwZjg5YzZkMTU2ZmVlYTZkZDA=|1499409651|b11d79de017910aff6a53f827d1942fec965cb1a"; cap_id="MjI2YTg4MWMwNWI3NDMwN2FiM2FkZmEyMjEyOWFhOTk=|1499409651|eb7d4b5fd1aba8afdc4e6eda3bc69b730a97841f"; z_c0=Mi4wQUZCQUZRMXp1QWtBTUFKbTlvVk1DeGNBQUFCaEFsVk4tcm1HV1FBOHpRZ1NrVEE4azNWM1FTYVBNZlRfVm5EOHN3|1499409658|db4be12cef042f4cefce8225f946d3ae3ef1efd5; _xsrf=2|fdfe722a|c2c773ab580213415facc5fdd290a8f3|1500736457; q_c1=5811cb06b8284bdf9682e935eb558f3f|1501034874000|1486893952000; aliyungf_tc=AQAAACTAb2gZlgAA1pWePZ4hEnAze66f; __utma=51854390.160129264.1490629456.1501039785.1501045634.47; __utmc=51854390; __utmz=51854390.1501045634.47.19.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/29470294; __utmv=51854390.100-1|2=registration_date=20160404=1^3=entry_date=20160404=1; _xsrf=2a911554-323f-4b53-af68-3045677dcb7a; XSRF-TOKEN=2|9dbc7948|afdd4079ac894c7cb08f4b7bfb914d2aa88f5429fb8a4165ae8c4d7dab8b4e2cfede4e29|1501060607'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.7 Safari/537.36',
           'Cookie': cookie,
           'Host':'www.zhihu.com',
           'Connection':'keep-alive'}

def getLinkList(num):
    page = input('输入你要抓取的页数：')
    results = []
    title = None
    for i in range(1,int(page)+1):
        link = 'https://www.zhihu.com/collection/{}?page={}'.format(num,i)
        response = requests.get(link,headers=headers).text
        #解析html
        dom = html.fromstring(response)
        #创建title
        if title is None:
            #//从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置,//title[@lang=’eng’]选取所有 title 元素，且这些元素拥有值为 eng 的 lang 属性。//text()本节点和子节点所有文本信息
            title = dom.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()')[0].strip()
            if not os.path.exists(title):
                os.mkdir(title)
        links = dom.xpath('//div[@class="zm-item"]//div[@class="zm-item-answer "]/link')#所有link元素
        for li in links:
            link = 'https://www.zhihu.com' + li.xpath('@href')[0]
            print(link)
            results.append(link)
    return [title,results]

def saveImages(collection,answerLink):
    response = requests.get(answerLink,headers=headers).text
    dom = html.fromstring(response)
    title = dom.xpath('//h1[@class="QuestionHeader-title"]/text()')[0].strip()
    try:
        author = dom.xpath('//a[@class="UserLink-link"]/text()')[0].strip()
    except:
        author=u'匿名'
    #子文件夹
    path = collection + '/' + title + '-' + author
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        n = 1
        for i in dom.xpath('//div[@class="RichContent-inner"]//img/@src'):
            if 'whitedot' not in i:#去除whitedot链接
                img = requests.get(i).content
                fname = path + '/' + str(n) + '.jpg'
                with open(fname,'wb') as f:
                    f.write(img)
                n += 1
        print(u'%s完成' % title)
    except:
        pass

if __name__ == '__main__':
    num = input('输入收藏夹号码：')
    r = getLinkList(num)
    collection = r[0]#title
    collectionList = r[1]#回答链接列表
    for k in collectionList:
        saveImages(collection,k)