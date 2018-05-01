#!/usr/bin/python3 -B

import sets
import element

_func_all = {}				#所有函数
_gset_all = {}				#所有集合
_table_vocable = {' '}		#所有字符
_spbase_all = {}			#所有语句
_identifyDict = {}			#身份认证
_gset_key = {}				#关键集合
_keyword_zzd = {}			#关键语句
_mend_add = {}				#增加修复集合
_mend_replace = {}			#替换修复集合

def getgs(g):
	try:
		return _gset_all[g]
	except:
		print(g)
		raise NameError

def getfn(f):
	try:
		return _func_all[f]
	except:
		print(f)
		raise NameError

def getsp(s):
	try:
		return _spbase_all[s[0]][s]
	except:
		print(s)
		raise NameError

def getsp_ok(s):
	if spin(s):
		return _spbase_all[s[0]][s]
	else:
		sp = element.seph(s)
		sp._fenci(False)
		return sp

def gsin(g):
	return True if g in _gset_all else False

def gsin(g):
	return True if g in _gset_all else False

def fnin(f):
	return True if f in _func_all else False
	
def spin(s):
	if s[0] in _spbase_all:
		if s in _spbase_all[s[0]]:
			return True
	return False
	
def legal(s):
	for v in s:
		if not v in _table_vocable:
			print('%s中有非法字符%s'%(s,v))
			return False
	return True

def fix(s):
	res = ''
	for v in s:
		if v in _table_vocable:
			res += v
	return res
	
def addgs(gs):
	_gset_all[gs.name] = gs

def addfn(fn):
	_func_all[fn.name] = fn

def addsp(sp):
	assert len(sp.s) >= 1
	if len(sp.s) == 1:
		_spbase_all[sp.s[0]] = {sp.s:sp}
	else:
		_spbase_all[sp.s[0]][sp.s] = sp

def checksp(sp):
	print('检查SP %s'%sp)
	sp = getsp(sp)
	print('1.实例信息')
	print(sp)
	if len(sp.gs) == 0:
		print('2.不属于任何集合')
	else:
		print('2.属合下列集合:')
		ancestor = []
		for gs in sp.gs:
			ancestor.extend(sets.gset.get_ancset(gs))
		ancestor=list(set(ancestor))
		for gs in ancestor:
			print(gs.name)
		for gs in sp.gs:
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
	
def checkgs(gram, recursion):
	assert gsin(gram)
	#检查gs的sp与子集的sp是否有重合
	gs = getgs(gram)
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
			checkgs(ch.name, True)
	print('check success')
	
def main():
	print('gdata')

if __name__ == '__main__':
	main()
