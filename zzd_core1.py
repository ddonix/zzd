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
	inWaaClass = []		#输入语句类型
	defineDict = {}

	def __init__(self, corelayer0):
		self.sentence = []
		self.corelayer0 = corelayer0
		self.state = 'init'
		self.mode = 'work'
		self.friend = None
		self.cursen = None
	
	@classmethod
	def init(cls):
		grammar.sentencephrase.init()
		zzd_core0.zzdcore0.init()
		
		zzdcore1.inWaaClass.append([u'math', zzdcore1._math, zzdcore1._solve_math])			#math
		zzdcore1.inWaaClass.append([u'defi', zzdcore1._define, zzdcore1._solve_define])		#define
		zzdcore1.inWaaClass.append([u'comm', zzdcore1._command, zzdcore1._solve_command])	#command
		zzdcore1.inWaaClass.append([u'echo', zzdcore1._echo, zzdcore1._solve_echo])			#echo
	
		zzdcore1.inWaaClass.append([u'copy', zzdcore1._copy, zzdcore1._solve_copy])			#copy
		zzdcore1.inWaaClass.append([u'debu', zzdcore1._debug, zzdcore1._solve_debug])		#debug
		zzdcore1.inWaaClass.append([u'none', zzdcore1._none, zzdcore1._solve_none])			#none
		
		xlsfile = r"data/grammar.xls"		# 打开指定路径中的xls文件
		book = xlrd.open_workbook(xlsfile)	#得到Excel文件的book对象，实例化对象
		# 通过sheet名字来获取，当然如果知道sheet名字就可以直接指定
		sheet = book.sheet_by_name('grammar_phrase')
		nrows = sheet.nrows
		for i in range(nrows):
			v = sheet.row_values(i)
			g = grammar.gset(v[0], v[1:])
			grammar.grammar_all[v[0]] = g
		
		sheet = book.sheet_by_name('grammar_sentence')
		nrows = sheet.nrows
		for i in range(nrows):
			v = sheet.row_values(i)
			g = grammar.gset(v[0], v[1:])
			grammar.grammar_all[v[0]] = g
		
		sheet = book.sheet_by_name('table_vocable')
		nrows = sheet.nrows
		for i in range(nrows):
			v = sheet.row_values(i)
			sp = grammar.sentencephrase(v)
			grammar.sp_all[v[0]]=sp
		
		sheet = book.sheet_by_name('table_phrase')
		nrows = sheet.nrows
		for i in range(nrows):
			v = sheet.row_values(i)
			sp = grammar.sentencephrase(v)
			grammar.sp_all[v[0]]=sp
		
		sheet = book.sheet_by_name('define')
		nrows = sheet.nrows
		for i in range(nrows):
			defi = sheet.row_values(i)
			zzdcore1.defineDict[defi[0]] = defi[1]
		book.release_resources()

	def inputs(self, friend, waa):
		(head,sen)= self._trans_2_1(friend, waa)
		if head == u'none':
			outs = u'对不起，我不明白您的意思!错误信息\"%s\"'%sen
			self.sentence.append([waa,(head,sen),outs])
			return self._sorry((u'copy',outs))
		
		if self.state == 'init':
			if head == u'comm' and sen[0:2] == u'id':
				res = self._command(sen)
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
			for t in zzdcore1.inWaaClass:
				if t[0] == head:
					outs = t[1](self, sen)
					self.sentence.append([waa,(head,sen),outs])
					return outs
			outs = self._sorry(waa)
			self.sentence.append([waa,(head,sen),outs])
			return outs
		else:
			outs = u'对不起，我懵了!'
			return self._sorry((u'copy', outs))
		
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
	
	def _echo(self, sen):
		return sen
	
	def _debug(self, sen):
		outs = u'调试模式'
		return outs
	
	def _copy(self, sen):
		return sen
	
	def _none(self, sen):
		return self._sorry((u'copy', sen))
	
	def _trans_2_1(self, friend, waa):
		if not self._zj(friend, waa):
			return (None, waa)
		head = waa[0:4]
		sen = waa[5:len(waa)]
		return head, sen
	
	def _fenci(self, friend, senclass, waa):
		phrases = []
		con = True
		while con:
			for p in grammar.sp_all.keys():
				if waa.find(p) == 0:
					phrases.append(grammar.sp_all[p])
					waa = waa[len(p):]
					con = False
					break
			con = not con
		return phrases

	def _fensp(self, friend, senclass, phrases):
		print('KIKKK^^^^^^%s^^^^^^'%senclass)
		for t in grammar.grammar_all.keys():
			print t
		ag = grammar.grammar_all[senclass].ag
		print('^^^^^^%s^^^^^^'%senclass)
		for g in ag:
			sps = []
			phrs = []
			for p in phrases:
				phrs.append(p)
			for attr in g[1]:
				r = self._fensp_turn(friend, phrs, attr)
				if r[0] == None:
					break
				else:
					sps.append(r[0])
					phrs = r[1]
			if phrs != []:
				continue
			if len(sps) == 1:
				return sps[0]
			else:
				return grammar.sentencephrase(sps)
		return None
	
	def _fensp_turn(self, friend, phrs, attr):
		if phrs == []:
			return (None, None)
		
		sp = phrs.pop(0)
		if sp.be(attr):
			return (sp, phrs)
		sp = grammar.sentencephrase([sp])
		while phrs != []:
			sp.append(phrs.pop(0))
			if sp.be(attr):
				return (sp, phrs)
		return (None, None)
	
	def _zj(self, friend, senclass, waa):
		phrases = self._fenci(friend, senclass, waa)
		if phrases == []:
			return False
		sps = self._fensp(friend, senclass, phrases)
		if sps == None:
			return False
		
		self.cursen = sps
		attr_nor = senclass
		if self.cursen.be(attr_nor):
			return True
		else:
			self.cursen = None
			return False
	
	def _solve_head(self, friend, waa):
		return waa[0:4]
	
	def _solve_sen(self, friend, head, waa):
		return waa[5:len(waa)]
	
	def _solve_math(self, friend, head, waa):
		return waa[5:len(waa)]
	
	def _solve_define(self, friend, head, waa):
		return waa[5:len(waa)]
	
	def _solve_command(self, friend, head, waa):
		return waa[5:len(waa)]
	
	def _solve_copy(self, friend, head, waa):
		return waa[5:len(waa)]
	
	def _solve_debug(self, friend, head, waa):
		return waa[5:len(waa)]
	
	def _solve_echo(self, friend, head, waa):
		return waa[5:len(waa)]
	
	def _solve_none(self, friend, head, waa):
		return waa[5:len(waa)]
	
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
	print('hello')
	core0 = zzd_core0.zzdcore0()
	core1 = zzdcore1(core0)
	zzdcore1.init()
	fc = core1._zj(None, u'S命令语句甲', u'播放歌曲!')
	print fc
	fc = core1._zj(None, u'S命令语句甲', u'播放歌曲')
	print fc
	fc = core1._zj(None, u'测试语句', u'“一瞬间”')
	print fc
'''
'''

if __name__ == '__main__':
	main()
