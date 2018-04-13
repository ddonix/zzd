#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import re
import xlrd
import copy
import sqlite3
	
gset_all = {}
spbase_all = {}
table_vocable = {u' '}
identifyDict = {}
defineDict = {}
keyword_zzd = {}


class gset:
	global gset_all
	def __init__(self, name, child):
		self.name = unicode(name)
		gset_all[self.name] = self
		self.sp = set()		#明确表示的元素集合
		self.plot = {}		#明确的划分;要有名字：比如人按性别分为男人和女人

		self.father = None	#父集
		self.child = []		#子集
		for ch in child:
			if ch == u'' or ch == None:
				continue
			if ch in gset_all:
				ch = gset_all[ch]
				ch.father = self
				self.child.append(ch)
			else:
				assert ch[0] == u'[' and ch[-1] == u']'
				if not u'|' in ch:	
					ch = gset(ch, [])
					ch.father = self
					self.child.append(ch)
				else:
					plot = ch[1:-1].split(u'|')
					plots = set()
					for p in plot[1:]:
						assert p in gset_all
						self.child.append(gset_all[p])
						gset_all[p].father = self
						plots.add(gset_all[p])
					self.plot[plot[0]]=plots

	def addplot(self, plot):
		assert type(plot) == set
		for gs in plot:
			assert isinstance(gs, gset)
			assert gs in self.child
		self.plot.append(plot)

	def __lt__(self, other): # if self < other: return True
		gs = self.father
		while gs:
			if gs == other:
				return True
			gs = gs.father
		return False
	
	def __gt__(self, other):#if self > other: return True
		gs = other.father
		while gs:
			if gs == self:
				return True
			gs = gs.father
		return False
	
	def __le__(self, other): # if self <= other: return True
		if self == other:
			return True
		gs = self.father
		while gs:
			if gs == other:
				return True
			gs = gs.father
		return False
	
	def __ge__(self, other):#if self >= other: return True
		if self == other:
			return True
		gs = other.father
		while gs:
			if gs == self:
				return True
			gs = gs.father
		return False

	
	def addsp(self, s):
		if isinstance(s, sentencephrase):
			self.sp.add(s)
		else:
			raise TypeError
	
	def contain(self, s):		
		if not isinstance(s, sentencephrase):
			raise TypeError
		if s in self.sp:
			return self
		if self.child != []:
			for ch in self.child:
				res = ch.contain(s)
				if res:
					return res
			return None
		else:						#没子集的都是构造出来的，不需要进行处理.
			return None

	def _fensp(self, phrases, mend):
		if phrases == []:
			if not mend:
				return None
			else:
				if self.name == u'句号':
					phrases.insert(0,sentencephrase(u'。'))
				elif self.name == u'感叹号':
					phrases.insert(0,sentencephrase(u'！'))
				elif self.name == u'问号':
					phrases.insert(0,sentencephrase(u'？'))
				elif self.name == u'下引号':
					phrases.insert(0,sentencephrase(u'”'))
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
					return (sentencephrase(phrases[0]), phrases[1:], key)
				else:
					if mend:
						if self.name == u'逗号':
								phrases.insert(0,sentencephrase(u'，'))
						elif self.name == u'句号':
								phrases.insert(0,sentencephrase(u'。'))
						elif self.name == u'感叹号':
								phrases.insert(0,sentencephrase(u'！'))
						elif self.name == u'问号':
								phrases.insert(0,sentencephrase(u'？'))
						elif self.name == u'上引号':
								phrases.insert(0,sentencephrase(u'“'))
						else:
							return None
						return (phrases[0], phrases[1:], key)
					return None
			else:
				ress = []
				for i, gram in enumerate(frame):
					if gram == '':
						continue
					if gram in gset_all:
						g = gset_all[gram]
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
									ress.append((sentencephrase(phrases[0]), phrases[1:], {}))
									phrases = phrases[1:]
									if phrases == []:
										break
							else:
								if phrases == []:
									break
								while True:
									ress.append((sentencephrase(phrases[0]), phrases[1:], {}))
									phrases = phrases[1:]
									if phrases == []:
										break
						elif gram[0] == u's':
							if phrases[0].s == gram[1:]:
								ress.append((sentencephrase(phrases[0]), phrases[1:], {}))
								phrases = phrases[1:]
							else:
								return None
						elif gram[0:2] == u'ws':
							if phrases[0].s == gram[2:]:
								ress.append((sentencephrase(phrases[0]), phrases[1:], {}))
								phrases = phrases[1:]
							else:
								if mend:
									ress.append((sentencephrase(gram[2:]), phrases, {}))
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
				sp = sentencephrase(sps, self)
				key[self.name] = sp.s
				return (sp, ress[-1][1], key)

