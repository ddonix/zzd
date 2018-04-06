#!/usr/bin/python -B
# -*- coding: UTF-8 -*-

class gset:
	def __init__(self, name, gram):
		self.name = unicode(name)
		self.sp = set()		#明确表示的元素集合
		self.ag = []		#满足ag中的一项，即属于这个集合。肯定集合
		for g in gram:
			self.ag.append(unicode(g))
	
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
				if g.find(u'x') != -1 and g.find(u'X') == -1:
					x = s
				elif g.find(u'X') != -1 and g.find(u'x') == -1:
					X = s.c
				else:
					raise NameError
				R = False
				gram = u'R=(%s)'%g
				try:
					exec(gram)
				except:
					print('YYYYYYYYYYYYY')
					print(gram)
					raise NameError
				if R:
					return True
			return False
	
class sentencephrase:
	grammar_all = None
	def __init__(self, arg):
		if type(arg[0]) == str or type(arg[0]) == unicode:
			describe = arg
			self.s = describe[0]	#string
			self.c = []				#child
			self.t = describe[0]	#tree
			self.len = 1			
			
			self.attr = []			#attribute
			for a in describe[1:]:
				if a == '':
					break
				self.attr.append(a)
				try:
					gram = sentencephrase.grammar_all[a]
				except:
					print('!!!!!!!!!!!')
					print a
					print('FFFFFFFFFFFFF')
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

	@classmethod
	def init(cls, grammar_all):
		cls.grammar_all = grammar_all
	
	def be(self, gram):
		gram = unicode(gram)
		for a in self.attr:
			if gram == a:
				return True
		g = sentencephrase.grammar_all[gram]
		if g.contain(self):
			self.attr.append(gram)
			return True
		return False
	
	def append(self, sp):
		if self.ag == []:
			self.s += sp.s
			self.t.append(sp.t)
			self.c.append(phrase)
			self.len += 1
			
def main():
	print('grammar')
	g = gset(('',''), [])
	print g

if __name__ == '__main__':
	main()
