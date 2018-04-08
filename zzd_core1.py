#!/usr/bin/python -B
# -*- coding: UTF-8 -*-
import zzd_core0
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

	def __init__(self, corelayer0):
		self.sentence = []
		self.corelayer0 = corelayer0
		self.state = 'init'
		self.mode = 'work'
		self.friend = None
		self.cursen = None
	
	@classmethod
	def init(cls):
		zzd_core0.zzdcore0.init()
		zzdcore1.inWaaClass[u'verify'] = [zzdcore1._verify, zzdcore1._solve_verify]			#math
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
		(head,sen)= self._trans_2_1(friend, waa)
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
				self.sentence.append([waa,(head,sen),res[1]])
				return res[1]
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
		return None
		
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
		return val
	
	def _define(self, sen):
		o = zzdcore1.defineDict.get(sen)
		if o == None:
			return self._sorry((u'defi',sen))
		return sen+u'是'+o
	
	def _command(self, sen):
		if sen[0:2] == u'id':
			if self.state != 'init':
				return (True, u'您已经认证过身份了。服务多人功能正在开发中，请耐心等待。')
			elif len(sen) == 10 and sen[2:10] == u'12345678':
				return (True, u'您的身份认证通过。谢谢您回来，您有什么想对我说的吗？')
			else:
				return (False, u'认证失败。请重新认证。')
		else:
			return self._sorry((u'comm', sen))

	def _system(self, phrases):
		return None
	
	def _other(self, phrases):
		return None
	
	def _trans_2_1(self, friend, waa):
		head = waa[0:4]
		sen = waa[5:len(waa)]
		return head, sen
	
	def _zj(self, friend, waa):
		phrases = grammar._fenci(waa)
		for p in phrases:
			print p.s
		keyword = [x for x in phrases if x.be(u'zzd关键字')]
		assert(keyword)
		for k in keyword:
			if k == u'None':
				pass
			res = None
			assert k.s in zzdcore1.keyword_zzd
			ex = u'res = self._zj_%s(friend, phrases)'%zzdcore1.keyword_zzd[k.s][0]
			try:
				exec(ex)
			except:
				pass
			return res
		return None
	
	def _solve_verify(self, friend, phrases):
		res = u'comm:'
		return res
	
	def _solve_math(self, friend, phrases):
		return None
	
	def _solve_define(self, friend, phrases):
		res = u'comm:'
		return res
	
	def _solve_command(self, friend, phrases):
		res = u'comm:'
		return res
	
	def _solve_system(self, friend, phrases):
		return None
	
	def _solve_other(self, friend, phrases):
		return None
	
	def _sorry(self, waa):
		if waa[0] == u'copy':
			return waa[1]
		elif waa[0] == u'defi':
			return u'对不起，我没有\"'+waa[1]+u'\"的定义。请进入训练模式，添加定义。'
		elif waa[0] == u'math':
			return u'对不起，我无法计算\"'+waa[1]+u'\"。请检查表达式。'
		elif waa[0] == u'comm':
			return u'对不起，我无法执行\"'+waa[1]+u'\"。请检查命令。'
		else:
			return u'对不起，我无法处理\"'+waa[1]+u'\"。'
	
	
def main():
	print('zzd_core1')
	grammar.initall()
	core0 = zzd_core0.zzdcore0()
	core1 = zzdcore1(core0)
	zzdcore1.init()

	fc = core1._zj(None, u'播放歌曲!')
	print fc

if __name__ == '__main__':
	main()
