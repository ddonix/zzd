# coding: utf-8

#init:初始化。
#stand：完成一次交互，等待下一次交互。没有预期。
#wait:期待human的回应。有预期。
#initiative:主动状态，主动发起对话。
STATE = ('init', 'stand', 'wait', 'initiative')

#0:工作模式；1:娱乐模式;2:训练模式;3:调试模式.
MODE = ('work', 'train', 'debug')

class zzdLayer1:
	inSentenceClass = []		#输入语句类型
	defineDict = {}

	def __init__(self, corelayer0):
		self.sentence = []
		self.corelayer0 = corelayer0
		self.state = 'init'
		self.mode = 'work'
		self.init()
	
	def _solvesen(self, sen):
		eq = sen[5:len(sen)]
		if eq.find(u'x') != -1:
			eq1 = eq.replace("=","-(")+")"
			try:
				c = eval(eq1,{u'x':1j})
				val = int(-c.real/c.imag)
				val = u'x='+str(val)
			except:
				return self._sorrysen(sen)
		else:
			try:
				val = eval(eq)
				if val == True:
					val = u'对'
				else:
					val = u'错'
			except:
				return self._sorrysen(sen)
		
		return 'solv:'+val
	
	def _debugsen(self, sen):
		outs = u'debu:调试模式'
		return outs
	
	def inputs(self, sen):
		outs = None
		if self.mode == 'work':
			for t in zzdLayer1.inSentenceClass:
				if t[0] == sen[0:5]:
					outs = t[1](self, sen)
					break
			if outs == None:
				outs = self._sorrysen(sen)
		
			self.sentence.append([sen,outs])
			return outs
		elif self.mo
	
	def init(self):
		zzdLayer1._definesen_init(self)
		zzdLayer1.inSentenceClass.append([u'copy:', zzdLayer1._copysen])			#copy
		zzdLayer1.inSentenceClass.append([u'debu:', zzdLayer1._debugsen])			#debug
		zzdLayer1.inSentenceClass.append([u'sorr:', zzdLayer1._sorrysen])			#sorry
		zzdLayer1.inSentenceClass.append([u'solv:', zzdLayer1._solvesen])			#solve
		zzdLayer1.inSentenceClass.append([u'defi:', zzdLayer1._definesen])			#define
	
	def _definesen_init(self):
		zzdLayer1.defineDict[u'爱'] = u'在一起'
	
	def _definesen(self, sen):
		define = sen[5:len(sen)]
		o = zzdLayer1.defineDict.get(define)
		if o == None:
			return self._sorrysen(u'copy:对不起，我没有\"'+define+u'\"的定义。'+u'请进入训练模式，添加定义。')
		return sen+u'是'+o
	
	def _copysen(self, sen):
		outs = sen
		return outs
	
	def _sorrysen(self, sen):
		if sen[0:5] == u'copy:':
			return sen
		else:
			outs = u'sorr:对不起，我无法处理\"'+sen+'\"'
			return outs
