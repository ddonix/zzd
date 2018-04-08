# -*- coding:utf-8 -*- 
import zzd_unity
import zzd_core0
import zzd_core1

#语音的层级
#free:自由表达的语言，有各种风格，例如幽默、严肃、简练、罗嗦.例如：一加一是不是比二大呢？(这里的呢字在表义上是多余的)
#2:规范汉语，汉语的规范表达。例如：1+1大于2，是吗？
#1:格式化语言，由zzd进行处理。例如：solv:1+1>2
#0:核心语言：暂时没有定义，留待以后扩展

class zzd(zzd_unity.unity):
	def __init__(self, show):
		zzd_unity.unity.__init__(self)
		self.show = show
		self.core = zzd_core1.zzdcore1()
	
	@classmethod
	def init(cls):
		zzd_core1.zzdcore1.init()
		
	def echo(self, sour, waa_in):
		waa = self._trans_free_2(waa_in)
		waa_out = self.core.inputs(sour, waa)
		waa_out = self._trans_2_free(waa_out)
		self.show(waa_out)
		return waa_out
    
	def act(self, dest, waa_out):
		return None
	
	def forword(self, dest, waa_out):
		return None
	
	def _trans_free_2(self, waa):
		return waa
	
	def _trans_2_free(self, waa):
		return waa
