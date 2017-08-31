#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/5/0005 16:53
# @Author  : Usher
# @Site    : 
# @File    : split.py
import os
os.chdir(r'D:\python project\词云\词云分析')
f = open('love.txt','r')
w = f.readlines()
s = []
ff = open('love3.txt','w')

for i in w:
    ww = i.strip('\n').split('    ')
    new_w = ww[1]
    print(new_w)
    ff.write(new_w)
    ff.write('\n')

f.close()
ff.close()