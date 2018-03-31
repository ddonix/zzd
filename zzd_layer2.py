# coding: utf-8

class zzdLayer2:
	def __init__(self, corelayer1):
		self.corelayer1 = corelayer1
	
	def inputs(self, sen):
		outs = self.corelayer1.inputs(sen)
		return outs
