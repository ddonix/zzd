#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import re
import xlrd
import copy
import sqlite3
import ipdb

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
			ipdb.set_trace()
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
			sp = seph(v[0])
			database.addsp(sp)
			
			for g in v[1:]:
				if not (g == '' or g == None):
					database.gs(g).addsp(sp)
		conn.close()

	@classmethod
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
				print keyword[0]
				raise TypeError
			cls._keyword_zzd[keyword[0]] = keyword[1:]
	
		for sp in cls.gs(u'zzd关键字').sp:
			if not sp.s in cls._keyword_zzd:
				print('%s在符号表中定义为zzd关键字，但是没有在关键字表中出现'%sp)
				raise NameError

		try:
			cursor = conn.execute("select * from verify")
		except:
			raise TypeError
		for guest in cursor:
			cls._identifyDict[guest[0]] = guest[1]
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
	
	def contain(self, sp):
		if not isinstance(sp, seph):
			raise TypeError
		if sp in self.sp:
			return self
		if self.child != []:
			for ch in self.child:
				res = ch.contain(s)
				if res:
					return res
		return None

	def _fensp(self, phrases, mend):
		if phrases == []:
			if not mend:
				return None
			else:
				if self.name == u'句号':
					phrases.insert(0,database.sp(u'。'))
				elif self.name == u'感叹号':
					phrases.insert(0,database.sp(u'！'))
				elif self.name == u'问号':
					phrases.insert(0,database.sp(u'？'))
				elif self.name == u'下引号':
					phrases.insert(0,database.sp(u'”'))
				else:
					return None
				return (phrases[0], [], {})
		if self.child != []:
			ress = []
			for i in range(-1,-len(self.child)-1, -1):
				res = self.child[i]._fensp(phrases, mend)
				if res:
					res[2][self.name] = res[0].s
					ress.append(res)
					return res
		else:
			if self.name[0] == '[' and self.name[-1] == u']':
				frame = self.name[1:-1].split(u' ')
			else:
				frame = []
			key = {}
			if frame == []:
				if phrases[0].be(self.name):
					key[self.name] = phrases[0].s
					return (phrases[0], phrases[1:], key)
				else:
					if mend:
						if self.name == u'逗号':
								phrases.insert(0,database.sp(u'，'))
						elif self.name == u'句号':
								phrases.insert(0,database.sp(u'。'))
						elif self.name == u'感叹号':
								phrases.insert(0,database.sp(u'！'))
						elif self.name == u'问号':
								phrases.insert(0,database.sp(u'？'))
						elif self.name == u'上引号':
								phrases.insert(0,database.sp(u'“'))
						else:
							return None
						return (phrases[0], phrases[1:], key)
					return None
			else:
				ress = []
				for i, gram in enumerate(frame):
					if gram == '':
						continue
					if database.gsin(gram):
						g = database.gs(gram)
						res = g._fensp(phrases, mend)
						if res == None:
							return None
						key[g.name] = res[0].s
						for k in res[2]:
							key[k] = res[2][k]
						ress.append(res)
						phrases = res[1]
					else:
						if gram == u'...':
							if i < len(frame)-1:
								while not (phrases[0].be(frame[i+1])):
									ress.append((phrases[0], phrases[1:], {}))
									phrases = phrases[1:]
									if phrases == []:
										break
							else:
								if phrases == []:
									break
								while True:
									ress.append((phrases[0], phrases[1:], {}))
									phrases = phrases[1:]
									if phrases == []:
										break
						elif gram[0] == u's':
							if phrases[0].s == gram[1:]:
								ress.append((phrases[0], phrases[1:], {}))
								phrases = phrases[1:]
							else:
								return None
						elif gram[0:2] == u'ws':
							if phrases[0].s == gram[2:]:
								ress.append((phrases[0], phrases[1:], {}))
								phrases = phrases[1:]
							else:
								if mend:
									ress.append((database.sp(gram[2:]), phrases, {}))
								else:
									continue
						elif gram[0] == u'w':
							assert gram[1:] in gset_all
							g = gset_all[gram[1:]]
							res = g._fensp(phrases, mend)
							if res != None:
								key[g.name] = res[0].s
								for k in res[2]:
									key[k] = res[2][k]
								ress.append(res)
								phrases = res[1]
							else:
								if mend and len(g.sp) == 1:
									for ph in g.sp:
										ress.append((ph, phrases, {}))
										break
								else:
									continue
						else:
							return None
				sps = []
				for res in ress:
					sps.append(res[0])
				sp = seph(sps)
				g.addsp(sp)
				key[self.name] = sp.s
				return (sp, ress[-1][1], key)
	
class seph:
	def __init__(self, s):
		if type(s) == unicode:
			self.s = s				#sting
			self.d = (s)			#迪卡尔
		elif type(s) == list and isinstance(s[0], seph):
			self.s = u''			#sting
			d = []
			for sp in s:
				d.append(sp.d)
			self.d = tuple(d)
		else:
			print s
			raise TypeError

	def be(self, gram):
		gs = database.gs(gram)
		if gs.contain(self) != None:
			return True
		return False

def fenci(waa, point):
	phrases = []
	con = False
	znumber =  u'0123456789'
	cnumber =  u'零一二三四五六七八九十百千万亿'
	zstr = u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	zpoint = u'，。,.！!？?'
	if not database.legal(waa):
		raise
	while waa != '':
		if waa[0] == u' ':
			waa = waa[1:]
		elif waa[0] in znumber:
			s = waa[0]
			waa = waa[1:]
			while waa != u'' and waa[0] in znumber:
				s += waa[0]
				waa = waa[1:]
			sp = seph(s)
			database.gs(u'数').addsp(sp)
			phrases.append(sp)
		elif waa[0] in cnumber:
			s = waa[0]
			waa = waa[1:]
			while waa != u'' and waa[0] in cnumber:
				s += waa[0]
				waa = waa[1:]
			sp = seph(s)
			database.gs(u'汉语数').addsp(sp)
			phrases.append(sp)
		elif waa[0] in zstr[10:]:
			s = waa[0]
			waa = waa[1:]
			while waa != u'' and waa[0] in zstr:
				s += waa[0]
				waa = waa[1:]
			sp = seph(s)
			database.gs(u'字符串').addsp(sp)
			phrases.append(sp)
		elif waa[0:2] == u'!=':
			phrases.append(database.sp(u'!='))
			waa = waa[2:]
		elif waa[0] in zpoint:
			if point:
				phrases.append(database.sp(waa[0]))
			waa = waa[1:]
		else:
			for i in range(min(8,len(waa)),0,-1):
				if database.spin(waa[0:i]):
					phrases.append(database.sp(waa[0:i]))
					waa = waa[i:]
					break
	return phrases
	
def main():
	print('db')
	database.gsinit()
	database.spinit()
	database.coreinit()
	
	phrases = fenci(u'十减去三十等于几', False)
	for p in phrases:
		print p.s
	g = database.gs(u'数学语句')
	sp = g._fensp(phrases, True)
	print sp[0]
	print sp[1]
	for k in sp[2]:
		print k+'='+sp[2][k]

if __name__ == '__main__':
	main()
