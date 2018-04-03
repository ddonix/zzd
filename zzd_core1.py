# coding: utf-8
import zzd_core0
#init:初始化。
#stand：完成一次交互，等待下一次交互。没有预期。
#wait:期待human的回应。有预期。
#initiative:主动状态，主动发起对话。
STATE = ('init', 'stand', 'wait', 'initiative')

#0:工作模式；1:娱乐模式;2:训练模式;3:调试模式.
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
	
	def _debug(self, sen):
		outs = u'调试模式'
		return outs
	
	def inputs(self, friend, waa):
		(head,sen)= self._trans_2_1(friend, waa)
		if head == u'none':
			outs = u'对不起，我不明白您的意思!错误信息\"%s\"'%sen
			self.sentence.append([waa,(head,sen),outs])
			return self._sorry((u'copy',outs))
		
		if self.state == 'init':
			if head == u'comm' and sen[0:2] == u'认证':
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
	
	@classmethod
	def init(cls):
		zzd_core0.zzdcore0.init()
		
		zzdcore1._define_init()
		zzdcore1.inWaaClass.append([u'math', zzdcore1._math])		#math
		zzdcore1.inWaaClass.append([u'defi', zzdcore1._define])	#define
		zzdcore1.inWaaClass.append([u'comm', zzdcore1._command])			#command
		zzdcore1.inWaaClass.append([u'copy', zzdcore1._copy])			#copy
		zzdcore1.inWaaClass.append([u'debu', zzdcore1._debug])			#debug
		
	@classmethod
	def _define_init(cls):
		zzdcore1.defineDict[u'爱'] = u'在一起'
	
	def _define(self, sen):
		o = zzdcore1.defineDict.get(sen)
		if o == None:
			return self._sorry((u'defi',sen))
		return sen+u'是'+o
	
	def _copy(self, sen):
		outs = sen
		return outs
	
	def _command(self, sen):
		if sen[0:2] == u'认证':
			if self.state != 'init':
				return (True, u'您已经认证过身份了。服务多人功能正在开发中，请耐心等待。')
			elif len(sen) == 10 and sen[2:10] == u'12345678':
				return (True, u'您的身份认证通过。谢谢您回来，您有什么想对我说的吗？')
			else:
				return (False, u'认证失败。请重新认证。')
		else:
			return self._sorry((u'comm', sen))
	
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
	
	def _trans_2_1(self, friend, waa):
		head = waa[0:4]
		sen = waa[5:len(waa)]
		return head, sen
	
	def _trans_1_2(self, waa):
		return waa
	
	def _trans_2_1(self, friend, waa):
		head = self._solve_head(friend, waa)
		sen = self._solve_sen(friend, head, waa)
		return head, sen
	
	def _trans_1_2(self, waa):
		return waa
	
	def _solve_head(self, friend, waa):
		return waa[0:4]
	
	def _solve_sen(self, friend, head, waa):
		return waa[5:len(waa)]
