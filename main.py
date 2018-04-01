#!/usr/bin/python
# -*- coding: UTF-8 -*-
from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '11025174'
API_KEY = 'AVn9EvSNIMvLzF7Uaf309nkM'
SECRET_KEY = 'GVbbscDlDlGREoWTib5Om1q6WPFlEGpm'

# 读取文件
def get_file_content(filePath):
	with open(filePath, 'rb') as fp:
		return fp.read()

# 识别本地文件
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
res = client.asr(get_file_content('output.pcm'), 'pcm', 16000, {'dev_pid': '1536',})
print res.get(u'result')[0]
result = client.synthesis(u'1+1等于2', 'zh', 1, {'vol': 5,})
if not isinstance(result, dict):
	with open('auido.mp3', 'wb') as f:
		f.write(result)
