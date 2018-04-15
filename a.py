#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import thread
import time
import os
import sys

player = False
 
# 为线程定义一个函数
def print_time( threadName, delay):
	global player
	count = 0
	while count < 20 or player == True:
		time.sleep(delay)
		count += 1
		print "%s: %s" % ( threadName, time.ctime(time.time()) )
		print player

def play( threadName, delay):
	global player
	player = True
	os.system('mplayer 一瞬间.mp3')
	player = False


# 创建两个线程
try:
	thread.start_new_thread( print_time, ("Thread-1", 2, ) )
	time.sleep(20)
	thread.start_new_thread( play, ("Thread-2", 4, ) )
except:
	print "Error: unable to start thread"
 
while 1:
	pass
