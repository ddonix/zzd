#!/usr/bin/python3 -B
import sqlite3
import copy
import gdata
import element

class gset:
	def __init__(self, name, child):
		self.name = name
		gdata.addgs(self)
		
		self.father = []	#父集
		self.child = []		#子集
		self.sp = set()		#元素集合，这个集合里的元素不属于任何子集.
		self.plot = {}		#划分.分为命名划分和匿名划分
							#命名划分：人划分为[性别:男|女],子集为男人，女人.
							#匿名划分:自然数划分为[奇数|偶数],子集为奇数，偶数.
		
		#形如[A (a) B]的集合，[]不允许递归.把包含的(a)型集合创建出来。
		if name[0] == '[' and name[-1] == ']':
			assert child == []
			name = name[1:-1].split(' ')
			for gram in name:
				#（a b c）集合包含a b c三个元素,这种是匿名集合.
				if gram[0] == '(' and gram[-1] == ')':
					gset(gram, [])
		
		#形如(a b c)的集合，a b c是其元素。在初始化元素的时候，添加到集合里来，现在不能操作。
		if name[0] == '(' and name[-1] == ')':
			pass

		for ch in child:
			if ch == '' or ch == None:
				continue
			if gdata.gsin(ch):
				ch = gdata.getgs(ch)
				if not ch in self.child:
					self.child.append(ch)
				if not self in ch.father:
					ch.father.append(self)
			elif ch[0] == '(' and ch[-1] == ')':
				ch = gset(ch, [])
				if not ch in self.child:
					self.child.append(ch)
				if not self in ch.father:
					ch.father.append(self)
			else:
				assert ch[0] == '[' and ch[-1] == ']'
				#[主语 谓语 宾语]
				if not '|' in ch:
					ch = gset(ch, [])
					if not ch in self.child:
						self.child.append(ch)
					if not self in ch.father:
						ch.father.append(self)
				else:
					#[性别:男|女]
					if ':' in ch:
						name = ch[1:ch.find(':')]
						plots = ch[ch.find(':')+1:-1].split('|')
						plot = set()
						for p in plots:
							if p[0] == '(' and p[-1] == ')':
								ch = gset(p,[])
							else:
								assert gdata.gsin('%s%s'%(p,self.name))
								ch = gdata.getgs('%s%s'%(p,self.name))
							if not ch in self.child:
								self.child.append(ch)
							if not self in ch.father:
								ch.father.append(self)
							plot.add(ch)
						self.plot[name]=plot
					#[奇数|偶数]
					else:
						plots = ch[1:-1].split('|')
						plot = set()
						for p in plots:
							if p[0] == '(' and p[-1] == ')':
								ch = gset(p,[])
							else:
								assert gdata.gsin(p)
								ch = gdata.getgs(p)
							if not ch in self.child:
								self.child.append(ch)
							if not self in ch.father:
								ch.father.append(self)
							plot.add(ch)
						self.plot[ch]=plot
	
	
	@classmethod
	def intersection(cls, gs_A, gs_B):
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

	@classmethod
	def prevgram(cls, gram):
		res = []
		for g in gram:
			res.extend(cls._prevgram(g))
		return res
	
	@classmethod
	def _prevgram(cls, gram):
		if gram == '' or gram == None:
			return []
		if not (gram[0] == '[' and gram[-1] == ']'):
			return [gram]
		gram = gram[1:-1].split(' ')
		tmp = []
		cls.__prevgram(gram,tmp)
		tmp.sort(key=lambda x:len(x))
		
		res = []
		for t in tmp:
			r = '[%s'%t[0]
			for s in t[1:]:
				r += ' %s'%s
			r += ']'
			res.append(r)
		return res
	
	@classmethod
	def __prevgram(cls, gram, res):
		if gram == []:
			return
		if gram[0] == '' or gram[0] == None:
			return
		if len(gram) == 1:
			if gram[0][0] == 'w':
				res.append([])
				res.append([gram[0][1:]])
			else:
				res.append([gram[0]])
			return
		cls.__prevgram(gram[1:], res)
		if gram[0][0] == 'w':
			res2 = []
			for g in res:
				ag = copy.deepcopy(g)
				ag.insert(0,gram[0][1:])
				res2.append(ag)
			res.extend(res2)
			return
		else:
			for g in res:
				g.insert(0,gram[0])
			return
			

	def addsp(self, sp):
		if not isinstance(sp, element.seph):
			raise TypeError
		if not self.contain(sp):
			self.sp.add(sp)
	
	def removesp(self, sp):
		if not isinstance(sp, element.seph):
			raise TypeError
		if sp not in self.sp:
			raise TypeError
		self.sp.remove(sp)
	
	def contain(self, sp):#苏格拉底是男人，是人。但是数据库中之记录苏格拉底是男人.
		if not isinstance(sp, element.seph):
			raise TypeError
		res = []
		if not self.child:
			if sp in self.sp:
				res.append(self)
			return res
		
		if sp in self.sp:
			return self
		if self.child != []:
			for ch in self.child:
				res = ch.contain(sp)
				if res:
					return res
		return None
	
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
		g.addsp(sp)
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

if __name__ == '__main__':
	main()
