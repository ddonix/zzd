#!/usr/bin/python3 -B

import zzd_unity
import zzd_core1
import sys
import time

class zzd(zzd_unity.unity):
	def __init__(self, show, semaphore):
		zzd_unity.unity.__init__(self)
		self.core = zzd_core1.zzdcore1(semaphore)
		self.show = show
		
		self.working = True
		self.master = True
	
	@classmethod
	def init(cls):
		zzd_core1.zzdcore1.init()
	
	#human主进程调用
	def input(self, sour, waa):
		self.core.input(sour,waa)
	
	def output(self, dest, waa):
		print(waa[0][0])
		print(waa[0][1])
		print(waa[1])
		self.show(waa[0][1], waa[1])
		dest.input(self, waa[1])

	def work(self):
		while self.working and self.master:
			print('zzd working',time.time())
			waa = self.core.getoutput()
			if waa == None:
				time.sleep(1)
			else:
				self.output(self.core.friend, waa)
				if waa[0][1] == u'再见' or waa[0][1] == '拜拜':
					self.working = False

def main():
	print('zzd_zzd')
	zzd.init()

if __name__ == '__main__':
	main()
