#!/usr/bin/python3 -B
import xlrd
import sqlite3
import sys
import time

#output函数运行在root主进程
#input函数运行在zhd线程
#其他函数运行在xhh线程.
class human():
	def __init__(self, name):
		self.name = name
		self.working = True
		self.root = True
    
	@classmethod
	def init(cls):
		print('human init')

	#运行在zhd线程
	def input(self, sour, waa):
		if waa == u'再见！' or waa == '拜拜！':
			self.working = False
		else:
			pass			#这里体现人不理会机器的反应
	
	#运行在root主进程
	def output(self, dest, waa):
		dest.input(self, waa)
	
	def live(self):
		while self.working and self.root:
			print('xhh working',time.time())
			time.sleep(1)

def main():
	print('zzd_human')
	human.init()

if __name__ == '__main__':
	main()
