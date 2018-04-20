#!/usr/bin/python3 -B
import sqlite3
import copy
import gdata
import element

class gset:
	def __init__(self, name):
		self.name = name
		gdata.addgs(self)
		
		self.father = []	#父集
		self.child = []		#子集
		self.sp = set()		#元素集合，这个集合里的元素不属于任何子集.
		self.plot = {}		#划分.分为命名划分和匿名划分
							#命名划分：人划分为[性别:男|女],子集为男人，女人.
							#匿名划分:自然数划分为[奇数|偶数],子集为奇数，偶数.
		
		#形如[A (a) B]的集合，[]不允许递归.把包含的(a)型集合创建出来。
		if name[0] == '[' and name[-1] == ']' and name.find('(') != -1:
			name = name[1:-1].split(' ')
			for gram in name:
				#（a b c）集合包含a b c三个元素,这种是匿名集合.
				if gram[0] == '(' and gram[-1] == ')':
					gset(gram)
		

	def add_child(self, gram):
		for ch in gram:
			self._add_child(ch)

	def _add_child(self, ch):
		assert ch
		if gdata.gsin(ch):
			ch = gdata.getgs(ch)
			return self.__add_child(ch)
		if ch[0] == '(' and ch[-1] == ')':
			ch = gset(ch)
			return self.__add_child(ch)
		assert ch[0] == '[' and ch[-1] == ']'
		if not '|' in ch:					#[主语 谓语 宾语]
			ch = gset(ch)
			return self.__add_child(ch)
		if ':' in ch:						#[性别:男|女]
			name = ch[1:ch.find(':')]
			plots = ch[ch.find(':')+1:-1].split('|')
			plot = set()
			for p in plots:
				if p[0] == '(' and p[-1] == ')':
					ch = gset(p)
				else:
					assert gdata.gsin('%s%s'%(p,self.name))
					ch = gdata.getgs('%s%s'%(p,self.name))
				if not self.__add_child(ch):
					return False
				plot.add(ch)
			self.plot[name]=plot
		else:								#[奇数|偶数]
			plots = ch[1:-1].split('|')
			plot = set()
			for p in plots:
				if p[0] == '(' and p[-1] == ')':
					ch = gset(p,[])
				else:
					assert gdata.gsin(p)
					ch = gdata.getgs(p)
				if not self.__add_child(ch):
					return False
				plot.add(ch)
			self.plot[ch]=plot
		return True
	
	def __add_child(self, ch):
		if ch in self.child:
			assert self in ch.father
			return True
		assert not self in ch.father
		if gset.conflict(self, ch):
			print('%s and %s is conflict.'%(self.name,ch.name))
			return False
		self.child.append(ch)
		ch.father.append(self)
		return True
	
	#集合A的父集, 包括自己
	@classmethod
	def get_ancset(cls, gs_A):
		res = []
		res.append(gs_A)
		for fa in gs_A.father:
			res.append(fa)
			res.extend(cls.get_ancset(fa))
		res=list(set(res))
		return res
	
	#集合A的子集,包括自己
	@classmethod
	def get_subset(cls, gs_A):
		res = []
		res.append(gs_A)
		for ch in gs_A.child:
			res.append(ch)
			res.extend(cls.get_subset(ch))
		return res
	
	
	#集合A和B的合集是否为空集，是返回True.
	#合集不为空集或者无法判定，返回False.
	@classmethod
	def conflict(cls, gs_A, gs_B):
		if not gs_A.father or not gs_B.father:
			return False
		for A_fa in gs_A.father:
			for B_fa in gs_B.father:
				if A_fa == B_fa:
					for plot in A_fa.plot:
						if gs_A in A_fa.plot[plot] and gs_B in A_fa.plot[plot]:
							return True
		for fa in gs_A.father:
			if cls.conflict(fa, gs_B) == True:
				return True
		for fa in gs_B.father:
			if cls.conflict(gs_A, fa) == True:
				return True
		return False
	
	#集合A包含于集合B 	A<=B
	@classmethod
	def involved_in(cls, gs_A, gs_B):
		if gs_A == gs_B:
			return True
		for fa in gs_A.father:
			if cls.involved_in(fa, gs_B):
				return True
		return False
	
	#集合A包含集合B 	A>=B (B<=A)
	@classmethod
	def involved(cls, gs_A, gs_B):
		if gs_A == gs_B:
			return True
		for ch in gs_A.child:
			if cls.involved(ch, gs_B):
				return True
		return False

	def _addsp(self, sp):
		if not self.contain(sp):
			self.sp.add(sp)
	def _removesp(self, sp):
		if sp not in self.sp:
			raise TypeError
		self.sp.remove(sp)
	
	def contain(self, sp):#苏格拉底是男人，是人。但是数据库中之记录苏格拉底是男人.
		res = []
		if sp in self.sp:
			res.append(self)
		for ch in self.child:
			res.extend(ch.contain(sp))
		return res
	
	#只处理基本集合。没有子集，不依赖任何别的集合。例如，句号，感叹号，阿拉伯数字,基本汉字
	def fensp_1(self, phrases, mend):
		assert self.child == []
		assert self.name[0] != '(' and self.name[0] != ')'
		assert self.name[0] != '[' and self.name[0] != ']'
		if phrases != [] and phrases[0] in self.sp:
			return (phrases[0], phrases[1:], {self.name:phrases[0].s})
		else:
			if not mend:
				return None
			if self.name in gdata._mend_add:
				phrases.insert(0,gdata.getsp(gdata._mend_add[self.name]))
				return (phrases[0], phrases[1:], {self.name:phrases[0].s})
			if phrases != [] and phrases[0].s in gdata._mend_replace:
				for replace in gdata._mend_replace[phrases[0].s]:
					if gdata.getsp(replace) in self.sp:
						phrases[0] = gdata.getsp(replace)
						return (phrases[0], phrases[1:], {self.name:phrases[0].s})
			return None
	
	#只处理()集合。没有子集，不依赖任何别的集合。例如(, o ?)
	def fensp_2(self, phrases, mend):
		assert self.child == []
		assert self.name[0] == '(' and self.name[-1] == ')'
		if phrases != [] and phrases[0] in self.sp:
			return (phrases[0], phrases[1:], {self.name:phrases[0].s})
		else:
			if not mend:
				return None
			for sp in self.sp:
				if sp in gdata._mend_add:
					phrases.insert(0,gdata.getsp(sp))
					return (phrases[0], phrases[1:], {self.name:sp})
			if phrases != [] and phrases[0].s in gdata._mend_replace:
				for replace in gdata._mend_replace[phrases[0].s]:
					if gdata.getsp(replace) in self.sp:
						phrases[0] = gdata.getsp(replace)
						return (phrases[0], phrases[1:], {self.name:phrases[0].s})
			return None
	
	#只处理[]集合。没有子集,但是要递归。例如[主语 谓语 句号] [上引号 ... 下引号] [认证命令 (身份)]
	def fensp_3(self, phrases, mend):
		assert self.child == []
		assert self.name[0] == '[' and self.name[-1] == ']'
		frame = self.name[1:-1].split(' ')
		if phrases == []:
			return None
		ress = []
		key = {}
		for i, gram in enumerate(frame):
			assert not (gram == '' or gram == ' ')
			if gdata.gsin(gram):
				g = gdata.getgs(gram)
				if g.child == []:
					if gram[0] == '(' and gram[-1] == ')':
						res = g.fensp_2(phrases, mend)
					else:
						res = g.fensp_1(phrases, mend)
				else:
					res = g._fensp(phrases, mend)
				if res == None:
					return None
				
				key[gram] = res[0].s
				for k in res[2]:
					key[k] = res[2][k]
				ress.append(res)
				phrases = res[1]
			elif gram == '.':
				if phrases == []:
					break
				ress.append((phrases[0], phrases[1:], {}))
				key['.'] = phrases[0].s
				phrases = phrases[1:]
			elif gram == '...':
				if i < len(frame)-1:
					while not (phrases[0].be(frame[i+1])):
						ress.append((phrases[0], phrases[1:], {}))
						phrases = phrases[1:]
						if phrases == []:
							break
				else:
					if phrases == []:
						break
					while True:
						ress.append((phrases[0], phrases[1:], {}))
						phrases = phrases[1:]
						if phrases == []:
							break
			else:
				print(gram)
				raise TypeError
			sps = []
			for res in ress:
				sps.append(res[0])
		sp = element.seph(sps)
		g._addsp(sp)
		key[self.name] = sp.s
		return (sp, ress[-1][1], key)
	
	def _fensp(self, phrases, mend):
		if self.child != []:
			ress = []
			for i in range(len(self.child)-1, -1, -1):
				res = self.child[i]._fensp(phrases, mend)
				if res:
					res[2][self.name] = res[0].s
					ress.append(res)
					return res
			return None
		else:
			if self.name[0] == '(' and self.name[-1] == ')':
				return self.fensp_2(phrases, mend)
			elif self.name[0] == '[' and self.name[-1] == ']':
				return self.fensp_3(phrases, mend)
			else:
				return self.fensp_1(phrases, mend)

def main():
	print('sets')
	gs1 = gset('人')
	gs2 = gset('男人')
	gs3 = gset('女人')
	gs4 = gset('活人')
	gs5 = gset('中国人')
	sp = element.seph('你')

	gs1.add_child(['[性别:男|女]', '活人', '中国人'])
	gs1._addsp(sp)
	sp.addgs(gs1)
	print(gset.conflict(gs1, gs2))
	print(gset.conflict(gs2, gs3))
	print(gset.conflict(gs1, gs3))
	print(gset.conflict(gs4, gs5))

if __name__ == '__main__':
	main()
