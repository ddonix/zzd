#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import grammar 
import xlrd 

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
	defineDict = {}
	keyword_zzd = {}

	def __init__(self):
		self.sentence = []
		self.state = 'init'
		self.mode = 'work'
		self.friend = None
		self.cursen = None
	
	@classmethod
	def init(cls):
		grammar.initall()
		zzdcore1.inWaaClass[u'verify'] = [zzdcore1._verify, zzdcore1._solve_verify]			#verify
		zzdcore1.inWaaClass[u'math'] = [zzdcore1._math, zzdcore1._solve_math]				#math
		zzdcore1.inWaaClass[u'define'] = [zzdcore1._define, zzdcore1._solve_define]			#define
		zzdcore1.inWaaClass[u'command'] = [zzdcore1._command, zzdcore1._solve_command]		#command
		zzdcore1.inWaaClass[u'system'] = [zzdcore1._system, zzdcore1._solve_system]			#system
		zzdcore1.inWaaClass[u'other'] = [zzdcore1._other, zzdcore1._solve_other]			#other
		
		xlsfile = r"data/grammar.xls"		# 打开指定路径中的xls文件
		book = xlrd.open_workbook(xlsfile)	#得到Excel文件的book对象，实例化对象

		# 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
		sheet = book.sheet_by_name(u'define')
		nrows = sheet.nrows
		for i in range(nrows):
			defi = sheet.row_values(i)
			zzdcore1.defineDict[defi[0]] = defi[1]
		
		sheet = book.sheet_by_name(u'zzd关键字')
		nrows = sheet.nrows
		for i in range(nrows):
			keyword = sheet.row_values(i)
			zzdcore1.keyword_zzd[keyword[0]] = keyword[1:]
		print zzdcore1.keyword_zzd
		book.release_resources()

	def inputs(self, friend, waa):
		(head,sen) = self._trans_2_1(friend, waa)
		if head == u'none':
			outs = u'对不起，我不明白您的意思!错误信息\"%s\"'%sen
			self.sentence.append([waa,(head,sen),outs])
			return self._sorry((u'copy',outs))

		if self.state == 'init':
			if head == u'verify':
				res = self._verify(sen)
				if res[0]:
					self.state = 'stand'
					self.friend = friend
				self.sentence.append([waa,(head,sen),res])
				return res
			else:
				outs = u'对不起，您需要先进行身份认证!'
				self.sentence.append([waa,(head,sen),outs])
				return self._sorry((u'copy', outs))
		elif self.mode == 'work':
			assert head in zzdcore1.inWaaClass
			outs = zzdcore1.inWaaClass[head][0](self, sen)
			self.sentence.append([waa,(head,sen),outs])
			return outs
		else:
			outs = u'对不起，我懵了!'
			return self._sorry((u'copy', outs))
	
	def _verify(self, sen):
		if self.state == 'init':
			return (True, u'验证通过')
		else:
			return (False, u'您已经通过验证了，不需要再验证。')
				
				return (True, u'您已经认证过身份了。服务多人功能正在开发中，请耐心等待。')
			elif len(sen) == 10 and sen[2:10] == u'12345678':
				return (True, u'您的身份认证通过。谢谢您回来，您有什么想对我说的吗？')
			else:
		
	def _math(self, sen):
		eq = sen
		if eq.find(u'x') != -1:
			eq1 = eq.replace("=","-(")+")"
			try:
				c = eval(eq1,{u'x':1j})
				val = int(-c.real/c.imag)
				val = u'x='+str(val)
			except:
				return self._sorry((u'math', sen))
		else:
			try:
				val = eval(eq)
				if val:
					val = u'对'
				else:
					val = u'错'
			except:
				return self._sorry((u'math', sen))
		return (True, val)
	
	def _define(self, sen):
		o = zzdcore1.defineDict.get(sen)
		if o == None:
			return self._sorry((u'define',sen))
		return (True, sen+u'是'+o)
	
	def _command(self, sen):
		return self._sorry((u'command', sen))

	def _system(self, phrases):
		return self._sorry((u'system', sen))
	
	def _other(self, phrases):
		return self._sorry((u'system', sen))
	
	def _trans_2_1(self, friend, waa):
		phrases = grammar._fenci(waa)
		for p in phrases:
			print p.s
		keyword = [x for x in phrases if x.be(u'zzd关键字')]
		bit = {u'verify':0,u'math':0,u'define':0,u'command':0,u'system':0}
		for k in keyword:
			assert k.s in zzdcore1.keyword_zzd
			if zzdcore1.keyword_zzd[k.s][0] == u'other':
				continue
			weight = zzdcore1.keyword_zzd[k.s][0].split(' ')
			for i in range(0,len(weight),2):
				bit[weight[i]] += int(weight[i+1])
		bit = sorted(bit.items(),key = lambda x:x[1],reverse = True)
		if bit[0][1] == 0:
			return zzdcore1.inWaaClass[u'other'][1](self, friend, phrases, keyword)
		return zzdcore1.inWaaClass[bit[0][0]][1](self, friend, phrases, keyword)
	
	def _solve_verify(self, friend, phrases, keyword):
		return (u'verify', None)
	
	def _solve_math(self, friend, phrases, keyword):
		return None
	
	def _solve_define(self, friend, phrases, keyword):
		return None
	
	def _solve_command(self, friend, phrases, keyword):
		return None
	
	def _solve_system(self, friend, phrases, keyword):
		return None
	
	def _solve_other(self, friend, phrases, keyword):
		return None

	def _sorry(self, waa):
		if waa[0] == u'copy':
			return (False, waa[1])
		elif waa[0] == u'define':
			return (False, u'对不起，我没有\"'+waa[1]+u'\"的定义。请进入训练模式，添加定义。')
		elif waa[0] == u'math':
			return (False, u'对不起，我无法计算\"'+waa[1]+u'\"。请检查表达式。')
		elif waa[0] == u'command':
			return (False, u'对不起，我无法执行\"'+waa[1]+u'\"。请检查命令。')
		else:
			return (False, u'对不起，我无法处理\"'+waa[1]+u'\"。')
	
	
def main():
	print('zzd_core1')
	grammar.initall()
	zzdcore1.init()
	core1 = zzdcore1()

	fc = core1._trans_2_1(None, u'认证12345678!')
	print fc

if __name__ == '__main__':
	main()
