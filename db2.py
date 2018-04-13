#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import re
import xlrd
import copy
import sqlite3

class database:
	_gset_all = {}
	_spbase_all = {}
	_table_vocable = {u' '}
	_identifyDict = {}
	_defineDict = {}
	_keyword_zzd = {}
	
	@classmethod
	def gs(cls, gram):
		try:
			return cls._gset_all[gram]
		except:
			raise NameError

	@classmethod
	def sp(cls, s):
		try:
			return cls._spbase_all[s[0]][s]
		except:
			raise NameError
	
	@classmethod
	def gsin(cls, gs):
		if gs in cls._gset_all:
			return True
		return False
	
	@classmethod
	def spin(cls, sp):
		if sp[0] in cls._spbase_all:
			if sp in cls._spbase_all[sp[0]]:
				return True
		return False
	
	@classmethod
	def legal(cls, s):
		for v in s:
			if not v in cls._table_vocable:
				print '%s中有非法字符%s',%(s,v)
				return False
		return True
	
	@classmethod
	def addgs(cls, gs):
		assert isinstance(gs, gset)
		cls._spbase_all[gs.name] = gs

	@classmethod
	def addsp(cls, sp):
		assert isinstance(sp, sentencephrase)
		assert len(sp.s) >= 1
		if len(sp.s) == 1:
			cls._spbase_all[sp.s[0]] = {sp.s:sp}
		else:
			cls._spbase_all[sp.s[0]][sp.s] = sp
	
	@classmethod
	def addv(cls, s):
		for v in s:
			cls._table_vocable.add(v)

	@classmethod
	def spinit():
		try:
			conn = sqlite3.connect('./data/grammar.db')
			cursor = conn.execute("select * from table_vocable")
		except:
			raise NameError
		for v in cursor:
			assert len(v[0]) == 1
			sp = sentencephrase(v[0])
			database.addsp(sp)
			database.addv(v[0][0])
			
			for g in v[1:]:
				gs = database.gs(g)
				gs.addsp(sp)
		
		try:
			cursor = conn.execute("select * from table_phrase")
		except:
			raise NameError
		for v in cursor:
			assert len(v[0]) > 1
			if not database.legal(v):
				raise NameError
			sp = sentencephrase(v)
			database.addsp(sp)
			
			for g in v[1:]:
				gs = database.gs(g)
				gs.addsp(sp)
		conn.close()

	
class gset:
	def __init__(self, name, child):
		self.name = unicode(name)

class sentencephrase:
	def __init__(self, s):
		self.s = s
		self.d = [s]
		self.key = {}

def main():
	print('db')
	print database.gs(u'名词')
	print database.sp(u'1')

if __name__ == '__main__':
	main()
