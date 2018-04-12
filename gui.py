#!/usr/bin/python -B
# -*- coding: UTF-8 -*-

import Tkinter as tk           # 导入 Tkinter 库
from PIL import Image
import voice
import thread 
import zzd_human
import zzd_zzd

xhh = None
zhd = None

input_layer0 = None
output_layer0 = None

input_layer1 = None
output_layer1 = None

entry_human = None
entry_zzd = None
	
autoplay = False
voicetrain = False 

def mouse_press_event(evt):
	return

def mouse_release_event(evt):
	return

def mouse_movie_event(evt):
	return

def mouse_press_event_right(evt):
	return
	
def voicePress(evt):
	thread.start_new_thread(voice.start_record, ())
	return

def voiceRelease(evt):
	global entry_human,voicetrain
	
	voice.stop_record()
	waa = voice.voice2txt()
	if waa == None:
		#这里的处置是情况外的，不进行学习.
		zhdShow(u'对不起，没有听清，请重复。')
		return
	entry_human.delete(0,'end')
	entry_human.insert(0, waa)
	
	if not voicetrain:
		enterSen(waa)
	else:
		voicetrain = True

def zhdShow(waa, form=''):
	global autoplay
	if form != '':
		input_layer1.delete(0,'end')
		input_layer1.insert(0, form)
		input_layer1.update()
	
	entry_zzd.delete(0,'end')
	entry_zzd.insert(0, waa)
	entry_zzd.update()
	if autoplay:
		voice.txt2voice(waa)
	
	
def voicePlay(evt):
	global entry_zzd
	waa = entry_zzd.get()
	voice.txt2voice(waa)

def enterSen(waa):
	for item in waa:
		if not item in zzd_human.human.table_vocable:
			zhdShow(u'对不起，我不认识\"%s\"这个字符。'%item)
			return
	xhh.act(zhd, waa)

def return_event(evt):
	global entry_human
	waa = entry_human.get()
	if waa == u'':
		return
	enterSen(waa)

def voiceTrain(evt):
	voicetrain = not voicetrain

def addTrain(evt):
	voicetrain = not voicetrain

def main():
	global xhh,zhd
	global entry_human, entry_zzd
	
	global input_layer1,output_layer1
	global entry_human,entry_zzd
	global autoplay

	autoplay = True
	zzd_human.human.init()
	zzd_zzd.zzd.init()
	
	xhh = zzd_human.human(u'nobody')
	zhd = zzd_zzd.zzd(show=zhdShow)
	
	voice.voiceInit()
	
	master = tk.Tk()
	master.geometry('640x480+20+20')
	
	master.bind("<ButtonPress-1>",mouse_press_event)
	master.bind("<ButtonRelease-1>",mouse_release_event)
	master.bind("<Motion>",mouse_movie_event)
	master.bind("<ButtonPress-3>",mouse_press_event_right)
	master.bind("<Return>",return_event)
	
	entry_human = tk.Entry(master)
	entry_human.place(x=95, y=40, width=400, height=20)
	input_layer1 = tk.Entry(master)
	input_layer1.place(x=95, y=60, width=400, height=20)
	input_layer0 = tk.Entry(master)
	input_layer0.place(x=95, y=80, width=400, height=20)
	tk.Label(master,text = "entry_human").place(x=5, y=40, width=90, height=20)
	tk.Label(master,text = "input_layer1").place(x=5, y=60, width=90, height=20)
	tk.Label(master,text = "input_layer0").place(x=5, y=80, width=90, height=20)
	
	output_layer0 = tk.Entry(master)
	output_layer0.place(x=95, y=110, width=400, height=20)
	output_layer1 = tk.Entry(master)
	output_layer1.place(x=95, y=130, width=400, height=20)
	entry_zzd = tk.Entry(master)
	entry_zzd.place(x=95, y=150, width=400, height=20)
	tk.Label(master,text = "output_layer0").place(x=5, y=110, width=90, height=20)
	tk.Label(master,text = "output_layer1").place(x=5, y=130, width=90, height=20)
	tk.Label(master,text = "entry_zzd").place(x=5, y=150, width=90, height=20)
	
	tk.Button(master, text = "确定", command = enterSen).place(x=500,y=40, width=60, height=20)
	
	vinputButton = tk.Button(master, text = "按住说话")
	vinputButton.place(x=560,y=40, width=60, height=20)
	vinputButton.bind("<ButtonPress>", voicePress)
	vinputButton.bind("<ButtonRelease>", voiceRelease)
	
	vinputButton = tk.Button(master, text = "加入训练")
	vinputButton.place(x=500,y=80, width=80, height=20)
	vinputButton.bind("<ButtonPress>", addTrain)
	vinputButton = tk.Button(master, text = "设置/取消识别")
	vinputButton.place(x=560,y=60, width=80, height=20)
	vinputButton.bind("<ButtonPress>", voiceTrain)
	
	voutButton = tk.Button(master, text = "播放")
	voutButton.place(x=560,y=150, width=60, height=20)
	voutButton.bind("<ButtonPress>", voicePlay)

	entry_human.focus_set()
	master.mainloop()

if __name__ == '__main__':
	main()
