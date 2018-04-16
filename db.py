#!/usr/bin/python3 -B
import sqlite3
import copy

class database: 
	_gset_all = {}				#所有集合
	_spbase_all = {}			#所有语句
	_table_vocable = {' '}		#所有字符
	
	_identifyDict = {}			#身份认证
	_defineDict = {}			#定义
	_gset_key = {}				#关键集合
	_keyword_zzd = {}			#关键语句
	_mend_add = {}				#增加修复集合
	_mend_replace = {}			#替换修复集合
	
	@classmethod
	def gs(cls, gram):
		try:
			return cls._gset_all[gram]
		except:
			print(gram)
			raise NameError

	@classmethod
	def sp(cls, s):
		try:
			return cls._spbase_all[s[0]][s]
		except:
			print(s)
			raise NameError
	
	@classmethod
	def gsin(cls, gs):
		if gs in cls._gset_all:
			return True
		return False
	
	@classmethod
	def spin(cls, sp):
		if sp[0] in cls._spbase_all:
			if sp in cls._spbase_all[sp[0]]:
				return True
		return False
	
	@classmethod
	def legal(cls, s):
		for v in s:
			if not v in cls._table_vocable:
				print('%s中有非法字符%s'%(s,v))
				return False
		return True
	
	@classmethod
	def addgs(cls, gs):
		assert isinstance(gs, gset)
		cls._gset_all[gs.name] = gs

	@classmethod
	def addsp(cls, sp):
		assert isinstance(sp, seph)
		assert len(sp.s) >= 1
		if len(sp.s) == 1:
			cls._spbase_all[sp.s[0]] = {sp.s:sp}
		else:
			cls._spbase_all[sp.s[0]][sp.s] = sp
	
	@classmethod
	def gsinit(cls):
		try:
			conn = sqlite3.connect('./data/grammar.db')
			cursor = conn.execute("select * from gset_phrase")
			v = cursor.fetchall()
			cursor = conn.execute("select * from gset_sentence")
			v.extend(cursor.fetchall())
			conn.close()
		except:
			return NameError
		while v != []:
			if cls.gsin(v[0][0]):
				v.pop(0)
				continue
			skip = True
			for g in v[0][1:]:
				if g == '' or g == None or cls.gsin(g):
					continue
				if g[0] == '(' and g[-1] == ')':
					continue
				if not (g[0] == '[' and g[-1] == ']'):
					break
				if not '|' in g:
					gsp = g[1:-1].split(' ')
					skip2 = True
					for gg in gsp:
						if gg == '' or gg == '...' or cls.gsin(gg):
							continue
						if gg[0] == 'w' and cls.gsin(gg[1:]):
							continue
						if gg[0] == '(' or gg[-1] == ')':
							continue
						break
					else:
						skip2 = False
					if skip2:
						print(v[0][0]+' 依赖 '+g)
						break
				else:
					gsp = g[1:-1].split('|')
					skip2 = True
					for gg in gsp:
						if not (gg == '' or cls.gsin(gg)):
							break
					else:
						skip2 = False
					if skip2:
						print(v[0][0]+' 依赖 '+gg)
						break
			else:
				gram = gset.prevgram(v[0][1:])
				gset(v[0][0], gram)
				v.pop(0)
				skip = False
			if skip:
				tmp = v.pop(0)
				v.append(tmp)

	@classmethod
	def spinit(cls):
		try:
			conn = sqlite3.connect('./data/grammar.db')
			cursor = conn.execute("select * from table_vocable")
		except:
			raise NameError
		for v in cursor:
			assert len(v[0]) == 1
			sp = seph(v[0])
			cls.addsp(sp)
			cls._table_vocable.add(v[0][0])
			for g in v[1:]:
				if not (g == '' or g == None):
					database.gs(g).addsp(sp)
		try:
			cursor = conn.execute("select * from table_phrase")
		except:
			raise NameError
		for v in cursor:
			assert len(v[0]) > 1
			if not database.legal(v[0]):
				raise NameError
			sp = seph(v[0])
			database.addsp(sp)
			
			for g in v[1:]:
				if not (g == '' or g == None):
					database.gs(g).addsp(sp)
		conn.close()
		
		#补充()类集合元素集
		for gram in database._gset_all:
			if gram[0] == '(' and gram[-1] == ')':
				item = gram[1:-1].split(' ')
				for sp in item:
					assert database.spin(sp)
					database.gs(gram).addsp(database.sp(sp))
				
	@classmethod
	def coreinit(cls):
		try:
			conn = sqlite3.connect('./data/grammar.db')
			cursor = conn.execute("select * from define")
		except:
			raise NameError
		
		for define in cursor:
			if not database.legal(define[0]):
				raise TypeError
			if not database.legal(define[1]):
				raise TypeError
			cls._defineDict[define[0]] = define[1]

		try:
			cursor = conn.execute("select * from zzd_keyword")
		except:
			raise NameError
		for keyword in cursor:
			if keyword[0] in cls._gset_all:
				cls._gset_key[keyword[0]] = keyword[1:]
				for sp in cls._gset_all[keyword[0]].sp:
					cls._keyword_zzd[sp.s] = keyword[1:]
					
			elif keyword[0][0] == '(' and keyword[0][-1] == ')':
				cls._gset_key[keyword[0]] = keyword[1:]
				gs = gset(keyword[0],[])
				item = keyword[0][1:-1].split(' ')
				for sp in item:
					assert database.spin(sp)
					gs.addsp(database.sp(sp))
					cls._keyword_zzd[sp] = keyword[1:]
			else:
				print(keyword[0])
				raise NameError

		try:
			cursor = conn.execute("select * from verify")
		except:
			raise TypeError
		for guest in cursor:
			cls._identifyDict[guest[0]] = guest[1]
		
		try:
			cursor = conn.execute("select * from mend_add")
		except:
			raise TypeError
		for mend in cursor:
			cls._mend_add[mend[0]] = mend[1]
		
		try:
			cursor = conn.execute("select * from mend_replace")
		except:
			raise TypeError

		for mend in cursor:
			rep = set()
			for m in mend:
				if m == '' or m == None:
					break
				rep.add(m)
				cls._mend_replace[m]=rep
		conn.close()
	
	@classmethod
	def datacheck(cls, mend):
		for gram in cls._gset_all:
			cls.checkgs(gram, False, mend)
			print('')
	
	@classmethod
	def checkgs(cls, gram, recursion, mend):
		assert database.gsin(gram)
		#检查gs的sp与子集的sp是否有重合
		gs = database.gs(gram)
		print(gs)
		print('检查集合 %s：'%gs.name)
		print('1.实例信息')
		print(gs)
		
		print('2.子集')
		if gs.child == []:
			print('没有子集')
		else:
			print('包含以下子集')
			for ch in gs.child:
				print(ch.name)

		print('3.元素')
		if len(gs.sp) == 0:
			print('没有元素')
		else:
			print('包含以下元素')
			for sp in gs.sp:
				print(sp.s)
		
		print('4. sp集合中元素是否属于子集')
		for sp in gs.sp:
			for ch in gs.child[1:]:
				if ch.contain(sp):
					print('check error. %s in %s and %s'%(sp.s, gs.name, ch.name))
					if mend:
						raise TypeError
					else:
						raise TypeError
		#检查gs的子集是否
		if recursion:
			for ch in gs.child:
				cls.checkgs(ch.name, True, mend)
		print('check success................................')

