#!/usr/bin/python3 -B
import os 
import threading

def mplayer_thread(core, arg):
	core.event.clear()
	
	print('播放 %s.mp3'%arg)
	cmd = 'mplayer -slave -input file=/tmp/mfifo %s.mp3'%arg
	os.system('rm /tmp/mfifo -rf')
	os.system('mkfifo /tmp/mfifo')
	core.FSM['music'] = True
	core.FSM['pause'] = False
	os.system(cmd)
	core.FSM['music'] = False
	core.FSM['pause'] = False
	print('播放完毕')
	
	core.event.set()

class player:

	def __init__(self):
		self.event = threading.Event()
		self.event.set()
		
		self.FSM = {'music':False, 'pause':False}

	def play(self, arg):
		assert arg
		if self.FSM['music'] == True:
			self.stop()
		self.event.wait()
		t = threading.Thread(target=mplayer_thread, args=(self, arg[1:-1]))
		t.start()
		return '好的'
	
	def con(self):
		if self.FSM['music'] == False:
			return '没有歌曲在播放'
		if self.FSM['pause'] == False:
			return '正在播放'
		assert os.path.exists('/tmp/mfifo')
		os.system('echo pause >> /tmp/mfifo')
		self.FSM['pause'] = False
		return '好的'
	
	def pause(self):
		if self.FSM['music'] == False:
			return '没有歌曲在播放'
		if self.FSM['pause'] == True:
			return '播放已经暂停'
		assert os.path.exists('/tmp/mfifo')
		os.system('echo pause >> /tmp/mfifo')
		self.FSM['pause'] = True
		return '好的'
	
	def stop(self):
		if self.FSM['music'] == False:
			return (False, '没有歌曲在播放')
		os.system('echo quit >> /tmp/mfifo')
		self.FSM['musci'] = False
		self.FSM['pause'] = False
		return '好的'

def main():
	print('play')

if __name__ == '__main__':
	main()
