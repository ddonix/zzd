#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import unity

class human(unity.unity):
	symboltabel = None
	def __init__(self):
		unity.unity.__init__(self)
		self.waalist = []
    
	@classmethod
	def init(cls):
		f=open('./txt/human_symbols.txt', 'r')
		tmp = f.read()
		f.close()
		
		tmp = tmp.replace('\n', '')
		tmp = tmp.decode('utf8')
		tmp = set(tmp)
		human.symboltabel = u''
		for item in tmp:
			human.symboltabel += item
    
	def act(self, dest, waa_out):
		res = dest.echo(self, waa_out)
		self.waalist.append([waa_out, res])
		return None
	
	def echo(self, sour, waa_in):
		raise NotImplementedError
    
	def forword(self, dest, waa_out):
		return waa_out
