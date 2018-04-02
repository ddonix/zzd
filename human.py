#!/usr/bin/python 
# -*- coding:utf-8 -*- 
import unity

class human(unity.unity):
	def __init__(self, core):
		unity.unity.__init__(self)
		self.core = core
    
	def act(self, dest, waa_out):
		return waa_out
	
	def echo(self, sour, waa_in):
		return waa_in
    
	def forword(self, dest, waa_out):
		return waa_out
