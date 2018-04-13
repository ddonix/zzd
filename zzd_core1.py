#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import xlrd 
import os 
import sqlite3
import db
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
		self.state = 'init'
		self.mode = 'work'
		self.name = u'小白'
		self.friend = None
		self.cursen = None
	
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
		self.friend = friend
		(head,sen,form) = self._trans_2_1(waa)
		if head == u'none':
			outs = u'对不起，我不明白您的意思!错误信息\"%s\"'%sen
			self.sentence.append([waa,(head,sen),outs])
			return (self._sorry(u'copy',outs),form)

		if self.state == 'init':
			if head == u'verify':
				res = self._verify(sen)
				if res[0]:
					self.state = 'stand'
					self.friend = friend
				self.sentence.append([waa,(head,sen),res])
				return (res,form)
			else:
				outs = u'对不起，您需要先进行身份认证!'
				self.sentence.append([waa,(head,sen),outs])
				return (False, self._sorry(u'copy', outs),form)
		elif self.mode == 'work':
			assert head in zzdcore1.inWaaClass
			outs = zzdcore1.inWaaClass[head][0](self, sen)
			self.sentence.append([waa,(head,sen),outs])
			return (outs,form)
		else:
			outs = u'对不起，我懵了!'
			return (False, self._sorry(u'copy', outs),form)
	
	def _verify(self, sen):
		if self.state == 'init':
			if sen[u'id'] in db.database._identifyDict:
				self.friend.name = db.database._identifyDict[sen[u'id']]
				return (True, u'%s您好，身份认证通过。我有什么为您服务的吗？'%self.friend.name)
			return (False, u'认证失败。')
		else:
			return (False, u'您已经认证过身份了。服务多人功能正在开发中，请耐心等待。')
				
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
		com = sen.encode('utf8')
		print com
		pid = os.fork()
		if pid == 0:
			os.system(com)
			sys.exit()
		else:
			return (True, u'好的')

	def _system(self, phrases):
		return self._sorry((u'system', sen))
	
	def _other(self, phrases):
		return self._sorry((u'system', sen))
	
	def _trans_2_1(self, waa):
		phrases = db.fenci(waa, False)
		keyword = [x for x in phrases if x.be(u'zzd关键字')]
		bit = {u'verify':0,u'math':0,u'define':0,u'command':0,u'system':0}
		for k in keyword:
			assert k.s in db.database._keyword_zzd
			weight = db.database._keyword_zzd[k.s][0].split(' ')
			for i in range(0,len(weight),2):
				if weight[i] != '':
					bit[weight[i]] += int(weight[i+1])
		bit = sorted(bit.items(),key = lambda x:x[1],reverse = True)
		if bit[0][1] == 0:
			return zzdcore1.inWaaClass[u'other'][1](self, phrases, keyword)
		return zzdcore1.inWaaClass[bit[0][0]][1](self, phrases, keyword)
	
	def _solve_verify(self, phrases, keyword):
		sp = db.database.gs(u'认证语句')._fensp(phrases, True)
		if sp == None:
			return (u'none', u'认证语法不对', '')
		else:
			assert u'数' in sp[2]
			return (u'verify', {u'id':sp[2][u'数']}, sp[0].s)
	
	def _solve_math(self, phrases, keyword):
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
	
	def _solve_define(self, phrases, keyword):
		sp = db.database.gs(u'定义语句')._fensp(phrases, True)
		if sp == None:
			return (u'none', u'定义语法不对','')
		else:
			assert u'定义词' in sp[2]
			return (u'define', sp[2][u'定义词'], sp[0].s)
	
	def _solve_command(self, phrases, keyword):
		sp = db.database.gs(u'命令语句')._fensp(phrases, True)
		if sp == None:
			return (u'none', u'命令语法不对','')
		else:
			assert u'命令确认' in sp[2]
			assert u'命令参数' in sp[2]
			print sp[2][u'命令确认']
			print sp[2][u'命令参数']
			assert sp[2][u'命令确认'][0:2] in db.database._keyword_zzd
			exe = db.database._keyword_zzd[sp[2][u'命令确认'][0:2]][1]
			arg = sp[2][u'命令参数']
			print exe
			res = ''
			try:
				exec(exe)
			except:
				return (u'none', u'命令语法错误')
			return (u'command', res,sp[0].s)
	
	def _solve_system(self, phrases, keyword):
		for ph in phrases:
			print ph.s
		return (u'none', u'对不起，出错了!', u'')
	
	def _solve_other(self, phrases, keyword):
		ph = [x for x in phrases]
		res = self._solve_verify(ph, keyword)
		if res[0] != u'none':
			return res
		
		ph = [x for x in phrases]
		res = self._solve_define(ph, keyword)
		if res[0] != u'none':
			return res
		
		ph = [x for x in phrases]
		res = self._solve_command(ph, keyword)
		if res[0] != u'none':
			return res
		
		ph = [x for x in phrases]
		res = self._solve_math(ph, keyword)
		if res[0] != u'none':
			return res
		
		res = self._solve_system(phrases, keyword)
		if res[0] != u'none':
			return res
		return (u'none', u'对不起，出错了!', u'')

	def _sorry(self, head, sen):
		if head == u'copy':
			return sen
		elif head == u'define':
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

	fc = core1._trans_2_1(u'14>24')
	print fc[0],fc[1]

if __name__ == '__main__':
	main()
