#!/usr/bin/python3 -B
import zzd_unity
import xlrd
import sqlite3
import sys

class human(zzd_unity.unity):
	def __init__(self, name):
		zzd_unity.unity.__init__(self)
		self.name = name
    
	@classmethod
	def init(cls):
		print('human init')
	
	def input(self, sour, waa):
		if waa == u'再见！' or waa == '拜拜！':
			print('sys.exit()')
			sys.exit()
	
	def output(self, dest, waa):
		dest.input(self, waa)

def main():
	print('zzd_human')
	human.init()

if __name__ == '__main__':
	main()