class gset:
	def __init__(self, name, child):
		self.name = name
		database.addgs(self)
		
		self.sp = set()		#明确表示的元素集合
		self.plot = {}		#明确的划分;要有名字：比如人按性别分为男人和女人

		if name[0] == '[' and name[-1] == ']':
			assert child == []
			name = name[1:-1].split(' ')
			for gram in name:
				if gram[0] == '(' and gram[-1] == ')':
					gset(gram, [])
		
		self.child = []		#子集
		for ch in child:
			if ch == '' or ch == None:
				continue
			if database.gsin(ch):
				ch = database.gs(ch)
				self.child.append(ch)
			elif ch[0] == '(' and ch[-1] == ')':
				ch = gset(ch, [])
				self.child.append(ch)
			else:
				assert ch[0] == '[' and ch[-1] == ']'
				if not '|' in ch:
					ch = gset(ch, [])
					self.child.append(ch)
				else:
					plots = ch[1:-1].split('|')
					plot = set()
					for p in plots[1:]:
						assert database.gsin(p)
						ch = gset('[%s|%s]'%(plots[0],p),[])
						self.child.append(ch)
						plot.add(ch)
					self.plot[plots[0]]=plot
	
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
		if not isinstance(sp, seph):
			raise TypeError
		if not self.contain(sp):
			self.sp.add(sp)
	
	def removesp(self, sp):
		if not isinstance(sp, seph):
			raise TypeError
		if sp not in self.sp:
			raise TypeError
		self.sp.remove(sp)
	
	
	def contain(self, sp):
		if not isinstance(sp, seph):
			raise TypeError
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
			if self.name in database._mend_add:
				phrases.insert(0,database.sp(database._mend_add[self.name]))
				return (phrases[0], phrases[1:], {self.name:phrases[0].s})
			if phrases != [] and phrases[0].s in database._mend_replace:
				for replace in database._mend_replace[phrases[0].s]:
					if database.sp(replace) in self.sp:
						phrases[0] = database.sp(replace)
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
				if sp in database._mend_add:
					phrases.insert(0,database.sp(sp))
					return (phrases[0], phrases[1:], {self.name:sp})
			if phrases != [] and phrases[0].s in database._mend_replace:
				for replace in database._mend_replace[phrases[0].s]:
					if database.sp(replace) in self.sp:
						phrases[0] = database.sp(replace)
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
			if database.gsin(gram):
				g = database.gs(gram)
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
		sp = seph(sps)
		g.addsp(sp)
		key[self.name] = sp.s
		return (sp, ress[-1][1], key)
	
	def _fensp(self, phrases, mend):
		if self.child != []:
			ress = []
			for i in range(-1,-len(self.child)-1, -1):
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

