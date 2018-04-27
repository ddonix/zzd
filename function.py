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
		
		self.func = set()
		desc = desc.split('~')
		for des in desc:
			d,f=des.split(',')
			dset = d[d.find(':')+1:d.find('-')]
			vset = d[d.find('>')+1:]
			fn = f[2:]
			self.func.add((dset,vset,fn))

	def ds(self, sp):
		for f in self.func:
			if sp.be(f[0])[0] == 0:
				return True
		return False
	
	def vs(self, sp):
		for f in self.func:
			if sp.be(f[0])[0] == 0:
				return f[1]
		return None
	
	#取值或者判断真假的函数
	def value_a(self, sp):
		for f in self.func:
			if f[1] == '数' or f[1] == '(True False)':
				if f[2].find('eval(x)') != -1:
					e = f[2].replace('eval(x)','(%s)'%sp.s)
				else:
					e = f[2]
				return eval(e)
		return False
	
	def judge_a(self, sp, desp):
		print('sp.s, desp', sp.s, desp)
		return [2]
	
	def value_A(self, gs):
		return None
