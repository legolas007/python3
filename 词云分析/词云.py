#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/1/0001 11:39
# @Author  : Usher
# @Site    :

import jieba.analyse
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import os
import PIL.Image as Image
import numpy as np

with open('love.txt','r',encoding='gbk') as f:
    text = f.read()
    f.close()
cut_text = " ".join(jieba.cut(text))  #使用空格连接 进行中文分词
cut_an= jieba.analyse.extract_tags(cut_text,50)  # 关键词提取,返回权重最高的前30，数字可以不填默认20

d = os.path.dirname(__file__) # 获取当前文件路径
color_mask = np.array(Image.open(os.path.join(d,'img.jpg')))   # 设置图片
cloud = WordCloud(
    background_color='#F0F8FF',      # 参数为设置背景颜色,默认颜色则为黑色
    font_path="FZLTKHK--GBK1-0.ttf", # 使用指定字体可以显示中文，或者修改wordcloud.py文件字体设置并且放入相应字体文件
    max_words=30000,  # 词云显示的最大词数
    font_step= 1,    # 步调太大，显示的词语就少了
    mask=color_mask,  #设置背景图片
    random_state= 20, # 设置有多少种随机生成状态，即有多少种配色方案
    min_font_size=15,  #字体最小值
    max_font_size=200, #字体最大值
    )
cloud.generate(cut_text)  #对分词后的文本生成词云
image_colors = ImageColorGenerator(color_mask)  # 从背景图片生成颜色值
plt.show(cloud.recolor(color_func=image_colors))  # 绘制时用背景图片做为颜色的图片
plt.imshow(cloud)            # 以图片的形式显示词云
plt.axis('off')                     # 关闭坐标轴
plt.show()                          # 展示图片

cloud.to_file(os.path.join(d, 'pic.jpg'))  # 图片大小将会按照 mask 保存
