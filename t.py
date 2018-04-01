# coding: utf-8

ops_rule = {
    u'+': 1,
    u'-': 1,
    u'*': 2,
    u'/': 2
}

class zzdLayer1:
	inSentenceClass = []		#输入语句类型
	outSentenceClass = []		#输出语句类型
	itemDict = {}
	defineDict = {}

	def __init__(self, corelayer0):
		self.sentence = []
		self.corelayer0 = corelayer0
		self.init()
'''
	def	_middle_to_after(self, s):
    	expression = []
    	ops = []
    	ss = s.split(u' ')
    	for item in ss:
        	if item in [u'+', u'-', u'*', u'/']:
            	while len(ops) >= 0:
                	if len(ops) == 0:
                    	ops.append(item)
                    	break
                	op = ops.pop()
                	if op == u'(' or ops_rule[item] > ops_rule[op]:
                    	ops.append(op)
                    	ops.append(item)
                    	break
                	else:
                    	expression.append(op)
        	elif item == u'(':
            	ops.append(item)
        	elif item == u')':
            	while len(ops) > 0:
                	op = ops.pop()
                	if op == '(':
                    	break
                	else:
                    	expression.append(op)
        	else:
            	expression.append(item)

    	while len(ops) > 0:
        	expression.append(ops.pop())

    	return expression
	
	def _cal(self, n1, n2, op):
    	if op == u'+':
        	return n1 + n2
    	if op == u'-':
        	return n1 - n2
    	if op == u'*':
        	return n1 * n2
    	if op == u'/':
        	return n1 / n2
 
	def _expression_to_value(self, expression):
    	stack_value = []
    	for item in expression:
        	if item in [u'+', u'-', u'*', u'/']:
            	n2 = stack_value.pop()
            	n1 = stack_value.pop()
            	result = self._cal(n1, n2, item)
            	stack_value.append(result)
        	else:
            	stack_value.append(int(item))
    	return stack_value[0]
''' 
	def _solvesen(self, sen):
		outs = u'对不起，我不知道如何处理.'
		return outs
	
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
		outs = u'solv:2'
		self._sen2expression(sen)
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
		buf = open('item.txt','r').readlines()
		for t in buf:
			t = t.decode('utf8')
			zzdLayer1.itemDict[t[0]] = t[2:len(t)-1]
		
		zzdLayer1._definesen_init(self)
		
		zzdLayer1.inSentenceClass.append([u'copy:', zzdLayer1._copysen])			#copy
		zzdLayer1.inSentenceClass.append([u'debu:', zzdLayer1._debugsen])			#debug
		zzdLayer1.inSentenceClass.append([u'sorr:', zzdLayer1._sorrysen])			#sorry
		zzdLayer1.inSentenceClass.append([u'judg:', zzdLayer1._judgesen])			#judge
		zzdLayer1.inSentenceClass.append([u'solv:', zzdLayer1._solvesen])			#solve
		zzdLayer1.inSentenceClass.append([u'defi:', zzdLayer1._definesen])			#define
		
		return
