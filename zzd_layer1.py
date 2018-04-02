# coding: utf-8
import voice 

class zzdLayer1:
	inSentenceClass = []		#输入语句类型
	outSentenceClass = []		#输出语句类型
	defineDict = {}

	def __init__(self, corelayer0):
		self.sentence = []
		self.corelayer0 = corelayer0
		self.init()
		voice.voiceInit()
	
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
	
	def _sorrysen(self, sen):
		outs = u'sorr:对不起，我无法处理\"'+sen+'\"'
		return outs
	
	def _copysen(self, sen):
		outs = sen
		return outs
	
	def _debugsen(self, sen):
		outs = u'debug模式'
		return outs
	
	def _definesen_init(self):
		zzdLayer1.defineDict[u'爱'] = u'在一起'
	
	def _definesen(self, sen):
		outs = u'defi:'
		o = zzdLayer1.defineDict.get(sen[5:len(sen)])
		if o == None:
			return self._sorrysen(sen)
		return outs+o
        
	def inputs(self, sen):
		outs = None
		for t in zzdLayer1.inSentenceClass:
			if t[0] == sen[0:5]:
				outs = t[1](self, sen)
				break
		if outs == None:
			outs = self._sorrysen(sen)
		
		self.sentence.append([sen,outs])
		return outs
	
	def init(self):
		zzdLayer1._definesen_init(self)
		zzdLayer1.inSentenceClass.append([u'copy:', zzdLayer1._copysen])			#copy
		zzdLayer1.inSentenceClass.append([u'debu:', zzdLayer1._debugsen])			#debug
		zzdLayer1.inSentenceClass.append([u'sorr:', zzdLayer1._sorrysen])			#sorry
		zzdLayer1.inSentenceClass.append([u'solv:', zzdLayer1._solvesen])			#solve
		zzdLayer1.inSentenceClass.append([u'defi:', zzdLayer1._definesen])			#define
