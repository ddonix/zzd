#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import re
import xlrd
import copy
import sqlite3

gset_all = {}
spbase_all = {}

class gset:
	global gset_all
	def __init__(self, name, child):
		self.name = unicode(name)
		gset_all[self.name] = self
		self.sp = set()		#明确表示的元素集合
		self.plot = []		#明确的划分

		self.father = None	#父集
		self.child = []		#子集
		for ch in child:
			if ch == u'' or ch == None:
				continue
			if ch in gset_all:
				ch = gset_all[ch]
			else:
				if ch[0] == u'[' and ch[-1] == u']':
					ch = gset(ch, [])
				elif ch[0] == u'(' and ch[-1] == u')':
					ch = ch[1:-1].split(' ')
					print 'fffffffffffffffffffff'
			ch.father = self
			self.child.append(ch)

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
							while not phrases[0].be(frame[i+1]):
								ress.append((sentencephrase(phrases[0]), phrases[1:], {}))
								phrases = phrases[1:]
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

def gsetadd(name, yilai):
	global gset_all
	global	conn
	
	if name in gset_all:
		return True
	#sql = u'select * from gset_phrase where name=\'%s\''%name
	sql = u'select * from gset_phrase where name=\'%s\''%name
	print sql
	
	cursor = conn.execute(sql)
	ok = True
	print name
	print cursor.fetchall()
'''	gram = cursor.fetchall()[0]
	conn.close()
	print gram
	for child in gram[1:]:
		if child == '' or child == None:
			continue
		gsetadd(child, yilai)
		print child
	return ok
'''
'''	
	for child in gram[1:]:
		print child
		if child == '' or child == None:
			continue
		if not gsetadd(child, yilai):
			yilai.append(child)
			ok = False
'''	
	
def initall():
	global gset_all
	global spbase_all
	
	conn = sqlite3.connect('./data/grammar.db')
	cursor = conn.execute("select * from gset_phrase")
	for v in cursor:
		g = gset(v[0], v[1:])
		gset_all[v[0]] = g
	
	cursor = conn.execute("select * from gset_sentence")
	for v in cursor:
		g = gset(v[0], v[1:])
		gset_all[v[0]] = g
	
	cursor = conn.execute("select * from table_vocable")
	for v in cursor:
		assert len(v[0]) == 1
		sp = sentencephrase(v)
		spbase_all[v[0]] = {v[0]:sp}
	sp = sentencephrase((u' ', u'空格'))
	spbase_all[u' '] = {u' ':sp}
	
	cursor = conn.execute("select * from table_phrase")
	for v in cursor:
		assert len(v[0]) > 1
		assert v[0][0] in spbase_all
		sp = sentencephrase(v)
		spbase_all[v[0][0]][v[0]] = sp
	conn.close()

def _fenci(waa, point):
	phrases = []
	con = False
	znumber =  u'0123456789'
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
	
conn = None
def main():
	print('grammar')
	#initall()
	global conn
	conn = sqlite3.connect('./data/grammar.db')
	yilai = []
	gsetadd(u'认证确认', yilai)
	print yilai
	conn.close()

if __name__ == '__main__':
	main()
'''	
	sheet = book.sheet_by_name('grammar_sentence')
	nrows = sheet.nrows
	for i in range(nrows):
		v = sheet.row_values(i)
		g = gset(v[0], v[1:])
		gset_all[v[0]] = g
		if v[0][0] == 'S':
			gset_zzd.append([v[0], g])
	book.release_resources()
'''	
'''	
	phrases = _fenci(u'小白，认证123456!', True)
	for p in phrases:
		print p.s
	g = gset_all[u'认证语句']
	sp = g._fensp(phrases, True)
	print sp[0]
	print sp[1]
	for k in sp[2]:
		print k+'='+sp[2][k]
'''
