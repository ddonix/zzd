# coding: utf-8

class vocable:
	def __init__(self, describe):
		self.v = describe[0]
		self.a = []
		self.len = 0
		self.type = 0
		for i in range(1, len(describe), 2):
			if describe[i] == u'':
				break
			self.a.append((describe[i], describe[i+1]))
			self.len += 1
	
	def belone(self, attr):
		for at in self.a:
			if at == attr:
				return True
		return False
	
class phrase:
	def __init__(self, describe):
		self.v = describe[0]
		self.a = []
		self.len = 0
		self.type = 1
		for i in range(1, len(describe), 2):
			if describe[i] == u'':
				break
			self.a.append((describe[i], describe[i+1]))
			self.len += 1
	
	def belone(self, attr):
		for at in self.a:
			if at == attr:
				return True
		return False
	
	def satisfygrammar(self, attr, gram, add):
		X = self
		R = False
		gram = u'R=(%s)'%gram
		try:
			exec(gram)
		except:
			return False
		if R and add:
			self.a.append(attr)
		return R

class sentence:
	def __init__(self, phras):
		self.v = phras
		self.a = []
		self.type = 2
		self.len = len(phras)
	
	def belone(self, attr):
		for at in self.a:
			if at == attr:
				return True
		return False
	
	def satisfygrammar(self, attr, gram, add):
		X = self
		R = False
		gram = u'R=(%s)'%gram
		try:
			exec(gram)
		except:
			return False
		if R and add:
			self.a.append(attr)
		return R
