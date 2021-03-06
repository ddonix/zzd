#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wave
import os
from pyaudio import PyAudio,paInt16
from aip import AipSpeech

recordflag = False
stoped = False

framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2
my_buf = []

#save the date to the wavfile
def save_wave_file(filename,data):
	wf=open(filename,'wb')
	wf.write(b"".join(data))
	wf.close()

def start_record():
	global recordflag,stoped, my_buf
	pa=PyAudio()
	stream=pa.open(format = paInt16,channels=1, rate=framerate,input=True, frames_per_buffer=NUM_SAMPLES)
	my_buf=[]
	recordflag = True
	stoped = False
	while recordflag:
		string_audio_data = stream.read(NUM_SAMPLES)
		my_buf.append(string_audio_data)
		print('.')
	stoped = True

def stop_record():
	global recordflag,stoped
	recordflag = False
	while not stoped:
		save_wave_file('input2.pcm',my_buf)

""" 你的 APPID AK SK """
APP_ID = '11025174'
API_KEY = 'AVn9EvSNIMvLzF7Uaf309nkM'
SECRET_KEY = 'GVbbscDlDlGREoWTib5Om1q6WPFlEGpm'
	
client = None

# 读取文件

def voiceInit():
	global client
	client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
	
def get_file_content(filePath):
	with open(filePath, 'rb') as fp:
		return fp.read()

# 识别本地文件
def voice2txt():
	global client
	res = client.asr(get_file_content('input2.pcm'), 'pcm', 16000, {'dev_pid': '1536',})
	txt = res.get(u'result')
	if txt != None:
		return txt[0]
	else:
		return None

def txt2voice(txt):
	global client
	result = client.synthesis(txt, 'zh', 1, {'vol': 5,})
	if not isinstance(result, dict):
		with open('output2.mp3', 'wb') as f:
			f.write(result)
		os.system('mplayer output2.mp3')
