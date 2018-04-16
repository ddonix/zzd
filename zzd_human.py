#!/usr/bin/python3 -B
import zzd_unity
import xlrd
import sqlite3

class human(zzd_unity.unity):
	def __init__(self, name):
		zzd_unity.unity.__init__(self)
		self.name = name
    
	@classmethod
	def init(cls):
		print('human init')
	
	def input(self, sour, waa):
		raise NotImplementedError
	
	def output(self, dest, waa):
		dest.input(self, waa)
		return None

def main():
	print('zzd_human')
	human.init()

if __name__ == '__main__':
	main()
