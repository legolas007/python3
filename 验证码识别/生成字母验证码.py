#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/6/0006 10:53
# @Author  : Usher
# @Site    : 
# @File    : 生成字母验证码.py
from PIL import Image,ImageDraw,ImageEnhance,ImageFont,ImageFilter
import random

#随机字母
def rndChar():
    return chr(random.randint(65,90))

#随机颜色
def rndColor():
    return (random.randint(65,255),random.randint(65,255),random.randint(65,255))
    #return (255,255,255)

def rndColor2():
    return (random.randint(32,127),random.randint(32,127),random.randint(32,127))
    #return (0,0,0)

width = 240
height = 60
image = Image.new('RGB',(width,height),(255,255,255))

font = ImageFont.truetype('FZLTKHK--GBK1-0.ttf',40)

draw = ImageDraw.Draw(image)
#填充像素
for x in range(width):
    for y in range(height):
        draw.point((x,y),fill=rndColor())

# 输出文字
for t in range(4):
    draw.text((60*t + 10,10),rndChar(),font=font,fill=rndColor2())

image = image.filter(ImageFilter.DETAIL)
image.save('code.jpg','jpeg')
