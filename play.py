#!/usr/bin/python3 -B
import os 
import sys
import threading
import db
import time
import zzd_math

def mplayer_thread(core, arg):
	global play_event
	play_event.clear()
	
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
	
	play_event.set()

class player:

	def __init__(self):
		self.event = threading.Event()
		self.event.set()
		self.FSM = {'music':False, 'pause':False}
		self.thread = None

	def play(self, arg):
		if self.FSM['music'] == True:
			self.stop()
		if arg == '' or arg == None:
			return '播放什么歌曲?'
		self.event.wait()
		self.thread = threading.Thread(target=mplayer_thread, args=(self, arg[1:-1]))
		self.thread.start()
		return '好的'
	
	def stop(self):
		pass
	
	def pause(self):
		if self.FSM['music'] == False:
			return (False, '没有歌曲在播放')
		if self.FSM['pause'] == True:
			return (False, '播放已经暂停')
		assert os.path.exists('/tmp/mfifo')
		os.system('echo pause >> /tmp/mfifo')
		pass
	
	def (self):
		if self.FSM['music'] == False:
			return (False, '没有歌曲在播放')
		if self.FSM['pause'] == True:
			return (False, '播放已经暂停')
		assert os.path.exists('/tmp/mfifo')
		os.system('echo pause >> /tmp/mfifo')


	def _command(self, sen):
		elif 'zzd暂停命令' in sen:
			if self.FSM['music'] == False:
				return (False, '没有歌曲在播放')
			if self.FSM['pause'] == True:
				return (False, '播放已经暂停')
			assert os.path.exists('/tmp/mfifo')
			os.system('echo pause >> /tmp/mfifo')
			self.FSM['pause'] = True
		elif 'zzd继续命令' in  sen:
			if self.FSM['music'] == False:
				return (False, '没有歌曲在播放')
			if self.FSM['pause'] == False:
				return (False, '正在播放')
			assert os.path.exists('/tmp/mfifo')
			os.system('echo pause >> /tmp/mfifo')
			self.FSM['pause'] = False
		elif 'zzd停止命令' in sen:
			if self.FSM['music'] == False:
				return (False, '没有歌曲在播放')
			os.system('echo quit >> /tmp/mfifo')
			self.FSM['musci'] = False
			self.FSM['pause'] = False
		elif 'zzd再见命令' in sen:
			if self.FSM['music'] == True:
				os.system('echo quit >> /tmp/mfifo')
			return (True, sen['zzd再见命令']+'！')
		else:
			return (False, '不识别的命令:%s'%cmd)
		return (True, '好的')

	def _system(self, phrases):
		return self._sorry(('system', sen))
	
	def _other(self, phrases):
		return self._sorry(('system', sen))
	
	def _trans_2_1(self, waa):
		phrases = db.fenci(waa, False)
		keyword = [x for x in phrases if x.s in db.database._keyword_zzd]
		bit = {'verify':0,'math':0,'define':0,'command':0,'system':0}
		for k in keyword:
			assert k.s in db.database._keyword_zzd
			weight = db.database._keyword_zzd[k.s][0].split(' ')
			for i in range(0,len(weight),2):
				if weight[i] != '':
					bit[weight[i]] += int(weight[i+1])
		bit = sorted(bit.items(),key = lambda x:x[1],reverse = True)
		if bit[0][1] == 0:
			return zzdcore1.inWaaClass['other'][1](self, phrases)
		return zzdcore1.inWaaClass[bit[0][0]][1](self, phrases)
	
	def _solve_verify(self, phrases):
		sp = db.database.gs('认证语句')._fensp(phrases, True)
		if sp == None:
			return ('none', '认证语法不对', '')
		else:
			assert '数' in sp[2]
			return ('verify', {'id':sp[2]['数']}, sp[0].s)
	
	def _solve_math(self, phrases):
		sp = db.database.gs('数学语句')._fensp(phrases, True)
		if sp == None:
			return ('none', '数学语法不对', '')
		else:
			if '数学判断' in sp[2] or '数学方程' in sp[2]:
				return ('math', sp[0].s, sp[0].s)
			else:
				sen = zzd_math.c2math(phrases)
				if sen:
					return ('math', sen, sen)
				else:
					return ('none', '数学语法错误%s'%sp[0].s, sp[0].s)
	
	def _solve_define(self, phrases):
		sp = db.database.gs('定义语句')._fensp(phrases, True)
		if sp == None:
			return ('none', '定义语法不对','')
		else:
			assert '定义词' in sp[2]
			return ('define', sp[2]['定义词'], sp[0].s)
	
	def _solve_command(self, phrases):
		sp = db.database.gs('命令语句')._fensp(phrases, True)
		if sp == None:
			return ('none', '命令语法不对','')
		else:
			assert 'zzd命令' in sp[2]
			return ('command', sp[2], sp[0].s)
			
	def _solve_system(self, phrases):
		for ph in phrases:
			print(ph.s)
		return ('none', '对不起，出错了!', '')
	
	def _solve_other(self, phrases):
		ph = [x for x in phrases]
		res = self._solve_verify(ph)
		if res[0] != 'none':
			return res
		
		ph = [x for x in phrases]
		res = self._solve_define(ph)
		if res[0] != 'none':
			return res
		
		ph = [x for x in phrases]
		res = self._solve_command(ph)
		if res[0] != 'none':
			return res
		
		ph = [x for x in phrases]
		res = self._solve_math(ph)
		if res[0] != 'none':
			return res
		
		res = self._solve_system(phrases)
		if res[0] != 'none':
			return res
		return ('none', '对不起，出错了!', '')

	def _sorry(self, head, sen):
		if head == 'define':
			return '对不起，我没有\"'+sen+'\"的定义。请进入训练模式，添加定义。'
		elif head == 'math':
			return '对不起，我无法计算\"'+sen+'\"。请检查表达式。'
		elif head == 'command':
			return '对不起，我无法执行\"'+sen+'\"。请检查命令。'
		else:
			return '对不起，我无法处理\"'+sen+'\"。'
	

def main():
	print('zzd_core1')
	zzdcore1.init()
	core1 = zzdcore1()
	
	a = '再见'
	phs = db.fenci(a, False)
	g = db.database.gs('命令语句')
	sp = g._fensp(phs,True)
	print(sp[0].s)
	print(sp[1])
	print(sp[2])
	for s in sp[2]:
		print(s,sp[2][s])
	
	#播放线程

	
if __name__ == '__main__':
	main()
