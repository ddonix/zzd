#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import zzd_unity
import xlrd
import sqlite3

class human(zzd_unity.unity):
	def __init__(self, name):
		zzd_unity.unity.__init__(self)
		self.waalist = []
		self.name = name
    
	@classmethod
	def init(cls):
		print 'human init'

	def act(self, dest, waa_out):
		res = dest.echo(self, waa_out)
		self.waalist.append([waa_out, res])
		return None
	
	def echo(self, sour, waa_in):
		raise NotImplementedError
    
	def forword(self, dest, waa_out):
		return waa_out

def main():
	print('zzd_human')
	human.init()

if __name__ == '__main__':
	main()
