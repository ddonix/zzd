#!/usr/bin/python3 -B
import sqlite3
import copy
import sets
import element
import gdata
import sys

#对子集进行排序，子集项多的在后
#原始子集在前的在前
def prevgram(gram):
	tmp = []
	for g in gram.split('~'):
		tmp.extend(_prevgram(g))
	tmp2 = []
	for t in tmp:
		if t in tmp2:
			continue
		for i in range(0,len(tmp2),1):
			if len(t) < len(tmp2[i]):
				tmp2.insert(i, t)
				break
			if len(t) == len(tmp2[i]):
				tmp2.insert(i+1, t)
				break
		else:
			tmp2.append(t)
	res = []
	for t in tmp2:
		if type(t) == str:
			r = t
		else:
			r = '[%s'%t[0]
			for s in t[1:]:
				r += ' %s'%s
			r += ']'
		res.append(r)
	return res
	
def _prevgram(gram):
	if gram == '' or gram == None:
		return []
	if not (gram[0] == '[' and gram[-1] == ']'):
		return [gram]
	gram = gram[1:-1].split(' ')
	res = []
	__prevgram(gram, res)
	return res

def __prevgram(gram, res):
	if not gram:
		return
	if len(gram) == 1:			#[w宾语] [谓语]
		if gram[0][0] == 'w':
			res.append([])
			res.append([gram[0][1:]])
		else:
			res.append([gram[0]])
		return
	__prevgram(gram[1:], res)	#[[w宾语], [谓语]]
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

#a是A的元素
def	add_database_a_in_A(sp_a, gs_A):
	try:
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.cursor()
		if len(sp_a) > 1:
			sql = '''select * from table_phrase where name=(?)'''
		else:
			sql = '''select * from table_vocable where name=(?)'''
		cursor.execute(sql, (sp_a,))
		conn.commit()
		info = cursor.fetchall()
		print(info)
		if not info:
			if len(sp_a) > 1:
				sql = '''insert into table_phrase (name, gs) values (?, ?)'''
			else:
				sql = '''insert into table_vocable (name, gs) values (?, ?)'''
    		# 把数据保存到name username和 id_num中
			cursor.execute(sql, (sp_a,gs_A))
		else:
			gs = '%s~%s'%(info[0][1],gs_A) if info[0][1] else gs_A
			if len(sp_a) > 1:
				sql = '''update table_phrase set gs=(?) where name=(?)'''
			else:
				sql = '''update table_vocable set gs=(?) where name=(?)'''
			cursor.execute(sql, (gs, sp_a))
		conn.commit()
		conn.close
	except:
		print('写入数据库失败')
		return False
	print('写入数据库成功')
	return True

#A是B的子集
def	add_database_A_in_B(gs_A, gs_B):
	try:
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.cursor()
		sql = '''select * from gset_phrase where name=(?)'''
		cursor.execute(sql, (gs_B,))
		conn.commit()
		info = cursor.fetchall()
		print(info)
		if not info:
			sql = '''insert into gset_phrase (name, subset) values (?, ?)'''
    		# 把数据保存到name username和 id_num中
			cursor.execute(sql, (gs_B,gs_A))
		else:
			gs = '%s~%s'%(info[0][1],gs_A) if info[0][1] else gs_A
			sql = '''update gset_phrase set subset=(?) where name=(?)'''
			cursor.execute(sql, (gs, gs_B))
		conn.commit()
		conn.close
	except:
		print('写入数据库失败')
		return False
	print('写入数据库成功')
	return True


#增加元素a属于集合A这条信息。
#成功返回0，无用返回1，矛盾返回2.
#原则：1.不能矛盾。苏格拉底原先是男人，现在不能是女人
#原则：2.不能无用。苏格拉底原先是男人，现在不能是人
def add_information_1(sp_a, gs_A):
	if not gdata.spin(sp_a):
		element.seph(sp_a)
	if not gdata.gsin(gs_A):
		sets.gset(gs_A)
	sp = gdata.getsp(sp_a)
	gs = gdata.getgs(gs_A)
	res = _add_information_1(sp, gs)
	return res

def _add_information_1(sp, gs):
	assert isinstance(sp, element.seph) and isinstance(gs, sets.gset)
	for g in list(sp.gs):
		#判断是否无用
		if sets.gset.involved_in(g, gs):
			return (1, '%s是%s,而%s是%s的子集'%(sp.s,g.name,g.name,gs.name))
		#判断是否删除
		if sets.gset.involved_in(gs, g):
			g._removesp(sp)
			sp._removegs(g)
		#判断是否矛盾
		if sets.gset.conflict(g, gs):
			return (2, '%s与%s不相容'%(g.name,gs.name))
	gs._addsp(sp)
	sp._addgs(gs)
	if gs.name == '集合' and not gdata.gsin(sp.s):
		sets.gset(sp.s)
	return (0, '')
	