class sentencephrase:
	global gset_all
	def __init__(self, arg, gs=None):
		if type(arg) == tuple and type(arg[0]) == unicode:#从数据库中生成
			describe = arg
			self.s = describe[0]	#string
			self.c = []				#child
			self.len = 1
			self.gs = set()			#
			for gram in describe[1:]:
				if gram == '' or gram == None:
					break
				try:
					gs = gset_all[gram]
				except:
					raise TypeError
				self.addgs(gs)
				gs.addsp(self)
		elif type(arg) == list and type(isinstance(arg[0], sentencephrase)):#由gset生成
			senphr = arg
			self.s = u''
			self.c = senphr
			self.gs = set()
			self.len = len(senphr)
			for sp in senphr:
				self.s += sp.s
			assert gs != None
			self.addgs(gs)
			gs.addsp(self)
		elif type(arg) == unicode:
			assert arg[0] in spbase_all
			assert arg in spbase_all[arg[0]]
			arg = spbase_all[arg[0]][arg]
			self.s = arg.s
			self.c = copy.deepcopy(arg.c)
			self.len = arg.len
			self.gs = set()
			for gs in arg.gs:
				self.addgs(gs)
				gs.addsp(self)
		elif isinstance(arg, sentencephrase):
			self.s = arg.s
			self.c = copy.deepcopy(arg.c)
			self.len = arg.len
			self.gs = set()
			for gs in arg.gs:
				self.addgs(gs)
				gs.addsp(self)
		else:
			raise TypeError
	
	def be(self, gram):
		gram = unicode(gram)
		if not gram in gset_all:
			return False
		g = gset_all[gram]
		for gs in self.gs:
			if gs <= g:
				self.addgs(g)
				g.addsp(self)
				gs.addsp(self)
				return True
		gs = g.contain(self)
		if gs:
			while gs != g:
				self.addgs(gs)
				gs.addsp(self)
				gs = gs.father
			self.addgs(gs)
			gs.addsp(self)
			return True
		return False

	def addgs(self, gs):
		if isinstance(gs, gset):
			self.gs.add(gs)
	
	def __radd__(self, other):#return other+self
		res = sentencephrase([other, self], None)
		return res

	def append(self, sp):
		sps = []
		if self.c == []:
			sps.append(self)
		else:	
			for sp in self.c:
				sps.append(sp)
		sps.append(sp)
		res = sentencephrase(sps, None)
		return res

def _fenci(waa, point):
	phrases = []
	con = False
	znumber =  u'0123456789'
	cnumber =  u'零一二三四五六七八九十百千万'
	zstr = u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	zpoint = u'，。？！,.?!'
	while waa != '':
		if waa[0] in znumber:
			n = sentencephrase(spbase_all[waa[0]][waa[0]])
			gs = gset_all[u'数']
			n.addgs(gs)
			gs.addsp(n)
			
			waa = waa[1:]
			while waa != u'' and waa[0] in znumber:
				n.s += waa[0]
				waa = waa[1:]

			phrases.append(n)
		elif waa[0] in cnumber:
			n = sentencephrase(spbase_all[waa[0]][waa[0]])
			gs = gset_all[u'汉语数']
			n.addgs(gs)
			gs.addsp(n)
			
			waa = waa[1:]
			while waa != u'' and waa[0] in cnumber:
				n.s += waa[0]
				waa = waa[1:]

			phrases.append(n)
		elif waa[0] in zstr[10:]:
			n = sentencephrase(spbase_all[waa[0]][waa[0]])
			gs = gset_all[u'字符串']
			n.addgs(gs)
			gs.addsp(n)
			
			waa = waa[1:]
			while waa != u'' and waa[0] in zstr:
				n.s += waa[0]
				waa = waa[1:]
			phrases.append(n)
		elif waa[0] in zpoint:
			if waa[0:2] == u'!=' or waa[0:2] == u'！=':
				phrases.append(sentencephrase(u'!='))
				waa = waa[2:]
			else:
				if point:
					phrases.append(sentencephrase(waa[0]))
				waa = waa[1:]
		else:
			for i in range(min(8,len(waa)),0,-1):
				if waa[0:i] in spbase_all[waa[0]]:
					phrases.append(sentencephrase(spbase_all[waa[0]][waa[0:i]]))
					waa = waa[i:]
					break
	if waa == '':
		return phrases
	return None
	

