#!/usr/bin/python3 -B

import tkinter as tk           # 导入 Tkinter 库
from PIL import Image
import voice
import _thread 
import db
import os
import zzd_human
import zzd_zzd
import time 

xhh = None
zhd = None


input_layer1 = None
output_layer1 = None

entry_human = None
entry_zzd = None
	
autoplay = False

def voicePress(evt):
	os.system('amixer set Master 70%')
	thread.start_new_thread(voice.start_record, ())
	return

def voiceRelease(evt):
	global entry_human
	os.system('amixer set Master 100%')
	voice.stop_record()
	waa = voice.voice2txt()
	if waa == None:
		#这里的处置是情况外的，不进行学习.
		zhdShow('对不起，没有听清，请重复。')
		return
	entry_human.delete(0,'end')
	entry_human.insert(0, waa)
	enterSen(waa)

def zhdShow(waa, form=''):
	global autoplay
	
	input_layer1.delete(0,'end')
	if form != '':
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
		if not db.database.legal(item):
			zhdShow('对不起，我不认识\"%s\"这个字符。'%item)
			return
	xhh.act(zhd, waa)

def human_entry():
	global entry_human
	waa = entry_human.get()
	if waa == '':
		return
	enterSen(waa)

def return_event(evt):
	human_entry()

def main():
	global xhh,zhd
	global entry_human, entry_zzd
	
	global input_layer1,output_layer1
	global entry_human,entry_zzd
	global autoplay

	zzd_human.human.init()
	zzd_zzd.zzd.init()
	
	xhh = zzd_human.human('nobody')
	zhd = zzd_zzd.zzd(show=zhdShow)
	
	voice.voiceInit()
	
	master = tk.Tk()
	master.geometry('640x480+20+20')
	
	master.bind("<Return>",return_event)
	
	entry_human = tk.Entry(master)
	entry_human.place(x=95, y=40, width=400, height=20)
	input_layer1 = tk.Entry(master)
	input_layer1.place(x=95, y=60, width=400, height=20)
	tk.Label(master,text = "entry_human").place(x=5, y=40, width=90, height=20)
	tk.Label(master,text = "input_layer1").place(x=5, y=60, width=90, height=20)
	
	output_layer1 = tk.Entry(master)
	output_layer1.place(x=95, y=130, width=400, height=20)
	entry_zzd = tk.Entry(master)
	entry_zzd.place(x=95, y=150, width=400, height=20)
	tk.Label(master,text = "output_layer1").place(x=5, y=130, width=90, height=20)
	tk.Label(master,text = "entry_zzd").place(x=5, y=150, width=90, height=20)
	
	tk.Button(master, text = "确定", command = human_entry).place(x=500,y=40, width=60, height=20)
	
	vinputButton = tk.Button(master, text = "按住说话")
	vinputButton.place(x=560,y=40, width=60, height=20)
	vinputButton.bind("<ButtonPress>", voicePress)
	vinputButton.bind("<ButtonRelease>", voiceRelease)
	
	voutButton = tk.Button(master, text = "播放")
	voutButton.place(x=560,y=150, width=60, height=20)
	voutButton.bind("<ButtonPress>", voicePlay)

	entry_human.focus_set()
	master.mainloop()

if __name__ == '__main__':
	main()
