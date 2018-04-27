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
		d,f=desc.split(',')
		self.dset = d[d.find(':')+1:d.find('-')]
		self.vset = d[d.find('>')+1:]
		self.f = f[5:]
		print(self.f)

	def ds(self, sp):
		return sp.be(self.dset)[0] == 0
	
	def vs(self):
		return self.vset
	
	def value(self, sp):
		if self.vset == '数' or self.vset == '(True False)':
			if self.f.find('eval(x)') != -1:
				print(self.vset)
				print(sp.s)
				e = self.f.replace('eval(x)','(%s)'%sp.s)
				return eval(e)
			else:
				return False
		else:
			return None
