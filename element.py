#!/usr/bin/python3 -B
import sets
import gdata
import db

class seph:
	def __init__(self, s):
		assert type(s) == str
		self.s = s				#sting
		self.d = [self]
		self.gs = set()
		gdata.addsp(self)
	
	#返回False，说明这条信息是多余的。
	#返回True, 说明这条信息是有用的。

	def _fenci(self, point):
		znumber =  '0123456789'
		cnumber =  '零一二三四五六七八九十百千万亿'
		zstr = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		zpoint = '，。,.！!？?的地得'
		waa = self.s
		
		while waa != '':
			if waa[0] == ' ':
				waa = waa[1:]
			elif waa[0] in znumber:
				s = waa[0]
				waa = waa[1:]
				while waa != '' and waa[0] in znumber:
					s += waa[0]
					waa = waa[1:]
				if gdata.spin(s):
					sp = gdata.getsp(s)
				else:
					sp = seph(s)
					gs = gdata.getgs('数')
					sp._addgs(gs)
					gs._addsp(sp)
				self.d.append(sp)
			elif waa[0] in cnumber:
				s = waa[0]
				waa = waa[1:]
				while waa != '' and waa[0] in cnumber:
					s += waa[0]
					waa = waa[1:]
				if gdata.spin(s):
					sp = gdata.getsp(s)
				else:
					sp = seph(s)
					gs = gdata.getgs('汉语数')
					sp._addgs(gs)
					gs._addsp(sp)
				self.d.append(sp)
			elif waa[0] in zstr[10:]:
				s = waa[0]
				waa = waa[1:]
				while waa != '' and waa[0] in zstr:
					s += waa[0]
					waa = waa[1:]
				if gdata.spin(s):
					sp = gdata.getsp(s)
				else:
					sp = seph(s)
					gs = gdata.getgs('汉语数')
					sp._addgs(gs)
					gs._addsp(sp)
				self.d.append(sp)
			elif waa[0:2] == '!=':
				self.d.append(gdata.getsp('!='))
				waa = waa[2:]
			elif waa[0] in zpoint:
				if point:
					self.d.append(gdata.getsp(waa[0]))
				waa = waa[1:]
			else:
				for i in range(min(8,len(waa)),0,-1):
					if gdata.spin(waa[0:i]):
						self.d.append(gdata.getsp(waa[0:i]))
						waa = waa[i:]
						break

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
			if gs.contain(self):
				return True
			return False
		elif gdata.fnin(gram):
			fn = gdata.getfn(gram)
			if fn.ds(self) == True and fn.vs() == '(True False)':
				return fn.value(self)
			return False
		else:
			return False

def main():
	print('element')
	db.spinit()
	sp = seph('1234+2*x+2341我的时间苏格拉底再见=2')
	sp._fenci(False)
	for sp in sp.d:
		print(sp.s)

if __name__ == '__main__':
	main()
