#!/usr/bin/python -B
# -*- coding: UTF-8 -*-

dict0={u'0':0,u'1':1,u'2':2, u'3':3,u'4':4, u'5':5, u'6':6, u'7':7, u'8':8,u'9':9, u'+':10, u'-':11}
dict1={u'零':0,u'一':1,u'二':2, u'三':3,u'四':4, u'五':5, u'六':6, u'七':7, u'八':8,u'九':9}
dict2={u'十':10,u'百':100,u'千':1000,u'万':10000,u'亿':100000000}

def transNumber(data):
	if dict0.get(data[0]):
		return int(data)
	if not dict2.get(data[0]):
		res = u''
		for d in data:
			if d == u'正':
				res += u'+'
			elif d == u'负':
				res += u'-'
			else:
				res += unicode(dict1[d])
		return int(res)
	
	if data[0] == u'负':
		sign = -1
		data = data[1:]
	elif data[0] == u'正':
		sign = 1
		data = data[1:]
	else:
		sign = 1
	res = 0
	for d in data:
		r = dict1.get(d)
		if r:
			res += r
		else:
			res = res*dict2[d]
	return res*sign

#print transNumber(u'正一二三')
#print transNumber(u'负一二三')
#print transNumber(u'一二三')
print transNumber(u'一千二百零三')
print transNumber(u'负一千二百零三')