def gsetinit():
	global gset_all, spbase_all, table_vocable, identifyDict, defineDict, keyword_zzd
	
	conn = sqlite3.connect('./data/grammar.db')
	cursor = conn.execute("select * from gset_phrase")
	v = cursor.fetchall()
	cursor = conn.execute("select * from gset_sentence")
	v.extend(cursor.fetchall())
	conn.close()
	while v != []:
		if v[0][0] in gset_all:
			v.pop(0)
			continue
		skip = True
		for g in v[0][1:]:
			if g == '' or g == None or (g in gset_all):
				continue
			if not (g[0] == u'[' and g[-1] == u']'):
				break
			if not u'|' in g:
				gsp = g[1:-1].split(' ')
				skip2 = True
				for gg in gsp:
					if gg == '' or gg == u'...' or gg[0] == u's' or gg[0:2] == u'ws' or (gg in gset_all):
						continue
					if gg[0] == u'p' and gg[1:] in gset_all:
						continue
					if gg[0] == u'w' and gg[1:] in gset_all:
						continue
					print u'依赖%s'%gg
					break
				else:
					skip2 = False
				if skip2:
					break
			else:
				gsp = g[1:-1].split('|')
				skip2 = True
				for gg in gsp[1:]:
					if not (gg == '' or (gg in gset_all)):
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
	for name in gset_all:
		print name, len(gset_all[name].child)
	
def spinit():
	global gset_all, spbase_all, table_vocable, identifyDict, defineDict, keyword_zzd
	conn = sqlite3.connect('./data/grammar.db')
	cursor = conn.execute("select * from table_vocable")
	table_vocable = set()
	for v in cursor:
		assert len(v[0]) == 1
		sp = sentencephrase(v)
		spbase_all[v[0]] = {v[0]:sp}
		table_vocable.add(v[0])
	sp = sentencephrase((u' ', u'空格'))
	spbase_all[u' '] = {u' ':sp}
	
	cursor = conn.execute("select * from table_phrase")
	for v in cursor:
		assert len(v[0]) > 1
		for i in v[0]:
			if not i in spbase_all:
				print '在词组表中出现的字符没有在字符表中出现',v[0],i
			assert i in spbase_all
		sp = sentencephrase(v)
		spbase_all[v[0][0]][v[0]] = sp
	conn.close()

def coreinit():
	global gset_all, spbase_all, table_vocable, identifyDict, defineDict, keyword_zzd
	conn = sqlite3.connect('./data/grammar.db')
	cursor = conn.execute("select * from define")
	for define in cursor:
		defineDict[define[0]] = define[1]
		for defi in define:
			for d in defi:
				if not d in table_vocable:
					print '定义中没有在字符表中出现的字符',defi, d
				assert d in table_vocable

		
	cursor = conn.execute("select * from zzd_keyword")
	for keyword in cursor:
		keyword_zzd[keyword[0]] = keyword[1:]
		
	for sp in spbase_all:
		for s in spbase_all[sp]:
			if spbase_all[sp][s].be(u'zzd关键字'):
				if not s in keyword_zzd:
					print '在符号表中定义为zzd关键字，但是没有在关键字表中出现',s
				assert s in keyword_zzd

	cursor = conn.execute("select * from verify")
	for guest in cursor:
		identifyDict[guest[0]] = guest[1]
	conn.close()

