#!/usr/bin/python3 -B
import gdata
import sets

class seph:
	def __init__(self, s):
		if type(s) == str:
			self.s = s				#sting
			self.d = (s)			#迪卡尔
			self.gs = []
		elif type(s) == list and isinstance(s[0], seph):
			self.s = ''			#sting
			d = []
			self.gs = []
			for sp in s:
				self.s += sp.s
				d.append(sp.d)
			self.d = tuple(d)
		else:
			raise TypeError
	
	#返回False，说明这条信息是多余的。
	#返回True, 说明这条信息是有用的。
	def addgs(self, gs):
		assert not gs in self.gs
		self.gs.append(gs)
	
	def removegs(self, gs):
		assert gs in self.gs
		self.gs.remove(gs)

	def be(self, gram):
		gs = gdata.getgs(gram)
		res = gs.contain(self)
		for g in res:
			print(g.name)
		if res:
			return True
		return False

def main():
	print('element')
	gs = sets.gset('你好')
	sp = seph('合理')
	sp.addgs(gs)
	gs.addsp(sp)

if __name__ == '__main__':
	main()
