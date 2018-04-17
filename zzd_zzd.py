#!/usr/bin/python3 -B
import os 
import sys
import threading
import db
import time
import zzd_math
import zzd_unity

play_event = None
#除input函数运行在xhh线程，其他函数运行在zhd线程.
class zzd(zzd_unity.unity):
	inWaaClass = {}		#输入语句类型
	
	def __init__(self, show):
		global play_event
		zzd_unity.unity.__init__(self)
		self.show = show
		
		self.working = True
		self.root = True
		
		self.name = db.database._identifyDict['299792458']
		self.friend = None
		self.desire = {'input':[]}						#欲望：大凡物不得其平则鸣
		
		self.waain = []
		self.outsemaphore = threading.Semaphore(1)
		
		#有限状态机Finite-state machine
		self.FSM = {'verify':False, 'work':False, 'music':False, 'pause':False} 
		play_event = threading.Event()
		play_event.set()
	
	
	@classmethod
	def init(cls):
		db.database.gsinit()
		db.database.spinit()
		db.database.coreinit()
		
		cls.inWaaClass['verify'] = [zzd._verify, zzd._solve_verify]		#verify
		cls.inWaaClass['math'] = [zzd._math, zzd._solve_math]				#math
		cls.inWaaClass['define'] = [zzd._define, zzd._solve_define]		#define
		cls.inWaaClass['command'] = [zzd._command, zzd._solve_command]	#command
		cls.inWaaClass['system'] = [zzd._system, zzd._solve_system]		#system
		cls.inWaaClass['other'] = [zzd._other, zzd._solve_other]			#other
	
	#运行在xhh线程
	def input(self, sour, waa):
		record = {'waa':waa, 'sour':sour, 'time':time.time()}
		self.waain.append(record)
		self.desire['input'].append(record)
	
	def output(self, dest, waa):
		print('waa[0]',waa[0])
		print('waa[1]',waa[1])
		self.show(waa[0], waa[1])
		dest.input(self, waa[0])

	def work(self):
		while self.working and self.root:
			print('zzd working',time.time())
			waa = self.getoutput()
			if waa == None:
				time.sleep(1)
			else:
				self.output(self.friend, waa)
				if waa[0] == u'再见！' or waa[0] == '拜拜！':
					self.working = False


	
	def getoutput(self):
		assert 'input' in self.desire
		waaout = None
		if self.desire['input'] != []:
			d = self.desire['input'].pop(0)
			waaout=self.inputs(d['sour'], d['waa'])
			print(waaout[0], waaout[1])
		if waaout == None:
			t = time.localtime(time.time())
			if t.tm_sec == 0:
				return ('该休息了','')
			return None
		return waaout
	
	def inputs(self, friend, waa):
		self.friend = friend
		(head,sen,form) = self._trans_2_1(waa)
		if head == 'none':
			outs = sen
			return (outs, form)

		if self.FSM['verify'] == False:
			if head == 'verify':
				res = self._verify(sen)
				if res[0]:
					self.FSM['verify'] = True
					self.FSM['work'] = True
				return (res[1], form)
			else:
				outs = '对不起，您需要先进行身份认证!'
				return (outs, form)
		else:
			if head == 'verify':
				outs = '您已经认证过身份了。服务多人功能正在开发中，请耐心等待。'
				return (outs, form) 
		
		if self.FSM['work'] == True:
			assert head in zzd.inWaaClass
			outs = zzd.inWaaClass[head][0](self, sen)
			return (outs[1],form)
		outs = '对不起，我懵了!'
		return (outs, form)
	
	def _verify(self, sen):
		assert self.FSM['verify'] == False
		if sen['id'] in db.database._identifyDict:
			self.friend.name = db.database._identifyDict[sen['id']]
			return (True, '%s您好，认证通过。%s很高兴为您服务。'%(self.friend.name, self.name))
		return (False, '认证失败。')
				
	def _math(self, sen):
		eq = sen
		if eq.find('x') != -1:
			eq1 = eq.replace("=","-(")+")"
			try:
				c = eval(eq1,{'x':1j})
				val = int(-c.real/c.imag)
				val = str(val)
			except:
				return (False, self._sorry('math', sen))
		else:
			try:
				val = eval(eq)
				val = '对' if type(val) == bool and val else val
				val = '错' if type(val) == bool and not val else val
			except:
				return (False, self._sorry('math', sen))
		return (True, val)
	
	def _define(self, sen):
		if sen in db.database._defineDict:
			explain = db.database._defineDict[sen]
			return (True, sen+'是'+explain+'。')
		else:
			return (False, self._sorry('define', sen))
	
	def _command(self, sen):
		global play_event
		exe = db.database._keyword_zzd[sen['zzd命令']][1]
		if not (exe == '' or exe == None):
			cmd = sen['zzd命令']
			arg = sen['命令参数']
			return (True, '好的')
		if 'zzd播放命令' in sen:
			if not '命令参数' in sen:
				return (False, '播放什么歌曲?')
			if self.FSM['music'] == True:
				os.system('echo quit >> /tmp/mfifo')
			arg = sen['命令参数']
			play_event.wait()
			t = threading.Thread(target=mplayer_thread, args=(self, arg[1:-1]))
			t.start()
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
			return zzd.inWaaClass['other'][1](self, phrases)
		return zzd.inWaaClass[bit[0][0]][1](self, phrases)
	
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
	print('zzd_1')
	zzd.init()
	zhd = zzd(None)
	
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
	
if __name__ == '__main__':
	main()
