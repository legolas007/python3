#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/28/0028 19:21
# @Author  : Usher
# @Site    : 
# @File    : 基于图灵机的QQ聊天机器人.py
from qqbot import QQBotSlot, RunBot
import requests


KEY = 'f75b599f42f947988d117823c1f5fd02'

# 向api发送请求
def get_response(msg):
  apiUrl = 'http://www.tuling123.com/openapi/api'
  data = {
    'key'  : KEY,
    'info'  : msg,
    'userid' : 'pth-robot',
  }
  try:
    r = requests.post(apiUrl, data=data).json()
    return r.get('text')
  except:
    return

@QQBotSlot
def onQQMessage(bot,contact,member,content):
    if getattr(member,'uin',None) == bot.conf.qq:
        pass
    elif content == '下线':
        bot.SendTo(contact,'再见喽')
        bot.Stop()
    elif '@ME' in content:
        response = get_response(content)
        bot.SendTo(contact, response)
    else:
        pass



if __name__ == '__main__':
    RunBot()