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
				print u'%s中有非法字符%s'%(s,v)
				return False
		return True
	
	@classmethod
	def addgs(cls, gs):
		assert isinstance(gs, gset)
		cls._gset_all[gs.name] = gs

	@classmethod
	def addsp(cls, sp):
		assert isinstance(sp, seph)
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
	def gsinit(cls):
		try:
			conn = sqlite3.connect('./data/grammar.db')
			cursor = conn.execute("select * from gset_phrase")
			v = cursor.fetchall()
			cursor = conn.execute("select * from gset_sentence")
			v.extend(cursor.fetchall())
			conn.close()
		except:
			return NameError
		while v != []:
			if cls.gsin(v[0][0]):
				v.pop(0)
				continue
			skip = True
			for g in v[0][1:]:
				if g == '' or g == None or cls.gsin(g):
					continue
				if not (g[0] == u'[' and g[-1] == u']'):
					break
				if not u'|' in g:
					gsp = g[1:-1].split(u' ')
					skip2 = True
					for gg in gsp:
						if gg == '' or gg == u'...' or cls.gsin(gg):
							continue
						if gg[0] == u'w' and cls.gsin(gg[1:]):
							continue
						if gg[0] == u's' or gg[0:2] == u'ws':
							continue
						print u'%s:  依赖： %s'%(v[0][0],gg)
						break
					else:
						skip2 = False
					if skip2:
						break
				else:
					gsp = g[1:-1].split('|')
					skip2 = True
					for gg in gsp[1:]:
						if not (gg == '' or cls.gsin(gg)):
							break
					else:
						skip2 = False
					if skip2:
						break
			else:
				gset(v[0][0], v[0][1:])
				v.pop(0)
				skip = False
			if skip:
				tmp = v.pop(0)
				v.append(tmp)

	@classmethod
	def spinit(cls):
		try:
			conn = sqlite3.connect('./data/grammar.db')
			cursor = conn.execute("select * from table_vocable")
		except:
			raise NameError
		for v in cursor:
			assert len(v[0]) == 1
			sp = seph(v[0])
			database.addsp(sp)
			database.addv(v[0][0])
			
			for g in v[1:]:
				if not (g == '' or g == None):
					database.gs(g).addsp(sp)
		
		try:
			cursor = conn.execute("select * from table_phrase")
		except:
			raise NameError
		for v in cursor:
			assert len(v[0]) > 1
			if not database.legal(v[0]):
				raise NameError
			sp = seph(v)
			database.addsp(sp)
			
			for g in v[1:]:
				if not (g == '' or g == None):
					database.gs(g).addsp(sp)
		conn.close()

	def coreinit(cls):
		try:
			conn = sqlite3.connect('./data/grammar.db')
			cursor = conn.execute("select * from define")
		except:
			raise NameError
		
		for define in cursor:
			if not database.legal(define[0]):
				raise TypeError
			if not database.legal(define[1]):
				raise TypeError
			cls._defineDict[define[0]] = define[1]

		try:
			cursor = conn.execute("select * from zzd_keyword")
		except:
			raise NameError
		for keyword in cursor:
			if not cls.spin(keyword[0]):
				raise TypeError
			cls._keyword_zzd[keyword[0]] = keyword[1:]
	
		for sp in cls.gs(u'zzd关键字').sp:
			if not sp in keyword_zzd:
				print '在符号表中定义为zzd关键字，但是没有在关键字表中出现',s
				raise NameError

		cursor = conn.execute("select * from verify")
		for guest in cursor:
			identifyDict[guest[0]] = guest[1]
		conn.close()

class gset:
	def __init__(self, name, child):
		self.name = unicode(name)
		database.addgs(self)
		
		self.sp = set()		#明确表示的元素集合
		self.plot = {}		#明确的划分;要有名字：比如人按性别分为男人和女人

		self.child = []		#子集
		for ch in child:
			if ch == u'' or ch == None:
				continue
			if database.gsin(ch):
				ch = database.gs(ch)
				self.child.append(ch)
			else:
				assert ch[0] == u'[' and ch[-1] == u']'
				if not u'|' in ch:
					ch = gset(ch, [])
					self.child.append(ch)
				else:
					plots = ch[1:-1].split(u'|')
					plot = set()
					for p in plots[1:]:
						assert database.gsin(p)
						plot.add(database.gs(p))
						self.child.append(database.gs(p))
					self.plot[plots[0]]=plot
	
	def addsp(self, sp):
		if isinstance(sp, seph):
			self.sp.add(sp)
		else:
			raise TypeError
	

class seph:
	def __init__(self, arg):
		try:
			self.s = arg[0]			#string
			self.d = (arg[0])		#迪卡尔
		except:
			raise TypeError

def main():
	print('db')
	print database.gsinit()
	print database.spinit()

if __name__ == '__main__':
	main()
