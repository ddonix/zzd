#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wave
import os
from pyaudio import PyAudio,paInt16
from aip import AipSpeech
import subprocess

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

num=['零','一','二','三','四','五','六','七','八','九']  
kin=['十','百','千','万','零']  
  
def sadd(x):  
    x.reverse()  
    if len(x) >= 2:  
        x.insert(1,kin[0])  
        if len(x) >= 4:  
            x.insert(3,kin[1])  
            if len(x) >= 6:  
                x.insert(5,kin[2])  
                if len(x) >= 8:  
                    x.insert(7,kin[3])  
                    if len(x) >= 10:  
                        x.insert(9,kin[0])  
                        if len(x) >= 12:  
                            x.insert(11,kin[1])  
  
    x=fw(x)  
    x=d1(x)  
    x=d2(x)  
    x=dl(x)  
    return x  
      
      
def rankis(i):
    rank=[]
    i=list(str(i))  
    for j in i:  
        i[(i.index(j))]=num[int(j)]  
    i=sadd(i)
    rank.append(i)
    return rank  
  
  
def d1(x):  
    if '零' in x:  
        a=x.index('零')  
        if a==0:  
            del x[0]  
            d1(x)  
        else:  
            if x[a+2] in ['十','百','千','万','零']:  
                if x[a+1] != '万':  
                    del x[a+1]  
                    d1(x)       
    return x  
def d2(x):  
    try:  
        a=x.index('零')  
        if x[a-1] in ['十','百','千','零']:  
            del x[a-1]  
            d2(x[a+1])  
    except:pass  
    return x  
  
def fw(x):  
    if len(x) >= 9:  
        if x[8] == '零':  
            del x[8]  
    return x  
def dl(x):  
    try:  
        if x[0]=='零':  
            del x[0]  
            del1(x)  
    except:pass  
    x.reverse()  
    x=''.join(x)  
    return x  


def txt2voice(txt):
	global client
	try:
		a = int(txt)
		if a:
			rank = rankis(a)
			res = rank[0]
		else:
			res = u'0'
	except:
		res = txt
	
	result = client.synthesis(res, 'zh', 1, {'vol': 5,})
	if not isinstance(result, dict):
		with open('output2.mp3', 'wb') as f:
			f.write(result)
		os.system('play output2.mp3')

def main():
	print('void')
	voiceInit()
	a = subprocess.check_output(["date", "+%H:%M:%S"])
	txt2voice(a)

if __name__ == '__main__':
	main()