class seph:
	def __init__(self, s):
		if type(s) == str:
			self.s = s				#sting
			self.d = (s)			#迪卡尔
			self.gs = {}
			self.attr = {}
		elif type(s) == list and isinstance(s[0], seph):
			self.s = ''			#sting
			d = []
			self.gs = {}
			self.attr = {}
			for sp in s:
				self.s += sp.s
				d.append(sp.d)
			self.d = tuple(d)
		else:
			raise TypeError
	
	def setattr(self, name, value):
		return None

	def getattr(self, name):
		return None

	def addgs(self, gs):
		assert isinstance(gs, gset)
		assert not gs in self.gs
		self.gs.add(gs)

	def removegs(self, gs):
		assert isinstance(gs, gset)
		assert gs in self.gs
		self.gs.remove(gs)

	def _setattr(self, gram, name, value):
		assert self.be(gram)
		gs = database.gs(gram)
		
		if name in self.attr:
			oldgs = database.gs(self.attr[name])
			newgs = database.gs(value)
			assert newgs in gs.plot[name]
			oldgs.removesp(self)
			newgs.addsp(self)
			self.attr[name]=value
			return True
		
		for p in gs.plot:
			if p == name:
				for v in gs.plot[p]:
					if v.name == value:
						gs.removesp(self)
						v.addsp(self)
						self.attr[name]=value
						return True
		return False
		
	
	def _getattr(self, gram, name):
		assert self.be(gram)
		return '男'

	def be(self, gram):
		gs = database.gs(gram)
		if gs.contain(self) != None:
			return True
		return False

def fenci(waa, point):
	phrases = []
	con = False
	znumber =  '0123456789'
	cnumber =  '零一二三四五六七八九十百千万亿'
	zstr = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	
class seph:
	def __init__(self, s):
		if type(s) == str:
			self.s = s				#sting
			self.d = (s)			#迪卡尔
			self.gs = {}
			self.attr = {}
		elif type(s) == list and isinstance(s[0], seph):
			self.s = ''			#sting
			d = []
			self.gs = {}
			self.attr = {}
			for sp in s:
				self.s += sp.s
				d.append(sp.d)
			self.d = tuple(d)
		else:
			raise TypeError
	
	def setattr(self, name, value):
		return None
		return None
	
