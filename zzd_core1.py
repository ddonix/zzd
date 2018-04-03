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
	inSentenceClass = []		#输入语句类型
	defineDict = {}

	def __init__(self, corelayer0):
		self.sentence = []
		self.corelayer0 = corelayer0
		self.state = 'init'
		self.mode = 'work'
		self.friend = None

	def _solvesen(self, sen):
		eq = sen
		if eq.find(u'x') != -1:
			eq1 = eq.replace("=","-(")+")"
			try:
				c = eval(eq1,{u'x':1j})
				val = int(-c.real/c.imag)
				val = u'x='+str(val)
			except:
				return self._sorry((u'solv', sen))
		else:
			try:
				val = eval(eq)
				if val:
					val = u'对'
				else:
					val = u'错'
			except:
				return self._sorry((u'solv', sen))
		return val
	
	def _debugsen(self, sen):
		outs = u'调试模式'
		return outs
	
	def inputs(self, friend, waa):
		if self.state == 'init':
			if waa[0] == u'comm' and waa[1][0:2] == u'认证':
				res = self._commandsen(waa[1])
				if res[0]:
					self.state = 'stand'
					self.friend = friend
				return res[1]
			else:
				return self._sorry((u'copy', u'对不起，您需要先进行身份认证!'))
		if self.mode == 'work':
			for t in zzdcore1.inSentenceClass:
				if t[0] == waa[0]:
					outs = t[1](self, waa[1])
					self.sentence.append([waa,outs])
					return outs
			outs = self._sorry(waa)
			self.sentence.append([waa,outs])
			return outs
	
	@classmethod
	def init(cls):
		zzd_core0.zzdcore0.init()
		
		zzdcore1._definesen_init()
		zzdcore1.inSentenceClass.append([u'solv', zzdcore1._solvesen])			#solve
		zzdcore1.inSentenceClass.append([u'defi', zzdcore1._definesen])			#define
		zzdcore1.inSentenceClass.append([u'comm', zzdcore1._commandsen])		#identify
		zzdcore1.inSentenceClass.append([u'copy', zzdcore1._copysen])			#copy
		zzdcore1.inSentenceClass.append([u'debu', zzdcore1._debugsen])			#debug
		
	@classmethod
	def _definesen_init(cls):
		zzdcore1.defineDict[u'爱'] = u'在一起'
	
	def _definesen(self, sen):
		o = zzdcore1.defineDict.get(sen)
		if o == None:
			return self._sorry((u'defi',sen))
		return sen+u'是'+o
	
	def _copysen(self, sen):
		outs = sen
		return outs
	
	def _commandsen(self, sen):
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
		elif waa[0] == u'solv':
			return u'对不起，我无法计算\"'+waa[1]+u'\"。请检查表达式。'
		elif waa[0] == u'comm':
			return u'对不起，我无法执行\"'+waa[1]+u'\"。请检查命令。'
		else:
			return u'对不起，我无法处理\"'+waa[1]+u'\"。'