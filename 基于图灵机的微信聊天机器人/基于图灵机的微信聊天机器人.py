#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/31/0031 19:27
# @Author  : Usher
# @Site    : 
# @File    : 基于图灵机的微信聊天机器人.py

import requests
import itchat
from itchat.content import *

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
# 注册方法
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    # 默认回复
    defaultReply = 'I received: ' + msg['Text']
    reply = get_response(msg['Text'])
    if u'下线' in msg['Text']:
        itchat.send(u'再见喽',msg['FromUserName'])
        itchat.logout()
    return reply or defaultReply

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        reply = get_response(msg['Text'])
        itchat.send(u'@%s\u2005 %s' % (msg['ActualNickName'], reply), msg['FromUserName'])


itchat.auto_login(hotReload=True)#hotReload=True热启动
itchat.run()