#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import zzd_unity
import xlrd
import sqlite3

class human(zzd_unity.unity):
	table_vocable = set()
	def __init__(self, name):
		zzd_unity.unity.__init__(self)
		self.waalist = []
		self.name = name
    
	@classmethod
	def init(cls):
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.execute("select name from table_vocable")
		for v in cursor:
			assert len(v[0]) == 1
			human.table_vocable.add(v[0])
		conn.close()
	
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
