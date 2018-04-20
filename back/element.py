#!/usr/bin/python3 -B
import sqlite3
import copy
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
		assert isinstance(gs, sets.gset)
		assert not gs in self.gs
		return False
	
	def removegs(self, gs):
		assert isinstance(gs, sets.gset)
		assert gs in self.gs
		self.gs.remove(gs)

	def be(self, gram):
		gs = gdata.getgs(gram)
		if gs.contain(self) != None:
			return True
		return False

def main():
	print('element')

if __name__ == '__main__':
	main()
