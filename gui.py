#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Tkinter as tk           # 导入 Tkinter 库
from PIL import Image
import zzd_layer0
import zzd_layer1
import zzd_layer2
import voice
import thread 

corelayer0 = None
corelayer1 = None
corelayer2 = None

input_layer0 = None
output_layer0 = None

input_layer1 = None
output_layer1 = None

input_layer2 = None
output_layer2 = None


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
	global input_layer2,output_layer2
	voice.stop_record()
	
	input_layer2.delete(0,'end')
	output_layer2.delete(0,'end')
	sen = voice.voice2txt()
	
	input_layer2.insert(0, sen)
	out = corelayer2.inputs(sen)
	output_layer2.insert(0, out)

def return_event(evt):
	enterSen()
	return

def enterSen():
	global input_layer2,output_layer2
	output_layer2.delete(0,'end')
	sen = input_layer2.get()
	out = corelayer2.inputs(sen)
	output_layer2.insert(0, out)

def return_event(evt):
	enterSen()

def main():
	global corelayer0,corelayer1,corelayer2
	global input_layer1,output_layer1
	global input_layer2,output_layer2
	
	corelayer0 = zzd_layer0.zzdLayer0()
	corelayer1 = zzd_layer1.zzdLayer1(corelayer0)
	corelayer2 = zzd_layer2.zzdLayer2(corelayer1)

	master = tk.Tk()
	master.geometry('640x480+20+20')
	
	master.bind("<ButtonPress-1>",mouse_press_event)
	master.bind("<ButtonRelease-1>",mouse_release_event)
	master.bind("<Motion>",mouse_movie_event)
	master.bind("<ButtonPress-3>",mouse_press_event_right)
	master.bind("<Return>",return_event)
	
	
	input_layer2 = tk.Entry(master)
	input_layer2.place(x=95, y=40, width=400, height=20)
	input_layer1 = tk.Entry(master)
	input_layer1.place(x=95, y=60, width=400, height=20)
	input_layer0 = tk.Entry(master)
	input_layer0.place(x=95, y=80, width=400, height=20)
	tk.Label(master,text = "input_layer2").place(x=5, y=40, width=90, height=20)
	tk.Label(master,text = "input_layer1").place(x=5, y=60, width=90, height=20)
	tk.Label(master,text = "input_layer0").place(x=5, y=80, width=90, height=20)
	
	output_layer0 = tk.Entry(master)
	output_layer0.place(x=95, y=110, width=400, height=20)
	output_layer1 = tk.Entry(master)
	output_layer1.place(x=95, y=130, width=400, height=20)
	output_layer2 = tk.Entry(master)
	output_layer2.place(x=95, y=150, width=400, height=20)
	tk.Label(master,text = "output_layer0").place(x=5, y=110, width=90, height=20)
	tk.Label(master,text = "output_layer1").place(x=5, y=130, width=90, height=20)
	tk.Label(master,text = "output_layer2").place(x=5, y=150, width=90, height=20)
	
	tk.Button(master, text = "确定", command = enterSen).place(x=500,y=40, width=60, height=20)
	
	vbotton = tk.Button(master, text = "语音")
	vbotton.place(x=560,y=40, width=60, height=20)
	vbotton.bind("<ButtonPress>", voicePress)
	vbotton.bind("<ButtonRelease>", voiceRelease)
	input_layer2.focus_set()
	
	master.mainloop()

if __name__ == '__main__':
	main()
