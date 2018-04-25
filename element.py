#!/usr/bin/python3 -B
import sets
import gdata

class seph:
	def __init__(self, s):
		assert not gdata.spin(s)
		if type(s) == str:
			self.s = s				#sting
			self.d = (s)			#迪卡尔
			self.gs = set()
			gdata.addsp(self)
		elif type(s) == list and isinstance(s[0], seph):
			self.s = ''			#sting
			d = []
			self.gs = set()
			for sp in s:
				self.s += sp.s
				d.append(sp.d)
			self.d = tuple(d)
			gdata.addsp(self)
		else:
			raise TypeError
	
	#返回False，说明这条信息是多余的。
	#返回True, 说明这条信息是有用的。
	def _addgs(self, gs):
		assert not gs in self.gs
		self.gs.add(gs)
	
	def _removegs(self, gs):
		assert gs in self.gs
		self.gs.remove(gs)

	#0:是
	#1:不是
	#2:不清楚
	def bebe(self, gram):
		gs = gdata.getgs(gram)
		res = gs.contain(self)
		if res:
			return (0,res)
		for g in self.gs:
			res = sets.gset.conflict(g, gs)
			if res:
				return (1,res[1])
		return (2,'')

def main():
	print('element')

if __name__ == '__main__':
	main()
