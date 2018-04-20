#!/usr/bin/python3 -B

import sets
import element

_gset_all = {}				#所有集合
_spbase_all = {}			#所有语句
_table_vocable = {' '}		#所有字符
	
_identifyDict = {}			#身份认证
_defineDict = {}			#定义
_gset_key = {}				#关键集合
_keyword_zzd = {}			#关键语句
_mend_add = {}				#增加修复集合
_mend_replace = {}			#替换修复集合

def getgs(gram):
	try:
		return _gset_all[gram]
	except:
		print(gram)
		raise NameError

def getsp(s):
	try:
		return _spbase_all[s[0]][s]
	except:
		print(s)
		raise NameError
	
def gsin(gs):
	if gs in _gset_all:
		return True
	return False
	
def spin(sp):
	if sp[0] in _spbase_all:
		if sp in _spbase_all[sp[0]]:
			return True
	return False
	
def legal(s):
	for v in s:
		if not v in _table_vocable:
			print('%s中有非法字符%s'%(s,v))
			return False
	return True
	
def addgs(gs):
	assert isinstance(gs, sets.gset)
	_gset_all[gs.name] = gs

def addsp(sp):
	assert isinstance(sp, element.seph)
	assert len(sp.s) >= 1
	if len(sp.s) == 1:
		_spbase_all[sp.s[0]] = {sp.s:sp}
	else:
		_spbase_all[sp.s[0]][sp.s] = sp
	
def main():
	print('gdata')

if __name__ == '__main__':
	main()
