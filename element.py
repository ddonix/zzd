#!/usr/bin/python3 -B
import sets
import gdata
import db

class seph:
	def __init__(self, s):
		assert type(s) == str
		self.s = s				#sting
		self.d = []
		self.gs = set()
		self.fn = set()
		gdata.addsp(self)
	
	def _fenci(self, point):
		znumber =  '0123456789'
		cnumber =  '零一二三四五六七八九十百千万亿'
		zstr = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		zpoint = '，。,.！!？?的地得'
		if self.gs or self.d:
			return
		ss = self.s
		while ss != '':
			if ss[0] == ' ':
				ss = ss[1:]
			elif ss[0] in znumber:
				s = ss[0]
				ss = ss[1:]
				while ss != '' and ss[0] in znumber:
					s += ss[0]
					ss = ss[1:]
				sp = gdata.getsp(s) if gdata.spin(s) else seph(s)
				if not sp.gs:
					gs = gdata.getgs('数')
					sp._addgs(gs)
					gs._addsp(sp)
				self.d.append(sp)
			elif ss[0] in zstr[10:]:
				s = ss[0]
				ss = ss[1:]
				while ss != '' and ss[0] in zstr:
					s += ss[0]
					ss = ss[1:]
				sp = gdata.getsp(s) if gdata.spin(s) else seph(s)
				if not sp.gs:
					gs = gdata.getgs('字符串')
					sp._addgs(gs)
					gs._addsp(sp)
				self.d.append(sp)
			elif ss[0:2] == '!=':
				self.d.append(gdata.getsp('!='))
				ss = ss[2:]
			elif ss[0:2] == '>=':
				self.d.append(gdata.getsp('>='))
				ss = ss[2:]
			elif ss[0:2] == '<=':
				self.d.append(gdata.getsp('<='))
				ss = ss[2:]
			elif ss[0] in zpoint:
				if point:
					self.d.append(gdata.getsp(ss[0]))
				ss = ss[1:]
			else:
				for i in range(min(8,len(ss)),1,-1):
					if gdata.spin(ss[0:i]):
						if gdata.getsp(ss[0:i]) == self:
							continue
						self.d.append(gdata.getsp(ss[0:i]))
						ss = ss[i:]
						break
				else:
					if ss[0] not in cnumber:
						assert gdata.spin(ss[0])
						self.d.append(gdata.getsp(ss[0]))
						ss = ss[1:]
					else:
						s = ss[0]
						ss = ss[1:]
						while ss != '' and ss[0] in cnumber:
							s += ss[0]
							ss = ss[1:]
						sp = gdata.getsp(s) if gdata.spin(s) else seph(s)
						if not sp.gs:
							gs = gdata.getgs('汉语数')
							sp._addgs(gs)
							gs._addsp(sp)
						self.d.append(sp)
		if len(self.d) == 1:
			self.d = []

	def _addgs(self, gs):
		assert not gs in self.gs
		self.gs.add(gs)
	
	def _removegs(self, gs):
		assert gs in self.gs
		self.gs.remove(gs)
	
	#0:是
	#1:不是
	#2:不清楚
	def _be(self, gram):
		gs = gdata.getgs(gram)
		res = gs.contain(self)
		if res:
			return (0,res)
		for g in self.gs:
			res = sets.gset.conflict(g, gs)
			if res:
				return (1, g.name)
		return [2]

	#True:是
	#False:不是或者不确定
	def be(self, gram):
		if gdata.gsin(gram):
			gs = gdata.getgs(gram)
			res = gs.contain(self)
			if res:
				return (True,res)
			sp2 = None
			if self.d:
				sp2 = gs.fensp(self.d, True)
			elif self.gs:
				sp2 = gs.fensp([self], True)
			if sp2:
				return (True,sp2)
			return [False]
		elif gdata.fnin(gram):
			fn = gdata.getfn(gram)
			if fn.ds(self) == True and fn.vs() == '(True False)':
				return [fn.value(self),{}]
			return [False]
		else:
			return [False]

def main():
	print('element')
	db.gsinit()
	db.fninit()
	db.spinit()
	db.coreinit()
	
	sp = seph('12一心一意23work+23*2x 一切一百五十六32')
	sp._fenci(False)
	print(sp.s, len(sp.gs))
	for sp in sp.d:
		print(sp.s, len(sp.gs))
	
	sp = gdata.getsp_ok('一百')
	sp._fenci(False)
	print(sp.s, len(sp.gs))
	for sp in sp.d:
		print(sp.s, len(sp.gs))

if __name__ == '__main__':
	main()
