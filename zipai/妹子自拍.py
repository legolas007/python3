#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/6/0006 18:15
# @Author  : Usher
# @Site    : 
# @File    :妹子自拍.py
import os
from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.7 Safari/537.36'}

def savePics(num):
    path = r'D:\mzitu'
    filename = '妹子自拍'
    filepath = path + '/' + filename
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    i = 0
    for page in range(num,0,-1):
        zipai_url = 'http://www.mzitu.com/zipai/comment-page-{page}/#comments'.format(page=page)
        start_html = requests.get(zipai_url,headers).text
        soup = BeautifulSoup(start_html,'lxml')
        all_li = soup.find_all('ul')[1]
        all_url = all_li.find_all(name='li')
        for a in all_url:
            i += 1
            imgurl = a.img.attrs['src']
            imgsource = requests.get(imgurl,headers=headers).content
            name = imgurl[-9:-4]
            img_path = filepath + '/' + name + '.jpg'
            with open(img_path,'wb') as f:
                f.write(imgsource)
                print(imgurl,'保存成功')

        if i >= 18:
            break

    print('共抓取%d张自拍'% i)

savePics(307)