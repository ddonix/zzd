#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Tkinter as tk           # 导入 Tkinter 库
from PIL import Image
import zzd_layer0
import zzd_layer1
import zzd_layer2

corelayer0 = None
corelayer1 = None
corelayer2 = None

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

def return_event(evt):
	global input_layer2,output_layer2
	output_layer2.delete(0,'end')
	sen = input_layer2.get()
	out = corelayer2.inputs(sen)
	output_layer2.insert(0, out)

def main():
	global corelayer0,corelayer1,corelayer2
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
	input_layer2.place(x=5, y=40, width=400, height=20)
	output_layer2 = tk.Entry(master)
	output_layer2.place(x=5, y=60, width=400, height=20)

	master.mainloop()

if __name__ == '__main__':
	main()
