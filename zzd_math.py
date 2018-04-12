#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import grammar

dict0={u'0':0,u'1':1,u'2':2, u'3':3,u'4':4, u'5':5, u'6':6, u'7':7, u'8':8,u'9':9, u'+':10, u'-':11}
dict1={u'零':0,u'一':1,u'二':2, u'三':3,u'四':4, u'五':5, u'六':6, u'七':7, u'八':8,u'九':9}
dict2={u'十':10,u'百':100,u'千':1000,u'万':10000}

def transNumber(data):
	if dict0.get(data[0]):		#12,-123,+123
		return int(data)
	if data[0] == u'负':
		sign = -1
		data = data[1:]
	elif data[0] == u'正':
		sign = 1
		data = data[1:]
	else:
		sign = 1
	
	if len(data) == 1:			#一，二，十
		return (10 if data[0] == u'十' else dict1[data[0]])*sign
		
	if data[0] == u'十':		#十五,十六
		res = 10+dict1[data[1]]
		return res*sign
		
	if not dict2.get(data[1]):	#五六八,二四
		res = u''
		for d in data:
			res += unicode(dict1[d])
		return int(res)*sign
	
	res = 0						#三百二十，四百五十六
	for i,d in enumerate(data):
		r=dict2.get(d)
		if r:
			res += r*dict1[data[i-1]]
	r = dict1.get(data[-1])
	if r:
		res += r
	return res*sign


def c2math(phrases):
	res = []
	tran1 = {u'加':u'+',u'加上':'+', u'减':u'-',u'减去':u'-','乘以':u'*', u'除以':u'/', u'大于':u'>',u'小于':u'<',u'等于':u'==',u'大于等于':'>=',u'小于等于':u'<=', u'不等于':u'!='}
	tran2 = {u'乘':'*',u'除':u'/'}
	x = False
	for ph in phrases:
		if ph.be(u'汉语变量'):
			x = True
			break
	for ph in phrases:
		if ph.be(u'汉语数'):
			res.append(unicode(transNumber(ph.s)))
		if ph.be(u'汉语运算符'):
			if ph.s in tran1:
				res.append(tran1[ph.s])
			else:
				res.append(tran1[ph.s])
		if ph.be(u'汉语赋值符'):
			if x:
				res.append(u'=')
			else:
				res.append(u'==')
		if ph.be(u'汉语变量'):
			res.append(u'x')
		if ph.be(u'数'):
			res.append(ph.s)
	return u''.join(res)


def main():
	print('zzd_math')
	grammar.gsetinit()
	grammar.spinit()

	phrases = grammar._fenci(u'十加上三十等于几', False)
	for p in phrases:
		print p.s
	res = c2math(phrases)
	print res

if __name__ == '__main__':
	main()
'''	
	sheet = book.sheet_by_name('grammar_sentence')
	nrows = sheet.nrows
	for i in range(nrows):
		v = sheet.row_values(i)
		g = gset(v[0], v[1:])
		gset_all[v[0]] = g
		if v[0][0] == 'S':
			gset_zzd.append([v[0], g])
	book.release_resources()
'''	
'''	
	phrases = _fenci(u'认证身份，口令是,认证123456', True)
	for p in phrases:
		print p.s
	g = gset_all[u'认证语句']
	sp = g._fensp(phrases, True)
	print sp[0]
	print sp[1]
	for k in sp[2]:
		print k+'='+sp[2][k]
'''
'''
print transNumber(u'正一二三')
print transNumber(u'负一二三')
print transNumber(u'一二三')
print transNumber(u'一千二百零三')
print transNumber(u'负十五')
print transNumber(u'正十')
print transNumber(u'八')
print transNumber(u'十')
print transNumber(u'负十')
print transNumber(u'十五')
print transNumber(u'正十五')
print transNumber(u'正三百五十五')
print transNumber(u'负四万三百五十五')
print transNumber(u'四万三百五十五')
'''