#x是集合:	x包含于集合A
#x是划分: 	x是集合A的划分
#成功返回0，无用返回1，矛盾返回2.
#原则：1.不能矛盾。鲸鱼原先是哺乳动物，现在不能鸟.因为鸟和哺乳动物冲突.
#原则：2.不能无用。鲸鱼原先是哺乳动物，现在不能是脊椎动物。因为哺乳动物都是脊椎动物.
def add_information_2(x, gs_A):
	assert gdata.gsin(gs_A)
	gsA = gdata.getgs(gs_A)
	if '|' in x:
		if ':' in x:						#[性别:男人|女人]
			plots = x[1:-1].split(':')[1].split('|')
		else:								#[奇数|偶数]
			plots = x[1:-1].split('|')
		for ch in plots:
			res = gsA.add_child(ch)
			if res[0] > 0:
				return res
		else:
			gsA.add_plot(x)
			return [0]
	else: 
		return gsA.add_child(x)

def gsinit():
	try:
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.execute("select * from gset_phrase")
		grammar = cursor.fetchall()
		cursor = conn.execute("select * from gset_sentence")
		grammar.extend(cursor.fetchall())
		conn.close()
	except:
		return NameError
	for v in grammar:
		if not v[0]:
			continue
		if not gdata.gsin(v[0]):
			gs = sets.gset(v[0])
		if not v[1]:
			continue
		gram = prevgram(v[1])
		for g in gram:
			add_information_2(g, v[0])


def spinit():
	try:
		conn = sqlite3.connect('./data/grammar.db')
		cursor = conn.execute("select * from table_vocable")
	except:
		raise NameError
	for v in cursor:
		assert len(v[0]) == 1
		sp = element.seph(v[0])
		gdata._table_vocable.add(v[0][0])
		for g in v[1].split('~') if v[1] else []:
			if not (g == '' or g == None):
				add_information_1(v[0], g)
	try:
		cursor = conn.execute("select * from table_phrase")
	except:
		raise NameError
	for v in cursor:
		assert len(v[0]) > 1
		if not gdata.legal(v[0]):
			print(v)
			raise NameError
		sp = element.seph(v[0])
		for g in v[1].split('~') if v[1] else []:
			if not (g == '' or g == None):
				add_information_1(v[0], g)
	conn.close()
		
	#补充所有集合类元素集,例如：集合语句是集合
	#补充()类集合里面的元素
	for gram in gdata._gset_all:
		if gram[0] != '[' and gram[0] != '(':
			add_information_1(gram, '集合')
		if gram[0] == '(' and gram[-1] == ')':
			item = gram[1:-1].split(' ')
			for sp in item:
				add_information_1(sp, gram)
	

			
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
			for sp in gdata._spbase_all:
				for s in gdata._spbase_all[sp]:
					if gdata._spbase_all[sp][s].be(keyword[0]):
						gdata._keyword_zzd[s] = keyword[1:]
		elif keyword[0][0] == '(' and keyword[0][-1] == ')':
			gs = sets.gset(keyword[0])
			gdata._gset_key[keyword[0]] = keyword[1:]
			item = keyword[0][1:-1].split(' ')
			for sp in item:
				add_information_1(sp, keyword[0])
				gdata._keyword_zzd[sp] = keyword[1:]
		else:
			print(keyword[0])
			raise NameError
	
	try:
		cursor = conn.execute("select * from verify")
	except:
		raise TypeError
	for guest in cursor:
		gdata._identifyDict[guest[0]] = guest[1]
		
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
			if gdata.spin(s):
				sp = gdata.getsp(s)
			else:
				sp = element.seph(s)
				gs = gdata.getgs('数')
				sp._addgs(gs)
				gs._addsp(sp)
			phrases.append(sp)
		elif waa[0] in cnumber:
			s = waa[0]
			waa = waa[1:]
			while waa != '' and waa[0] in cnumber:
				s += waa[0]
				waa = waa[1:]
			if gdata.spin(s):
				sp = gdata.getsp(s)
			else:
				sp = element.seph(s)
				gs = gdata.getgs('汉语数')
				sp._addgs(gs)
				gs._addsp(sp)
			phrases.append(sp)
		elif waa[0] in zstr[10:]:
			s = waa[0]
			waa = waa[1:]
			while waa != '' and waa[0] in zstr:
				s += waa[0]
				waa = waa[1:]
			if gdata.spin(s):
				sp = gdata.getsp(s)
			else:
				sp = element.seph(s)
				gs = gdata.getgs('汉语数')
				sp._addgs(gs)
				gs._addsp(sp)
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
	
def main(a1, a2):
	print('db')
	gsinit()
	spinit()
	coreinit()

	if a1 == 'sp':
		gdata.checksp(a2)
	else:
		gdata.checkgs(a2, True)

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])

'''
	f= open('千字文','r')
	book=f.read()
	f.close()
	for v in book:
		if v != '，' and v != '。' and v != ' ' and v != '\n':
			if v not in gdata._table_vocable:
				add_database_a_in_A(v, '普通汉字')
'''