def main():
	print('db')
	gsetinit()
	spinit()
	coreinit()

	phrases = _fenci(u'十减去三十等于几', False)
	for p in phrases:
		print p.s
	g = gset_all[u'数学语句']
	sp = g._fensp(phrases, True)
	print sp[0]
	print sp[1]
	for k in sp[2]:
		print k+'='+sp[2][k]

if __name__ == '__main__':
	main()

class database:
	@classmethod
	def gs(cls, gram):
		return None
	
	@classmethod
	def sp(cls, s):
		return None
	
class seph:
	def __init__(self, arg):
		try:
			self.s = arg[0]			#string
			self.d = (arg[0])		#迪卡尔
			
			for gram in arg[1:]:
				if not gram == '' or gram == None:
					break
				gs = database.gs(gram)
				gs.addsp(self)
		except:
			raise TypeError

	def copyseph(s):
		try:
			sp = seph([s])
			sp.d = copy.deepcopy(database.sp(s))
		except:
			raise TypeError

	def newseph:
		elif type(arg) == list and type(isinstance(arg[0], seph)):#由gset生成
			self.s = u''
			self.d = arg
			
			for sp in senphr:
				self.s += sp.s
			assert gs != None
			self.addgs(gs)
			gs.addsp(self)
			raise TypeError
	
	def be(self, gram):
		gram = unicode(gram)
		if not gram in gset_all:
			return False
		g = gset_all[gram]
		for gs in self.gs:
			if gs <= g:
				self.addgs(g)
				g.addsp(self)
				gs.addsp(self)
				return True
		gs = g.contain(self)
		if gs:
			while gs != g:
				self.addgs(gs)
				gs.addsp(self)
				gs = gs.father
			self.addgs(gs)
			gs.addsp(self)
			return True
		return False

	def addgs(self, gs):
		if isinstance(gs, gset):
			self.gs.add(gs)
	
	def __radd__(self, other):#return other+self
		res = sentencephrase([other, self], None)
		return res

	def append(self, sp):
		sps = []
		if self.c == []:
			sps.append(self)
		else:	
			for sp in self.c:
				sps.append(sp)
		sps.append(sp)
		res = sentencephrase(sps, None)
		return res

def _fenci(waa, point):
	phrases = []
	con = False
	znumber =  u'0123456789'
	cnumber =  u'零一二三四五六七八九十百千万'
	zstr = u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	zpoint = u'，。？！,.?!'
	while waa != '':
		if waa[0] in znumber:
			n = sentencephrase(spbase_all[waa[0]][waa[0]])
			gs = gset_all[u'数']
			n.addgs(gs)
			gs.addsp(n)
			
			waa = waa[1:]
			while waa != u'' and waa[0] in znumber:
				n.s += waa[0]
				waa = waa[1:]

			phrases.append(n)
		elif waa[0] in cnumber:
			n = sentencephrase(spbase_all[waa[0]][waa[0]])
			gs = gset_all[u'汉语数']
			n.addgs(gs)
			gs.addsp(n)
			
			waa = waa[1:]
			while waa != u'' and waa[0] in cnumber:
				n.s += waa[0]
				waa = waa[1:]

			phrases.append(n)
		elif waa[0] in zstr[10:]:
			n = sentencephrase(spbase_all[waa[0]][waa[0]])
			gs = gset_all[u'字符串']
			n.addgs(gs)
			gs.addsp(n)
			
			waa = waa[1:]
			while waa != u'' and waa[0] in zstr:
				n.s += waa[0]
				waa = waa[1:]
			phrases.append(n)
		elif waa[0] in zpoint:
			if waa[0:2] == u'!=' or waa[0:2] == u'！=':
				phrases.append(sentencephrase(u'!='))
				waa = waa[2:]
			else:
				if point:
					phrases.append(sentencephrase(waa[0]))
				waa = waa[1:]
		else:
			for i in range(min(8,len(waa)),0,-1):
				if waa[0:i] in spbase_all[waa[0]]:
					phrases.append(sentencephrase(spbase_all[waa[0]][waa[0:i]]))
					waa = waa[i:]
					break
	if waa == '':
		return phrases
	return None
	

