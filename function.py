#!/usr/bin/python3 -B
import sqlite3
import copy
import gdata

class func:
	def __init__(self, name, define):
		assert type(name) == str
		assert name
		assert not '|' in name
		assert not gdata.fnin(name)
		
		self.name = name
		gdata.addfn(self)
		print(define)

	def ds(self, sp):
		return sp.be('数')
	
	def vs(self):
		return '(True False)'
	
	def value(self, sp):
		res = False
		x = eval(sp.s)
		return x%2==0
