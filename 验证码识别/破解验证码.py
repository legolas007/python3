#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/6/0006 12:06
# @Author  : Usher
# @Site    : 
# @File    : 破解验证码.py
from PIL import Image
import pytesseract

def crack_code():
    image = Image.open(r'code.jpg')
    image = image.convert("L")
    #image.show()
    threshold = 108
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    # 通过查找表或函数映射此图像,只有当源图像具有“L”或“P”模式，输出模式为“1”或源图像模式为“I”，输出模式为“L”时，才能使用
    out = image.point(table, '1')
    out.save(r'crack_code.png', 'png')
    img = Image.open(r'crack_code.png')
    print(pytesseract.image_to_string(img))

crack_code()

