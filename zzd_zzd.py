#!/usr/bin/python3 -B

import zzd_unity
import zzd_core1
import sys
import time

#除input函数运行在xhh线程，其他函数运行在zhd线程.
class zzd(zzd_unity.unity):
	def __init__(self, show):
		zzd_unity.unity.__init__(self)
		self.core = zzd_core1.zzdcore1()
		self.show = show
		
		self.working = True
		self.root = True
	
	@classmethod
	def init(cls):
		zzd_core1.zzdcore1.init()
	
	#运行在xhh线程
	def input(self, sour, waa):
		self.core.input(sour,waa)
	
	def output(self, dest, waa):
		print('waa[0]',waa[0])
		print('waa[1]',waa[1])
		self.show(waa[0], waa[1])
		dest.input(self, waa[0])

	def work(self):
		while self.working and self.root:
			print('zzd working',time.time())
			waa = self.core.getoutput()
			if waa == None:
				time.sleep(1)
			else:
				self.output(self.core.friend, waa)
				if waa[0] == u'再见！' or waa[0] == '拜拜！':
					self.working = False

def main():
	print('zzd_zzd')
	zzd.init()

if __name__ == '__main__':
	main()
