#!/usr/bin/python3 -B
import sqlite3
import copy
import gdata

_fns_all = {}
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
			if vset[0] == '(' and vset[-1] == ')':
				if dset not in _fns_all:
					_fns_all[dset]={}
				_fns_all[dset][self.name]={}
				for v in vset[1:-1].split(' '):
					_fns_all[dset][self.name][v]=v
					_fns_all[dset][self.name]['%s的'%v]=v
					_fns_all[dset][self.name]['%s性'%v]=v
					_fns_all[dset][self.name]['%s类'%v]=v
					_fns_all[dset][self.name]['%s%s'%(v,dset)]=v
					_fns_all[dset][self.name]['%s的%s'%(v,dset)]=v
					_fns_all[dset][self.name]['%s%s的%s'%(self.name, v,dset)]=v
					_fns_all[dset][self.name]['%s是%s的%s'%(self.name, v,dset)]=v
					_fns_all[dset][self.name]['%s为%s的%s'%(self.name, v,dset)]=v
					print(_fns_all)
				
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
			if sp.be(f[0])[0] != 0:
				continue
			if f[1] == '数' or f[1] == 'bool':
				if f[2].find('eval(x)') != -1:
					e = f[2].replace('eval(x)','(%s)'%sp.s)
				else:
					e = f[2]
				return eval(e)
		return None
	
	def affirm_a(self, sp, desp):
		print('sp.s, desp', sp.s, desp)
		for f in self.func:
			if sp.be(f[0])[0] != 0:
				continue
			if f[1][0] != '(' or f[1][-1] != ')':
				continue
			if not f[2]:	#没有推理
				return [2,'现在还不会推理']
			else:			#有推理
				return [2,'现在还不会推理']
		return [2,'%s是未知的词'%desp]
	
	def judge_a(self, sp, desp):
		print('sp.s, desp', sp.s, desp)
		print('sp.s, desp', sp.s, desp)
		for f in self.func:
			if sp.be(f[0])[0] != 0:
				continue
			if f[1][0] != '(' or f[1][-1] != ')':
				continue
			if not f[2]:	#没有推理
				if desp in _fns_all[f[0]][self.name]:
					if self.name not in sp.fn:
						return (2,'%s的%s未知。'%(sp.s,self.name))
					else:
						if sp.fn[self.name] == _fns_all[f[0]][self.name][desp]:
							return (0,[],{self.name:sp.fn[self.name]})
						else:
							return (1,'%s的%s是%s'%(sp.s,self.name,sp.fn[self.name]))
				else:
					return (2,'%s是未知的词'%desp)
			else:			#有推理
				return (2,'现在还不会推理')
		for fns in _fns_all:
			for cls in _fns_all[fns]:
				#print(_fns_all[fns][cls])
				pass
		return (2,'%s是fffff未知的词'%desp)
	
	def value_A(self, gs):
		return None
