#!/usr/bin/python -B
# -*- coding: UTF-8 -*-

import re

grammar_all = {}
sp_all = {}

def prevgrammar(name, nl):
	gram = u''
	attrs = []
	if nl[0:3] == u'顺序:':
		nl = nl[3:]
		nl = nl.split(' ')
		gram = u'len(X) == %d'%len(nl)
		for i,p in enumerate(nl):
			gram += ' and X[%d].be(u\'%s\')'%(i,p)
			attrs.append(p)
	elif nl[0:3] == u'单个:':
		nl = nl[3:]
		gram = 'x.be(u\'%s\')'%nl
		attrs.append(nl)
	elif nl[0:3] == u'边界:':
		nl = nl[3:]
		nl = nl.split(' ')
		gram = 'X[0].be(u\'%s\') and X[-1].be(u\'%s\')'%(nl[0],nl[1])
		attrs.append(name)
	return gram, attrs

def _prevgram(gram):
	zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
	gram = list(gram)
	i = 0
	first = True
	while True:
		if i >= len(gram):
			break
		match = zhPattern.search(gram[i])
		if match:
			if first == True:
				gram.insert(i, u'u\'')
				first = False
				i += 1
			else:
				if i == (len(gram)-1):
					gram.append('\'')
					break
				else:
					i += 1
		else:
			if first == False:
				gram.insert(i, u'\'')
				i += 2
				first = True
			else:
				i += 1
	res = u''
	for g in gram:
		res += g
	return res

class gset:
	def __init__(self, name, gram):
		self.name = unicode(name)
		self.sp = set()		#明确表示的元素集合
		self.ag = []		#满足ag中的一项，即属于这个集合。肯定集合
		for g in gram:
			gg = prevgrammar(self.name, g)
			if gg[0] != u'':
				self.ag.append(gg)
	
	def copy(self, name):
		result = gset(name, [])
		for s in self.sp:
			result.sp.addsp(s)
		for g in self.ag:
			result.ag.append(g)
		return result
	
	def addsp(self, s):
		if isinstance(s, sentencephrase):
			self.sp.add(s)
	
	def addag(self, g):
		self.ag.append(unicode(g))
	
	def contain(self, s):
		if not isinstance(s, sentencephrase):
			raise TypeError
		if s in self.sp:
			return True
		else:
			for g in self.ag:
				if g[0].find(u'x') != -1 and g[0].find(u'X') == -1:
					x = s
				elif g[0].find(u'X') != -1 and g[0].find(u'x') == -1:
					X = s.c
				else:
					#print('^^^%s^^^'%g[0])
					raise NameError
				R = False
				gram = u'R=(%s)'%g[0]
				try:
					exec(gram)
				except:
					#print(gram)
					continue
				if R:
					return True
			return False
	
class sentencephrase:
	global grammar_all
	def __init__(self, arg, g=None):
		if type(arg[0]) == str or type(arg[0]) == unicode:
			describe = arg
			self.s = describe[0]	#string
			self.c = [self]			#child
			self.t = describe[0]	#tree
			self.len = 1
			
			self.attr = []			#attribute
			for a in describe[1:]:
				if a == '':
					break
				self.attr.append(a)
				try:
					gram = grammar_all[a]
				except:
					print('^^^^^^^^%s^^^^^^^'%a)
					print grammar_all
					raise TypeError
				gram.addsp(self)
		else:
			senphr = arg
			self.s = u''
			self.c = senphr
			self.t = []
			self.attr = []
			
			self.len = len(senphr)
			for sp in senphr:
				self.s += sp.s
				self.t.append(sp.t)
		if g != None:
			self.attr.append(g.name)
			g.addsp(self)

	@classmethod
	def init(cls):
		pass
	
	def be(self, gram):
		gram = unicode(gram)
		for a in self.attr:
			if gram == a:
				return True
		#print('$$%s'%gram)
		g = grammar_all[gram]
		if g.contain(self):
			self.attr.append(gram)
			return True
		return False
	
	def append(self, sp):
		if self.attr == []:
			self.s += sp.s
			self.t.append(sp.t)
			self.c.append(sp)
			self.len += 1
			
def main():
	print('grammar')
	g = gset(('',''), [])
	res = prevgrammar(u'juzi',u'顺序:谓语 宾语')
	print res[0]
	print res[1]
	res = prevgrammar(u'asdf', u'单个:及物动词')
	print res[0]
	print res[1]
	res = prevgrammar(u'addfa', u'边界:上引号 下引号')
	print res[0]
	print res[1]

	

if __name__ == '__main__':
	main()
