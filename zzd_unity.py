# -*- coding:utf-8 -*- 

class unity:
	def __init__(self):
		self.core = None
	
	def act(self, dest, waa_out):
		raise NotImplementedError
	
	def echo(self, sour, waa_in):
		raise NotImplementedError
    
	def forword(self, dest, waa_out):
		raise NotImplementedError
