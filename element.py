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
		self.fn = {}
		gdata.addsp(self)
	
	def _fenci(self, point):
		znumber =  '0123456789'
		cnumber =  '零一二三四五六七八九十百千万亿'
		zstr = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		zpoint = '，。,.！!？?的地得'
		if self.gs:
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
	
	def addfn(self, fn):
		fn = fn.split('~')
		for f in fn:
			name,value=f.split(':')
			self.fn[name]=value
		print(self.fn)
	
	def _addgs(self, gs):
		assert not gs in self.gs
		self.gs.add(gs)
	
	def _removegs(self, gs):
		assert gs in self.gs
		self.gs.remove(gs)
	
	#True:是
	#False:不是或者不确定
	def be(self, gram):
		if gdata.getgs('集合').contain(self):
			if gram == '集合':								#人是集合吗？
				return (0,(self.s, [],{'集合':self.s}))
			else:
				res = sets.gset.involved_in(self.s, gram)	#人会死吗？
				return res
		if gdata.gsin(gram):
			gs = gdata.getgs(gram)
			res = gs.contain(self)
			if res:
				return (0,(self.s, [], {gram:self.s}))		#苏格拉底是人吗？
			for g in self.gs:
				res = sets.gset.conflict(g, gs)				#苏格拉底是鸟吗？（苏格拉底是人，人与鸟冲突）
				if res:
					return (1, g.name)
			res = None
			if self.d:
				res = gs.fensp(self.d, True)				#播放歌曲是命令语句吗？
			elif self.gs:
				res = gs.fensp([self], True)				#1234是数吗？
			if res:
				return (0, res)
			return [2]
		elif gdata.fnin(gram):
			fn = gdata.getfn(gram)							#1234是偶数吗？
			if fn.ds(self) == True and fn.vs(self) == 'bool':
				if fn.value_a(self):
					return (0,fn)
				else:
					return (1,fn)
			return [2,'完全无知阿']
		#苏格拉底是男人吗？
		#苏格拉底是男的吗?
		#苏格拉底是男的人吗？
		#苏格拉底的性别是男吗?
		#苏格拉底是人，人有性别，性别把人分男女，苏格拉底是男人吗等价于苏格拉底的性别是男吗？
		else:
			print('else:', self.s,gram)
			for gs in self.gs:
				for name in gs.fn:
					print('fn.name',gs.fn[name])
					return gs.fn[name].judge_a(self, gram)
			return [2,'我完全不知道']

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
