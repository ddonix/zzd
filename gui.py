#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Tkinter as tk           # 导入 Tkinter 库
from PIL import Image
import zzd_layer1

corelayer1 = None

input_layer1 = None
output_layer1 = None

def mouse_press_event(evt):
	return

def mouse_release_event(evt):
	return

def mouse_movie_event(evt):
	return

def mouse_press_event_right(evt):
	return

def return_event(evt):
	global input_layer1,output_layer1
	output_layer1.delete(0,'end')
	sen = input_layer1.get()
	out = corelayer1.inputs(sen)
	output_layer1.insert(0, out)

def main():
	global corelayer1
	global input_layer1,output_layer1
	
	corelayer1 = zzd_layer1.zzdLayer1()

	master = tk.Tk()
	master.geometry('640x480+20+20')
	
	master.bind("<ButtonPress-1>",mouse_press_event)
	master.bind("<ButtonRelease-1>",mouse_release_event)
	master.bind("<Motion>",mouse_movie_event)
	master.bind("<ButtonPress-3>",mouse_press_event_right)
	master.bind("<Return>",return_event)
	
	input_layer1 = tk.Entry(master)
	input_layer1.place(x=5, y=40, width=400, height=20)
	output_layer1 = tk.Entry(master)
	output_layer1.place(x=5, y=60, width=400, height=20)

	master.mainloop()

if __name__ == '__main__':
	main()
