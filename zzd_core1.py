#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import os 
import sys
import thread
import db
import time
import zzd_math

#init:初始化。
#stand：完成一次交互，等待下一次交互。没有预期。
#wait:期待human的回应。有预期。
#initiative:主动状态，主动发起对话。
STATE = ('init', 'stand', 'wait', 'initiative')

#work:工作模式
#game:娱乐模式
#train:训练模式
#debug:调试模式
MODE = ('work', 'train', 'debug')

class zzdcore1:
	inWaaClass = {}		#输入语句类型

	def __init__(self):
		self.sentence = []
		self.name = db.database._identifyDict[u'299792458']
		self.friend = None
		self.cursen = None
		self.expect = []
		#有限状态机Finite-state machine
		self.FSM = {u'verify':False, u'work':False, u'music':False, u'pause':False} 
	
	@classmethod
	def init(cls):
		db.database.gsinit()
		db.database.spinit()
		db.database.coreinit()
		
		zzdcore1.inWaaClass[u'verify'] = [zzdcore1._verify, zzdcore1._solve_verify]			#verify
		zzdcore1.inWaaClass[u'math'] = [zzdcore1._math, zzdcore1._solve_math]				#math
		zzdcore1.inWaaClass[u'define'] = [zzdcore1._define, zzdcore1._solve_define]			#define
		zzdcore1.inWaaClass[u'command'] = [zzdcore1._command, zzdcore1._solve_command]		#command
		zzdcore1.inWaaClass[u'system'] = [zzdcore1._system, zzdcore1._solve_system]			#system
		zzdcore1.inWaaClass[u'other'] = [zzdcore1._other, zzdcore1._solve_other]			#other
	
	
	@classmethod
	def verifydatabase(cls):
		pass
		
				
	def inputs(self, friend, waa):
		(head,sen,form) = self._trans_2_1(waa)
		if head == u'none':
			outs = sen
			self.sentence.append([waa,(head,sen),outs])
			return ((False, outs),form)

		if self.FSM[u'verify'] == False:
			if head == u'verify':
				self.friend = friend
				res = self._verify(sen)
				if res[0]:
					self.FSM[u'verify'] = True
					self.FSM[u'work'] = True
				else:
					self.friend = None
				self.sentence.append([waa,(head,sen),res])
				return (res,form)
			else:
				outs = u'对不起，您需要先进行身份认证!'
				self.sentence.append([waa,(head,sen),outs])
				return ((False,outs),form)
		else:
			if head == u'verify':
				outs = u'您已经认证过身份了。服务多人功能正在开发中，请耐心等待。'
				return ((False,outs),form) 
		
		if self.FSM[u'work'] == True:
			assert head in zzdcore1.inWaaClass
			assert friend == self.friend
			outs = zzdcore1.inWaaClass[head][0](self, sen)
			self.sentence.append([waa,(head,sen),outs])
			return (outs,form)
		outs = u'对不起，我懵了!'
		return ((False,outs),form)
	
	def _verify(self, sen):
		assert self.FSM[u'verify'] == False
		if sen[u'id'] in db.database._identifyDict:
			self.friend.name = db.database._identifyDict[sen[u'id']]
			return (True, u'%s您好，认证通过。%s很高兴为您服务。'%(self.friend.name, self.name))
		return (False, u'认证失败。')
				
	def _math(self, sen):
		eq = sen
		if eq.find(u'x') != -1:
			eq1 = eq.replace("=","-(")+")"
			try:
				c = eval(eq1,{u'x':1j})
				val = int(-c.real/c.imag)
				val = str(val)
			except:
				return (False, self._sorry(u'math', sen))
		else:
			try:
				val = eval(eq)
				val = u'对' if type(val) == bool and val else val
				val = u'错' if type(val) == bool and not val else val
			except:
				return (False, self._sorry(u'math', sen))
		return (True, val)
	
	def _define(self, sen):
		if sen in db.database._defineDict:
			explain = db.database._defineDict[sen]
			return (True, sen+u'是'+explain+u'。')
		else:
			return (False, self._sorry(u'define', sen))
	
	def _command(self, sen):
		exe = db.database._keyword_zzd[sen[u'zzd命令']][1]
		if not (exe == '' or exe == None):
			cmd = sen[u'zzd命令']
			arg = sen[u'命令参数']
			return (True, u'好的')
		if u'zzd播放命令' in sen:
			if not u'命令参数' in sen:
				return (False, u'播放什么歌曲?')
			arg = sen[u'命令参数']
			if self.FSM[u'music'] == True:
				assert os.path.exists('/tmp/mfifo')
				f = open('/tmp/mfifo','w+')
				f.write('quit\n')
				f.close()
				time.sleep(2)
			thread.start_new_thread( mplayer_thread, ("mplayer播放歌曲", self, arg))
		elif u'zzd暂停命令' in sen:
			if self.FSM[u'music'] == False:
				return (False, u'没有歌曲在播放')
			if self.FSM[u'pause'] == True:
				return (False, u'播放已经暂停')
			assert os.path.exists('/tmp/mfifo')
			f = open('/tmp/mfifo','w+')
			f.write('pausing pause\n')
			f.close()
			self.FSM[u'pause'] = True
		elif u'zzd继续命令' in  sen:
			if self.FSM[u'music'] == False:
				return (False, u'没有歌曲在播放')
			if self.FSM[u'pause'] == False:
				return (False, u'正在播放')
			assert os.path.exists('/tmp/mfifo')
			f = open('/tmp/mfifo','w+')
			f.write('pausing pause\n')
			f.close()
			self.FSM[u'pause'] = False
		elif u'zzd停止命令' in sen:
			if self.FSM[u'music'] == False:
				return (False, u'没有歌曲在播放')
			f = open('/tmp/mfifo','w+')
			f.write('stop\n')
			f.close()
			self.FSM[u'musci'] = False
			self.FSM[u'pause'] = False
		elif u'zzd再见命令' in sen:
			if self.FSM[u'music'] == True:
				f = open('/tmp/mfifo','w+')
				f.write('stop\n')
				f.close()
			return (True, sen[u'zzd再见命令'])
		else:
			return (False, u'不识别的命令:%s'%cmd)
		return (True, u'好的')

	def _system(self, phrases):
		return self._sorry((u'system', sen))
	
	def _other(self, phrases):
		return self._sorry((u'system', sen))
	
	def _trans_2_1(self, waa):
		phrases = db.fenci(waa, False)
		keyword = [x for x in phrases if x.s in db.database._keyword_zzd]
		bit = {u'verify':0,u'math':0,u'define':0,u'command':0,u'system':0}
		for k in keyword:
			assert k.s in db.database._keyword_zzd
			weight = db.database._keyword_zzd[k.s][0].split(' ')
			for i in range(0,len(weight),2):
				if weight[i] != '':
					bit[weight[i]] += int(weight[i+1])
		bit = sorted(bit.items(),key = lambda x:x[1],reverse = True)
		if bit[0][1] == 0:
			return zzdcore1.inWaaClass[u'other'][1](self, phrases)
		return zzdcore1.inWaaClass[bit[0][0]][1](self, phrases)
	
	def _solve_verify(self, phrases):
		sp = db.database.gs(u'认证语句')._fensp(phrases, True)
		if sp == None:
			return (u'none', u'认证语法不对', '')
		else:
			assert u'数' in sp[2]
			return (u'verify', {u'id':sp[2][u'数']}, sp[0].s)
	
	def _solve_math(self, phrases):
		sp = db.database.gs(u'数学语句')._fensp(phrases, True)
		if sp == None:
			return (u'none', u'数学语法不对', '')
		else:
			if u'数学判断' in sp[2] or u'数学方程' in sp[2]:
				return (u'math', sp[0].s, sp[0].s)
			else:
				sen = zzd_math.c2math(phrases)
				if sen:
					return (u'math', sen, sen)
				else:
					return (u'none', u'数学语法错误%s'%sp[0].s, sp[0].s)
	
	def _solve_define(self, phrases):
		sp = db.database.gs(u'定义语句')._fensp(phrases, True)
		if sp == None:
			return (u'none', u'定义语法不对','')
		else:
			assert u'定义词' in sp[2]
			return (u'define', sp[2][u'定义词'], sp[0].s)
	
	def _solve_command(self, phrases):
		sp = db.database.gs(u'命令语句')._fensp(phrases, True)
		if sp == None:
			return (u'none', u'命令语法不对','')
		else:
			assert u'zzd命令' in sp[2]
			return (u'command', sp[2], sp[0].s)
			
	def _solve_system(self, phrases):
		for ph in phrases:
			print ph.s
		return (u'none', u'对不起，出错了!', u'')
	
	def _solve_other(self, phrases):
		ph = [x for x in phrases]
		res = self._solve_verify(ph)
		if res[0] != u'none':
			return res
		
		ph = [x for x in phrases]
		res = self._solve_define(ph)
		if res[0] != u'none':
			return res
		
		ph = [x for x in phrases]
		res = self._solve_command(ph)
		if res[0] != u'none':
			return res
		
		ph = [x for x in phrases]
		res = self._solve_math(ph)
		if res[0] != u'none':
			return res
		
		res = self._solve_system(phrases)
		if res[0] != u'none':
			return res
		return (u'none', u'对不起，出错了!', u'')

	def _sorry(self, head, sen):
		if head == u'define':
			return u'对不起，我没有\"'+sen+u'\"的定义。请进入训练模式，添加定义。'
		elif head == u'math':
			return u'对不起，我无法计算\"'+sen+u'\"。请检查表达式。'
		elif head == u'command':
			return u'对不起，我无法执行\"'+sen+u'\"。请检查命令。'
		else:
			return u'对不起，我无法处理\"'+sen+u'\"。'
	

def main():
	print('zzd_core1')
	zzdcore1.init()
	zzdcore1.verifydatabase()
	core1 = zzdcore1()
	
	a = u'再见'
	phs = db.fenci(a, False)
	g = db.database.gs(u'命令语句')
	sp = g._fensp(phs,True)
	print sp[0].s
	print sp[1]
	print sp[2]
	for s in sp[2]:
		print s,sp[2][s]
	
	#播放线程
def mplayer_thread( threadName, core1, arg):
	print(u'开始播放')
	cmd = u'mplayer -slave -input file=/tmp/mfifo %s.mp3'%arg[1:-1]
	cmd = cmd.encode('utf8')
	os.system('rm /tmp/mfifo -rf')
	os.system('mkfifo /tmp/mfifo')
	print cmd
	core1.FSM[u'music'] = True
	core1.FSM[u'pause'] = False
	os.system(cmd)
	core1.FSM[u'music'] = False
	core1.FSM[u'pause'] = False
	print(u'播放完毕')
	
	
if __name__ == '__main__':
	main()
