#!/usr/bin/python3 -B
import sqlite3
import copy
import ipdb
import sets
import element
import gdata

def gsinit():
	try:
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.execute("select * from gset_phrase")
		v = cursor.fetchall()
		cursor = conn.execute("select * from gset_set")
		v.extend(cursor.fetchall())
		cursor = conn.execute("select * from gset_sentence")
		v.extend(cursor.fetchall())
		conn.close()
	except:
		return NameError
	while v != []:
		if gdata.gsin(v[0][0]):
			v.pop(0)
			continue
		skip = True
		for g in v[0][1:]:
			if g == '' or g == None or gdata.gsin(g):
				continue
			if g[0] == '(' and g[-1] == ')':
				continue
			if not (g[0] == '[' and g[-1] == ']'):
				break
			if not '|' in g:
				gsp = g[1:-1].split(' ')
				skip2 = True
				for gg in gsp:
					if gg == '' or gg == '.' or gg == '...' or gdata.gsin(gg):
						continue
					if gg[0] == 'w' and gdata.gsin(gg[1:]):
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
				skip2 = True
				if g.find(':') == -1:
					gsp = g[1:-1].split('|')
					for gg in gsp:
						if not (gg == '' or (gg[0]=='(' and gg[-1]==')') or gdata.gsin(gg)):
							break
					else:
						skip2 = False
				else:
					gsp = g[g.find(':')+1:-1].split('|')
					for gg in gsp:
						if not (gg == '' or (gg[0]=='(' and gg[-1]==')') or gdata.gsin('%s%s'%(gg,v[0][0]))):
							break
					else:
						skip2 = False
				if skip2:
					print(v[0][0]+' 依赖 '+gg)
					break
		else:
			gram = sets.gset.prevgram(v[0][1:])
			sets.gset(v[0][0], gram)
			v.pop(0)
			skip = False
		if skip:
			tmp = v.pop(0)
			v.append(tmp)

def spinit():
	try:
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.execute("select * from table_vocable")
	except:
		raise NameError
	for v in cursor:
		assert len(v[0]) == 1
		sp = element.seph(v[0])
		gdata.addsp(sp)
		gdata._table_vocable.add(v[0][0])
		for g in v[1:]:
			if not (g == '' or g == None):
				gs = gdata.getgs(g)
				gs.addsp(sp)
				sp.addgs(gs)
	try:
		cursor = conn.execute("select * from table_phrase")
	except:
		raise NameError
	for v in cursor:
		assert len(v[0]) > 1
		if not gdata.legal(v[0]):
			raise NameError
		sp = element.seph(v[0])
		gdata.addsp(sp)
		
		for g in v[1:]:
			if not (g == '' or g == None):
				gs = gdata.getgs(g)
				gs.addsp(sp)
				sp.addgs(gs)
	conn.close()
		
	#补充()类集合元素集
	for gram in gdata._gset_all:
		if gram[0] == '(' and gram[-1] == ')':
			item = gram[1:-1].split(' ')
			for sp in item:
				assert gdata.spin(sp)
				gdata.getgs(gram).addsp(gdata.getsp(sp))
				gdata.getsp(sp).addgs(gdata.getgs(gram))
			
def coreinit():
	try:
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.execute("select * from define")
	except:
		raise NameError
	
	for define in cursor:
		if not gdata.legal(define[0]):
			raise TypeError
		if not gdata.legal(define[1]):
			raise TypeError
		gdata._defineDict[define[0]] = define[1]

	try:
		cursor = conn.execute("select * from zzd_keyword")
	except:
		raise NameError
	for keyword in cursor:
		if keyword[0] in gdata._gset_all:
			gdata._gset_key[keyword[0]] = keyword[1:]
			for sp in gdata._gset_all[keyword[0]].sp:
				gdata._keyword_zzd[sp.s] = keyword[1:]
					
		elif keyword[0][0] == '(' and keyword[0][-1] == ')':
			gdata._gset_key[keyword[0]] = keyword[1:]
			gs = sets.gset(keyword[0],[])
			item = keyword[0][1:-1].split(' ')
			for sp in item:
				assert gdata.spin(sp)
				gs.addsp(gdata.getsp(sp))
				gdata._keyword_zzd[sp] = keyword[1:]
		else:
			print(keyword[0])
			raise NameError

	try:
		cursor = conn.execute("select * from verify")
	except:
		raise TypeError

		_identifyDict[guest[0]] = guest[1]
		
	try:
		cursor = conn.execute("select * from mend_add")
	except:
		raise TypeError
	for mend in cursor:
		gdata._mend_add[mend[0]] = mend[1]
	
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
			gdata._mend_replace[m]=rep
	conn.close()
	
