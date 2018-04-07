#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import re
import xlrd 

gset_all = {}
gset_zzd = []
spbase_all = {}

def	nl2frame(nl):
	frame = []
	if nl[0:3] == u'顺序:':
		nl = nl[3:]
		nl = nl.split(' ')
		for f in nl:
			frame.append(f)
	elif nl[0:3] == u'边界:':
		nl = nl[3:]
		nl = nl.split(' ') 
		frame.append(nl[0])
		frame.append(u'while_not')
		frame.append(nl[1])
	return frame

class gset:
	global gset_all 
	def __init__(self, name, child):
		self.name = unicode(name)
		gset_all[self.name] = self
		self.sp = set()		#明确表示的元素集合
		self.father = None	#父集
		self.child = []		#子集
		for ch in child:
			if ch == u'':
				continue
			if ch in gset_all:
				ch = gset_all[ch]
			else:
				ch = gset(ch, [])
			ch.father = self
			self.child.append(ch)
	
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
	
	def contain(self, s):		#s的信息不要用,也不要修改s的信息s在这里只读。
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
		else:
			nl = self.name
			frame = []
			if nl[0:3] == u'顺序:':
				nl = nl[3:]
				nl = nl.split(' ')
				if len(nl) != s.len:
					return None
				for i,gram in enumerate(nl):
					gs = gset_all[gram]
					if gs.contain(s.c[i]) == None:
						return None
				return self
			elif nl[0:3] == u'边界:':
				nl = nl[3:]
				nl = nl.split(' ')
				l = gset_all[nl[0]]
				r = gset_all[nl[1]]
				if l.contain(s.c[0]) and r.contain(s.c[-1]):
					return self
				else:
					return None
			else:
				return None
	
class sentencephrase:
	global gset_all
	def __init__(self, arg, gs=None):
		if type(arg[0]) == str or type(arg[0]) == unicode:
			describe = arg
			self.s = describe[0]	#string
			self.c = []				#child
			self.len = 1
			self.gs = set()			#
			for gram in describe[1:]:
				if gram == '':
					break
				try:
					gs = gset_all[gram]
				except:
					raise TypeError
				self.addgs(gs)
				gs.addsp(self)
		else:
			senphr = arg
			self.s = u''
			self.c = senphr
			self.gs = set()
			self.len = len(senphr)
			for sp in senphr:
				self.s += sp.s
			if gs != None:
				self.addgs(gs)
				gs.addsp(self)
	
	def be(self, gram):
		gram = unicode(gram)
		if not gram in gset_all:
			return False
		g = gset_all[gram]
		for gs in self.gs:
			if g <= gs:
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

def initall():
	global gset_all
	global gset_zzd
	global spbase_all
	xlsfile = r"data/grammar.xls"		# 打开指定路径中的xls文件
	book = xlrd.open_workbook(xlsfile)	#得到Excel文件的book对象，实例化对象
	# 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
	sheet = book.sheet_by_name('grammar_phrase')
	nrows = sheet.nrows
	for i in range(nrows):
		v = sheet.row_values(i)
		g = gset(v[0], v[1:])
		gset_all[v[0]] = g
	
	sheet = book.sheet_by_name('grammar_sentence')
	nrows = sheet.nrows
	for i in range(nrows):
		v = sheet.row_values(i)
		g = gset(v[0], v[1:])
		gset_all[v[0]] = g
		if v[0][0] == 'S':
			gset_zzd.append([v[0], g])
	
	sheet = book.sheet_by_name('table_vocable')
	nrows = sheet.nrows
	for i in range(nrows):
		v = sheet.row_values(i)
		sp = sentencephrase(v)
		spbase_all[v[0]]=sp
	
	sheet = book.sheet_by_name('table_phrase')
	nrows = sheet.nrows
	for i in range(nrows):
		v = sheet.row_values(i)
		sp = sentencephrase(v)
		spbase_all[v[0]]=sp
	book.release_resources()
	

def fensp(gram, waa):
	if not gram in gset_all:
		return None
	phrases = _fenci(waa)
	res = _fensp(gset_all[gram], phrases)
	if res and res[1] == []:
		return res[0]
	else:
		return None

def _fenci(waa):
	phrases = []
	con = True
	while con:
		for p in spbase_all:
			if waa.find(p) == 0:
				phrases.append(spbase_all[p])
				waa = waa[len(p):]
				con = False
				break
		con = not con
	return phrases
	
def _fensp(gs, phrases):
	if not phrases or phrases == []:
		return None
	if gs.child != []:
		ress = []
		for ch in gs.child:
			res = _fensp(ch, phrases)
			if res:
				ress.append(res)
		if ress == []:
			return None
		for res in ress:
			if res[1] == []:
				return res
		return ress[0]
	else:
		frame = nl2frame(gs.name)
		if frame == []:
			if phrases[0].be(gs.name):
				return (phrases[0], phrases[1:])
			else:
				return None
		else:
			ress = []
			for i, gram in enumerate(frame):
				if gram in gset_all:
					g = gset_all[gram]
					res = _fensp(g, phrases)
					if res == None:
						return None
					else:
						ress.append(res)
						phrases = res[1]
				else:
					if gram != u'while_not':
						return None
					else:
						while not phrases[0].be(frame[i+1]):
							ress.append((phrases[0], phrases[1:]))
							phrases = phrases[1:]
			sps = []
			for res in ress:
				sps.append(res[0])
			sp = sentencephrase(sps, gs)
			return (sp, ress[-1][1])

def main():
	print('grammar')
	initall()
	sp = fensp(u'S命令语句丙', u'播放歌曲‘一瞬间’')
	print sp,sp.s
	sp = fensp(u'S命令语句甲', u'播放歌曲‘一瞬间’')
	print sp,sp.s

if __name__ == '__main__':
	main()
'''	
	print('grammar')
	sp = fensp(u'谓语', u'播放')
	print sp,sp.s
	sp = fensp(u'宾语', u'歌曲')
	print sp,sp.s
	sp = fensp(u'S命令语句甲', u'播放歌曲')
	print sp,sp.s
	initall()
	sp = fensp(u'S命令语句乙', u'播放歌曲!')
	print sp,sp.s
	sp = fensp(u'感叹号', u'!')
	print sp.s
	sp = fensp(u'感叹号', u'！')
	#print sp.s
	sp = fensp(u'名字', u'小白')
	#print sp,sp.s
	sp = fensp(u'主语', u'小白')
	#print sp,sp.s
	a = spbase_all[u'播放']
	b = spbase_all[u'歌曲']
	c = a+b
	res = c.be(u'S命令语句甲')
	print res
	res = b.be(u'S命令语句甲')
	print res
'''
