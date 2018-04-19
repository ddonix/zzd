#!/usr/bin/python3 -B

import tkinter as tk           # 导入 Tkinter 库
import voice
import db
import os
import sys
import zzd_human
import zzd_zzd
import threading
import signal
import w
from multiprocessing import Process

input_layer1 = None

entry_human = None
entry_zzd = None
	
autoplay = True

root = None
#主进程ident, 小涵涵进程结束后给root进程发消息，让主进程退出.
rootpid = 0

def voicePress(evt):
	os.system('amixer set Master 70%')
	recordthread = threading.Thread(target=voice.start_record, args=())
	recordthread.start()
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
	global autoplay,root
	if root == None:
		return
	
	if form:
		input_layer1.delete(0,'end')
		input_layer1.insert(0, form)
		input_layer1.update()
	
	if waa:
		entry_zzd.delete(0,'end')
		entry_zzd.insert(0, waa)
		entry_zzd.update()
		if autoplay:
			voice.txt2voice(waa)
	return
	
def voicePlay(evt):
	global entry_zzd
	waa = entry_zzd.get()
	voice.txt2voice(waa)

def enterSen(waa):
	for item in waa:
		if not db.database.legal(item):
			zhdShow('对不起，我不认识\"%s\"这个字符。'%item)
			return
	xhh.output(zhd, waa)

def human_entry():
	global entry_human
	waa = entry_human.get()
	if waa == '':
		return
	enterSen(waa)

def return_event(evt):
	human_entry()


def gameoversignal(signum,frame):
	sys.exit()

xhht = None
zhdt = None
webt = None
root = None

def delete_windows():
	global zhd, zhdt, xhh, xhht, webt, webtid
	if zhd:
		zhd.root = False
	if xhh:
		xhh.root = False
	if zhdt:
		zhdt.join()
	if xhht:
		xhht.join()
	print(webt)
	if webt:
		print('os.kill webtread')
		os.kill(webtid, signal.SIGTSTP)
		webt.join()
	sys.exit()
	return

zhd = None
zhd_running = None
class zhdthread(threading.Thread):
	def __init__(self,name):
		super().__init__()
		self.name = name

	def run(self):
		global zhd, zhd_running, root, xhh
		print('zhd_thread start.')
		zhd = zzd_zzd.zzd(show=zhdShow, friend=xhh)
		zhd_running.set()
		zhd.live()
		zhd = None
		print('zhd_thread over.')


xhh = None
xhh_running = None
class xhhthread(threading.Thread):
	def __init__(self,name):
		super().__init__()
		self.name = name

	def run(self):
		global xhh, xhh_running, root, rootpid
		print('xhh_thread start.')
		xhh = zzd_human.human('nobody')
		xhh_running.set()
		xhh.live()
		xhh = None
		print('xhh_thread over.')
		os.kill(rootpid, signal.SIGUSR1)


webtid = 0

def weboversignal(signum,frame):
	print('get SIGTSTP signal.')
	sys.exit()

def webthread_proc(port):
		global webt, webtid, rootpid
		webtid = os.getpid()
		print('web_thread start.tid is %d, rootpid is %d.'%(webtid, rootpid))
		signal.signal(signal.SIGTSTP, weboversignal)
		w.createserver()
		print('web_thread over.')
		webt = None

def main():
	global entry_human, entry_zzd
	global input_layer1
	global entry_human,entry_zzd
	global root, rootpid
	
	root = tk.Tk()
	root.geometry('640x480+20+20')
	root.protocol("WM_DELETE_WINDOW", delete_windows)
	root.bind("<Return>",return_event)
	
	entry_human = tk.Entry(root)
	entry_human.place(x=95, y=40, width=400, height=20)
	input_layer1 = tk.Entry(root)
	input_layer1.place(x=95, y=60, width=400, height=20)
	tk.Label(root,text = "entry_human").place(x=5, y=40, width=90, height=20)
	tk.Label(root,text = "entry_fix").place(x=5, y=60, width=90, height=20)
	
	entry_zzd = tk.Entry(root)
	entry_zzd.place(x=95, y=150, width=400, height=20)
	tk.Label(root,text = "entry_zzd").place(x=5, y=150, width=90, height=20)
	
	tk.Button(root, text = "确定", command = human_entry).place(x=500,y=40, width=60, height=20)
	
	vinputButton = tk.Button(root, text = "按住说话")
	vinputButton.place(x=560,y=40, width=60, height=20)
	vinputButton.bind("<ButtonPress>", voicePress)
	vinputButton.bind("<ButtonRelease>", voiceRelease)
	
	voutButton = tk.Button(root, text = "播放")
	voutButton.place(x=560,y=150, width=60, height=20)
	voutButton.bind("<ButtonPress>", voicePlay)
	entry_human.focus_set()
	
	
	rootpid = os.getpid()
	signal.signal(signal.SIGUSR1, gameoversignal)
	root.after(1000,xhh_zhd_web)
	root.mainloop()

def xhh_zhd_web():
	global root,rootpid
	global xhht, xhh, xhh_running
	global zhdt, zhd, zhd_running
	global webt 
	
	zzd_human.human.init()
	zzd_zzd.zzd.init()
	voice.voiceInit()
	
	xhh_running = threading.Event()
	xhh_running.clear()
	xhht = xhhthread('xhh_thread')
	xhht.start()
	xhh_running.wait()
	assert xhh != None
	
	zhd_running = threading.Event()
	zhd_running.clear()
	zhdt = zhdthread('zhd_thread')
	zhdt.start()
	zhd_running.wait()
	
	webt = Process(target=webthread_proc, args=('8080',))
	webt.start()
	
if __name__ == '__main__':
	main()
