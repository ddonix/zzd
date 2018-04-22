#!/usr/bin/python3 -B
import os 
import threading


def mplayer_thread(core):
	core.event.clear()
	for filename in core.list:
		if core.playflag == False:
			break
		print('播放 ../music/%s'%filename)
		cmd = 'mplayer -slave -input file=/tmp/mfifo ../music/%s'%filename
		print(cmd)
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
		self.list = []
		self.playflag = False

	def play(self, arg):
		if self.FSM['music'] == True:
			self.stop(True)
		if arg == '':
			self.zhd.say('播放什么歌曲','')
			arg = self.zhd.ask('命令参数')
			if not arg:
				return
			arg = arg[0]
		if arg == '随便':
			self.list = os.listdir('./music')
		else:
			self.list = ['%s.mp3'%arg[1:-1]]
		self.playflag = True
		self.zhd.say('好的','')
		self.event.wait()
		t = threading.Thread(target=mplayer_thread, args=(self,))
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
	
	def next(self):
		pass
	
	def stop(self, echo):
		if self.FSM['music'] == False:
			if echo:
				self.zhd.say('没有歌曲在播放', '')
			return
		self.playflag = False
		os.system('echo quit >> /tmp/mfifo')
		self.FSM['musci'] = False
		self.FSM['pause'] = False
		if echo:
			self.zhd.say('好的','')

def main():
	print('play')

if __name__ == '__main__':
	main()