class seph:
	def __init__(self, s):
		if type(s) == str:
			self.s = s				#sting
			self.d = (s)			#迪卡尔
			self.gs = {}
			self.attr = {}
		elif type(s) == list and isinstance(s[0], seph):
			self.s = ''			#sting
			d = []
			self.gs = {}
			self.attr = {}
			for sp in s:
				self.s += sp.s
				d.append(sp.d)
			self.d = tuple(d)
		else:
			raise TypeError
	
	def setattr(self, name, value):
		return None

	def getattr(self, name):
		return None

	def addgs(self, gs):
		assert isinstance(gs, gset)
		assert not gs in self.gs
		self.gs.add(gs)

	def removegs(self, gs):
		assert isinstance(gs, gset)
		assert gs in self.gs
		self.gs.remove(gs)

	def _setattr(self, gram, name, value):
		assert self.be(gram)
		gs = database.gs(gram)
		
		if name in self.attr:
			oldgs = database.gs(self.attr[name])
			newgs = database.gs(value)
			assert newgs in gs.plot[name]
			oldgs.removesp(self)
			newgs.addsp(self)
			self.attr[name]=value
			return True
		
		for p in gs.plot:
			if p == name:
				for v in gs.plot[p]:
					if v.name == value:
						gs.removesp(self)
						v.addsp(self)
						self.attr[name]=value
						return True
		return False
		
	
	def _getattr(self, gram, name):
		assert self.be(gram)
		return '男'

	def be(self, gram):
		gs = database.gs(gram)
		if gs.contain(self) != None:
			return True
		return False

def fenci(waa, point):
	phrases = []
	con = False
	znumber =  '0123456789'
	cnumber =  '零一二三四五六七八九十百千万亿'
	zstr = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	
class seph:
	def __init__(self, s):
		if type(s) == str:
			self.s = s				#sting
			self.d = (s)			#迪卡尔
			self.gs = {}
			self.attr = {}
		elif type(s) == list and isinstance(s[0], seph):
			self.s = ''			#sting
			d = []
			self.gs = {}
			self.attr = {}
			for sp in s:
				self.s += sp.s
				d.append(sp.d)
			self.d = tuple(d)
		else:
			raise TypeError
	
	def setattr(self, name, value):
		return None

	def getattr(self, name):
		return None

	def addgs(self, gs):
		assert isinstance(gs, gset)
		assert not gs in self.gs
		self.gs.add(gs)

	def removegs(self, gs):
		assert isinstance(gs, gset)
		assert gs in self.gs
		self.gs.remove(gs)

	def _setattr(self, gram, name, value):
		assert self.be(gram)
		gs = database.gs(gram)
		
		if name in self.attr:
			oldgs = database.gs(self.attr[name])
			newgs = database.gs(value)
			assert newgs in gs.plot[name]
			oldgs.removesp(self)
			newgs.addsp(self)
			self.attr[name]=value
			return True
		
		for p in gs.plot:
			if p == name:
				for v in gs.plot[p]:
					if v.name == value:
						gs.removesp(self)
						v.addsp(self)
						self.attr[name]=value
						return True
		return False
		
	def _getattr(self, gram, name):
		assert self.be(gram)
		return '男'

	def be(self, gram):
		gs = database.gs(gram)
		if gs.contain(self) != None:
			return True
		return False

def fenci(waa, point):
	phrases = []
	con = False
	znumber =  '0123456789'
	cnumber =  '零一二三四五六七八九十百千万亿'
	zstr = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	zpoint = '，。,.！!？?'
	if not database.legal(waa):
		raise
	while waa != '':
		if waa[0] == ' ':
			waa = waa[1:]
		elif waa[0] in znumber:
			s = waa[0]
			waa = waa[1:]
			while waa != '' and waa[0] in znumber:
				s += waa[0]
				waa = waa[1:]
			sp = seph(s)
			database.gs('数').addsp(sp)
			phrases.append(sp)
		elif waa[0] in cnumber:
			s = waa[0]
			waa = waa[1:]
			while waa != '' and waa[0] in cnumber:
				s += waa[0]
				waa = waa[1:]
			sp = seph(s)
			database.gs('汉语数').addsp(sp)
			phrases.append(sp)
		elif waa[0] in zstr[10:]:
			s = waa[0]
			waa = waa[1:]
			while waa != '' and waa[0] in zstr:
				s += waa[0]
				waa = waa[1:]
			sp = seph(s)
			database.gs('字符串').addsp(sp)
			phrases.append(sp)
		elif waa[0:2] == '!=':
			phrases.append(database.sp('!='))
			waa = waa[2:]
		elif waa[0] in zpoint:
			if point:
				phrases.append(database.sp(waa[0]))
			waa = waa[1:]
		else:
			for i in range(min(8,len(waa)),0,-1):
				if database.spin(waa[0:i]):
					phrases.append(database.sp(waa[0:i]))
					waa = waa[i:]
					break
	return phrases
	
def main():
	print('db')
	database.gsinit()
	database.spinit()
	database.coreinit()

if __name__ == '__main__':
	main()
