#!/usr/bin/python -B
# -*- coding: UTF-8 -*-

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
