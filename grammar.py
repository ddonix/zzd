#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import re
import xlrd
import copy

gset_all = {}
gset_zzd = []
spbase_all = {}

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
							if phrases[0].be(u'标点符号'):
								phrases[0] = sentencephrase(u'，')
							else:
								phrases.insert(0,sentencephrase(u'，'))
						elif self.name == u'句号':
							if phrases[0].be(u'标点符号'):
								phrases[0] = sentencephrase(u'。')
							else:
								phrases.insert(0,sentencephrase(u'。'))
						elif self.name == u'感叹号':
							if phrases[0].be(u'标点符号'):
								phrases[0] = sentencephrase(u'！')
							else:
								phrases.insert(0,sentencephrase(u'！'))
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
		if type(arg) == list and type(arg[0]) == unicode:
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
					print 'E'+gram
					raise TypeError
				self.addgs(gs)
				gs.addsp(self)
		elif type(arg) == list and type(isinstance(arg[0], sentencephrase)):
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
		elif type(arg) == str or type(arg) == unicode:
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
		if type(v[0]) == float:
			v[0] = unicode(int(v[0]))
		sp = sentencephrase(v)
		spbase_all[v[0]] = {v[0]:sp}
	sp = sentencephrase([u' ', u'空格'])
	spbase_all[u' '] = {u' ':sp}
	
	sheet = book.sheet_by_name('table_phrase')
	nrows = sheet.nrows
	for i in range(nrows):
		v = sheet.row_values(i)
		sp = sentencephrase(v)
		assert len(v[0]) > 1
		assert v[0][0] in spbase_all
		spbase_all[v[0][0]][v[0]] = sp
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
	con = False
	znumber =  u'0123456789'
	zstr = u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
		else:
			for i in range(min(8,len(waa)),0,-1):
				if waa[0:i] in spbase_all[waa[0]]:
					phrases.append(sentencephrase(spbase_all[waa[0]][waa[0:i]]))
					waa = waa[i:]
					break
	if waa == '':
		return phrases
	return None
	
def main():
	print('grammar')
	initall()

	phrases = _fenci(u'小白认证,口令123456')
	for p in phrases:
		print p.s
	g = gset_all[u'认证语句']
	sp = g._fensp(phrases, True)
	print sp[0]
	print sp[1]
	for k in sp[2]:
		print k+'='+sp[2][k]
	

if __name__ == '__main__':
	main()
'''	
	sp = _fenci(u'播-234放word i like you 23403*234(44)歌+324!')
	for s in sp:
		print s.s
'''
'''
						if self.name == u'逗号':
							if phrases[0].be(u'标点符号'):
								phrases[0] = sentencephrase(u'，')
							else:
								phrases.insert(0,sentencephrase(u'，'))
						elif self.name == u'句号':
							if phrases[0].be(u'标点符号'):
								phrases[0] = sentencephrase(u'。')
							else:
								phrases.insert(0,sentencephrase(u'。'))
						elif self.name == u'感叹号':
							if phrases[0].be(u'标点符号'):
								phrases[0] = sentencephrase(u'！')
							else:
								phrases.insert(0,(sentencephrase(u'！'))
						else:
							return None
						return (phrases[0], phrases[1:], key)
'''
