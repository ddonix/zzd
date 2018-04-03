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
		f=open('human_symbols.txt', 'r')
		human.symboltabel = f.read()
		f.close()
		human.symboltabel = human.symboltabel.replace('\n', '')
		human.symboltabel = human.symboltabel.decode('utf8')
    
	def act(self, dest, waa_out):
		res = dest.echo(self, waa_out)
		self.waalist.append([waa_out, res])
		return None
	
	def echo(self, sour, waa_in):
		raise NotImplementedError
    
	def forword(self, dest, waa_out):
		return waa_out