#增加元素a属于集合A这条信息。
#原则：1.不能矛盾。苏格拉底原先是男人，现在不能是女人，否则抛出异常
#原则：2.不能重复。苏格拉底原先是男人，现在不能是人，否则返回False.
def add_information_1(sp_a, gs_A):
	assert spin(sp_a) and gdata.gsin(gs_A)
	sp = gdata.getsp(sp_a)
	gs = gdata.getgs(gs_A)
	return _add_information_1(sp, gs)
	
def _add_information_1(sp, gs):
	assert isinstance(sp, element.seph) and isinstance(gs, sets.gset)
	descendant = get_descendant(gs)
	for gs in descendant:
		if gs in sp.gs:
			return False
	return True
	
def add_information_2(gs_A, gs_B):#集合A包含于集合B
	assert gdata.gsin(gs_A) and gsin(gs_B)
		
	
def checksp(sp):
	print('检查SP %s'%sp)
	sp = gdata.getsp(sp)
	print('1.实例信息')
	print(sp)
	if len(sp.gs) == 0:
		print('2.不属于任何集合')
	else:
		print('2.属合下列集合:')
		ancestor = []
		for gs in sp.gs:
			ancestor.extend(getancestor(gs))
		for gs in ancestor:
			print(gs.name)
	
def get_ancestor(gs):
	res = [gs]
	res.extend(gs.father)
	for fa in gs.father:
		res.extend(get_ancestor(fa))
	res = list(set(res))
	return res
	
def get_descendant(gs):
	res = [gs]
	res.extend(gs.child)
	for ch in gs.child:
		res.extend(get_descendant(ch))
	res = list(set(res))
	return res
	
def checkgs(gram, recursion, mend):
	assert gdata.gsin(gram)
	#检查gs的sp与子集的sp是否有重合
	gs = gdata.getgs(gram)
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
	
	print('3.父集')
	if gs.father == []:
		print('没有父集')
	else:
		print('包含于以下父集')
		for fa in gs.father:
			print(fa.name)

	print('4.元素')
	if len(gs.sp) == 0:
		print('没有元素')
	else:
		print('包含以下元素')
		for sp in gs.sp:
			print(sp.s)
	
	#递归检查gs的子集
	if recursion:
		for ch in gs.child:
			checkgs(ch.name, True, mend)
	print('check success')

def fenci(waa, point):
	phrases = []
	con = False
	znumber =  '0123456789'
	cnumber =  '零一二三四五六七八九十百千万亿'
	zstr = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	zpoint = '，。,.！!？?'
	if not gdata.legal(waa):
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
			sp = element.seph(s)
			gdata.getgs('数').addsp(sp)
			phrases.append(sp)
		elif waa[0] in cnumber:
			s = waa[0]
			waa = waa[1:]
			while waa != '' and waa[0] in cnumber:
				s += waa[0]
				waa = waa[1:]
			sp = element.seph(s)
			gdata.getgs('汉语数').addsp(sp)
			phrases.append(sp)
		elif waa[0] in zstr[10:]:
			s = waa[0]
			waa = waa[1:]
			while waa != '' and waa[0] in zstr:
				s += waa[0]
				waa = waa[1:]
			sp = element.seph(s)
			gdata.getgs('字符串').addsp(sp)
			phrases.append(sp)
		elif waa[0:2] == '!=':
			phrases.append(gdata.getsp('!='))
			waa = waa[2:]
		elif waa[0] in zpoint:
			if point:
				phrases.append(gdata.getsp(waa[0]))
			waa = waa[1:]
		else:
			for i in range(min(8,len(waa)),0,-1):
				if gdata.spin(waa[0:i]):
					phrases.append(gdata.getsp(waa[0:i]))
					waa = waa[i:]
					break
	return phrases
	
def main():
	print('db')
	gsinit()
	spinit()
	coreinit()
	checksp('苏格拉底')
#	add_information_1('苏格拉底', '人')
#	checksp('苏格拉底')

if __name__ == '__main__':
	main()