def gsetinit():
	global gset_all, spbase_all, table_vocable, identifyDict, defineDict, keyword_zzd
	
	conn = sqlite3.connect('./data/grammar.db')
	cursor = conn.execute("select * from gset_phrase")
	v = cursor.fetchall()
	cursor = conn.execute("select * from gset_sentence")
	v.extend(cursor.fetchall())
	conn.close()
	while v != []:
		if v[0][0] in gset_all:
			v.pop(0)
			continue
		skip = True
		for g in v[0][1:]:
			if g == '' or g == None or (g in gset_all):
				continue
			if not (g[0] == u'[' and g[-1] == u']'):
				break
			if not u'|' in g:
				gsp = g[1:-1].split(' ')
				skip2 = True
				for gg in gsp:
					if gg == '' or gg == u'...' or gg[0] == u's' or gg[0:2] == u'ws' or (gg in gset_all):
						continue
					if gg[0] == u'p' and gg[1:] in gset_all:
						continue
					if gg[0] == u'w' and gg[1:] in gset_all:
						continue
					print u'依赖%s'%gg
					break
				else:
					skip2 = False
				if skip2:
					break
			else:
				gsp = g[1:-1].split('|')
				skip2 = True
				for gg in gsp[1:]:
					if not (gg == '' or (gg in gset_all)):
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
	for name in gset_all:
		print name, len(gset_all[name].child)
	
def spinit():
	global gset_all, spbase_all, table_vocable, identifyDict, defineDict, keyword_zzd
	conn = sqlite3.connect('./data/grammar.db')
	cursor = conn.execute("select * from table_vocable")
	table_vocable = set()
	for v in cursor:
		assert len(v[0]) == 1
		sp = sentencephrase(v)
		spbase_all[v[0]] = {v[0]:sp}
		table_vocable.add(v[0])
	sp = sentencephrase((u' ', u'空格'))
	spbase_all[u' '] = {u' ':sp}
	
	cursor = conn.execute("select * from table_phrase")
	for v in cursor:
		assert len(v[0]) > 1
		for i in v[0]:
			if not i in spbase_all:
				print '在词组表中出现的字符没有在字符表中出现',v[0],i
			assert i in spbase_all
		sp = sentencephrase(v)
		spbase_all[v[0][0]][v[0]] = sp
	conn.close()

def coreinit():
	global gset_all, spbase_all, table_vocable, identifyDict, defineDict, keyword_zzd
	conn = sqlite3.connect('./data/grammar.db')
	cursor = conn.execute("select * from define")
	for define in cursor:
		defineDict[define[0]] = define[1]
		for defi in define:
			for d in defi:
				if not d in table_vocable:
					print '定义中没有在字符表中出现的字符',defi, d
				assert d in table_vocable

		
	cursor = conn.execute("select * from zzd_keyword")
	for keyword in cursor:
		keyword_zzd[keyword[0]] = keyword[1:]
		
	for sp in spbase_all:
		for s in spbase_all[sp]:
			if spbase_all[sp][s].be(u'zzd关键字'):
				if not s in keyword_zzd:
					print '在符号表中定义为zzd关键字，但是没有在关键字表中出现',s
				assert s in keyword_zzd

	cursor = conn.execute("select * from verify")
	for guest in cursor:
		identifyDict[guest[0]] = guest[1]
	conn.close()

def main():
	print('db')
	gsetinit()
	spinit()
	coreinit()

	phrases = _fenci(u'十减去三十等于几', False)
	for p in phrases:
		print p.s
	g = gset_all[u'数学语句']
	sp = g._fensp(phrases, True)
	print sp[0]
	print sp[1]
	for k in sp[2]:
		print k+'='+sp[2][k]

if __name__ == '__main__':
	main()