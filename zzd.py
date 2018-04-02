# -*- coding:utf-8 -*- 
import unity
import zzd_layer0
import zzd_layer1
import zzd_layer2

class zzd(unity.unity):
	def __init__(self, core, show):
		unity.unity.__init__(self)
		self.core = core
		self.show = show
		self.corelayer0 = zzd_layer0.zzdLayer0()
		self.corelayer1 = zzd_layer1.zzdLayer1(self.corelayer0)
		self.corelayer2 = zzd_layer2.zzdLayer2(self.corelayer1)
    
	def act(self, dest, waa_out):
		return waa_out
    
	def echo(self, sour, waa_in):
		waa_out = waa_in
		self.show(waa_out)
		return waa_out
    
	def forword(self, dest, waa_out):
		return waa_out
