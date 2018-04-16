import zzd_unity
import zzd_core1
import sys
import time
#语音的层级
#free:自由表达的语言，有各种风格，例如幽默、严肃、简练、罗嗦.例如：一加一是不是比二大呢？(这里的呢字在表义上是多余的)
#2:规范汉语，汉语的规范表达。例如：1+1大于2，是吗？
#1:格式化语言，由zzd进行处理。例如：solv:1+1>2
#0:核心语言：暂时没有定义，留待以后扩展

class zzd(zzd_unity.unity):
	def __init__(self, show):
		zzd_unity.unity.__init__(self)
		self.core = zzd_core1.zzdcore1()
		self.show = show
	
	@classmethod
	def init(cls):
		zzd_core1.zzdcore1.init()
	
	def input(self, sour, waa):
		self.core.input(sour,waa)
	
	def output(self, dest, waa):
		print(waa[0][0])
		print(waa[0][1])
		print(waa[1])
		self.show(waa[0][1], waa[1])
		dest.input(self, dest, waa[1])

	def work(self):
		working = True
		while working:
			print('zzd working')
			waa = getoutput(self)
			self.output(self.core.friend, waa)
			if waa[0][1] == u'再见' or waa[0][1] == '拜拜':
				working = False

	def getoutput(self):
		waa = self.core.inputs(sour, waa)
		return waa
