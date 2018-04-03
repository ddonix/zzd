#!/usr/bin/python -B
# -*- coding: UTF-8 -*-

dict0={u'0':0,u'1':1,u'2':2, u'3':3,u'4':4, u'5':5, u'6':6, u'7':7, u'8':8,u'9':9}
dict1={u'零':0,u'一':1,u'二':2, u'三':3,u'四':4, u'五':5, u'六':6, u'七':7, u'八':8,u'九':9,
		u'十':10,u'百':100,u'千':1000,u'万':1000}

def transNumber(data):
	res = 0
	for d in data:
		res +=dict0[d]
	return res

print transNumber(u'123')
