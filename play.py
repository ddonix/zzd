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
	def __init__(self, zhd):
		self.event = threading.Event()
		self.event.set()
		self.FSM = {'music':False, 'pause':False}
		self.zhd = zhd

	def play(self, arg):
		if self.FSM['music'] == True:
			self.stop()
		if arg == '':
			self.zhd.say('播放什么歌曲','')
			arg = self.zhd.ask('命令参数', )
			if not arg:
				return
		self.zhd.say('好的','')
		self.event.wait()
		t = threading.Thread(target=mplayer_thread, args=(self, arg[1:-1]))
		t.start()
	
	
	def con(self):
		if self.FSM['music'] == False:
			return self.zhd.say('没有歌曲在播放','')
		if self.FSM['pause'] == False:
			return self.zhd.say('正在播放','')
		assert os.path.exists('/tmp/mfifo')
		os.system('echo pause >> /tmp/mfifo')
		self.FSM['pause'] = False
		self.zhd.say('好的','')
	
	def pause(self):
		if self.FSM['music'] == False:
			return self.zhd.say('没有歌曲在播放', '')
		if self.FSM['pause'] == True:
			return self.zhd.say('播放已经暂停', '')
		assert os.path.exists('/tmp/mfifo')
		os.system('echo pause >> /tmp/mfifo')
		self.FSM['pause'] = True
		self.zhd.say('好的','')
	
	def stop(self):
		if self.FSM['music'] == False:
			return self.zhd.say('没有歌曲在播放', '')
		os.system('echo quit >> /tmp/mfifo')
		self.FSM['musci'] = False
		self.FSM['pause'] = False
		self.zhd.say('好的','')

def main():
	print('play')

if __name__ == '__main__':
	main()
