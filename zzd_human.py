#!/usr/bin/python3 -B
import zzd_unity
import xlrd
import sqlite3
import sys
import time

class human(zzd_unity.unity):
	def __init__(self, name):
		zzd_unity.unity.__init__(self)
		self.name = name
		self.working = True
		self.master = True
    
	@classmethod
	def init(cls):
		print('human init')

	# master调用
	def input(self, sour, waa):
		if waa == u'再见！' or waa == '拜拜！':
			self.working = False
	
	def output(self, dest, waa):
		dest.input(self, waa)
	
	def work(self):
		while self.working and self.master:
			print('xhh working',time.time())
			time.sleep(1)

def main():
	print('zzd_human')
	human.init()

if __name__ == '__main__':
	main()
