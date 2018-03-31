# coding: utf-8

class zzdLayer1:
	inSentenceClass = []		#输入语句类型
	outSentenceClass = []		#输出语句类型
	defineDict = {u'pi':u'3.14159'}
    
	def __init__(self, corelayer0):
		self.sentence = []
		self.corelayer0 = corelayer0
		self.initfun()
	
	def _sorrysen(self, sen):
		outs = u'对不起，我不知道如何处理.'
		return outs
	
	def _copysen(self, sen):
		outs = sen
		return outs
	
	def _debugsen(self, sen):
		outs = u'debug模式'
		return outs
	
	def _judgesen(self, sen):
		outs = u'judg:True'
		return outs
	
	def _solvesen(self, sen):
		outs = u'solv:True'
		return outs
	
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
	
	def initfun(self):
		zzdLayer1.inSentenceClass.append([u'copy:', zzdLayer1._copysen])			#copy
		zzdLayer1.inSentenceClass.append([u'debu:', zzdLayer1._debugsen])			#debug
		zzdLayer1.inSentenceClass.append([u'sorr:', zzdLayer1._sorrysen])			#sorry
		zzdLayer1.inSentenceClass.append([u'judg:', zzdLayer1._judgesen])			#judge
		zzdLayer1.inSentenceClass.append([u'solv:', zzdLayer1._solvesen])			#solve
		zzdLayer1.inSentenceClass.append([u'defi:', zzdLayer1._definesen])			#define
		return
