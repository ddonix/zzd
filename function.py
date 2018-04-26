#!/usr/bin/python3 -B
import sqlite3
import copy
import gdata

class func:
	def __init__(self, name, desc):
		assert type(name) == str
		assert name
		assert 'f' in desc
		assert ':' in desc
		assert '->' in desc
		assert not gdata.fnin(name)
		
		self.name = name
		gdata.addfn(self)
		print(desc)
		d,f=desc.split(',')
		print(d,f)
		self.dset = d[d.find(':')+1:d.find('-')]
		self.vset = d[d.find('>')+1:]
		print(self.dset,self.vset)
		self.f = f[5:]
		print(self.f)


	def ds(self, sp):
		return sp.be(self.dset)
	
	def vs(self):
		return self.vset
	
	def value(self, sp):
		res = False
		e = self.f.replace('eval(x)',sp.s)
		res = eval(e)
		return res
