#!/usr/bin/python3 -B
dict0={'0':0,'1':1,'2':2, '3':3,'4':4, '5':5, '6':6, '7':7, '8':8,'9':9, '+':10, '-':11}
dict1={'零':0,'一':1,'二':2, '三':3,'四':4, '五':5, '六':6, '七':7, '八':8,'九':9}
dict2={'十':10,'百':100,'千':1000,'万':10000}

def transNumber(data):
	if dict0.get(data[0]):		#12,-123,+123
		return int(data)
	if data[0] == '负':
		sign = -1
		data = data[1:]
	elif data[0] == '正':
		sign = 1
		data = data[1:]
	else:
		sign = 1
	
	if len(data) == 1:			#一，二，十
		return (10 if data[0] == '十' else dict1[data[0]])*sign
		
	if data[0] == '十':		#十五,十六
		res = 10+dict1[data[1]]
		return res*sign
		
	if not dict2.get(data[1]):	#五六八,二四
		res = ''
		for d in data:
			res += str(dict1[d])
		return int(res)*sign
	
	res = 0						#三百二十，四百五十六
	for i,d in enumerate(data):
		r=dict2.get(d)
		if r:
			res += r*dict1[data[i-1]]
	r = dict1.get(data[-1])
	if r:
		res += r
	return res*sign


def c2math(phrases):
	res = []
	tran1 = {'加':'+','加上':'+', '减':'-','减去':'-','乘以':'*', '除以':'/', '大于':'>','小于':'<','等于':'==','大于等于':'>=','小于等于':'<=', '不等于':'!='}
	tran2 = {'乘':'*','除':'/'}
	x = False
	rv = False
	for ph in phrases:
		if ph.be('汉语变量')[0] == True:
			x = True
			break
	for i,ph in enumerate(phrases):
		if ph.be('汉语数')[0] == True:
			if not rv:
				res.append(str(transNumber(ph.s)))
			else:
				t = res[-2]
				res[-2] = str(transNumber(ph.s))
				res.append(t)
		if ph.be('数')[0] == True:
			if not rv:
				res.append(ph.s)
			else:
				t = res[-2]
				res[-2] = transNumber(ph.s)
				res.append(t)
		if ph.be('汉语变量')[0] == True:
			if not rv:
				res.append('x')
			else:
				t = res[-2]
				res[-2] = 'x'
				res.append(t)
				
		if ph.be('汉语运算符')[0] == True:
			if ph.s in tran1:
				rv = False
				res.append(tran1[ph.s])
			else:
				rv = True
				print(ph.s)
				res.append(tran2[ph.s])
		if ph.be('汉语赋值符')[0] == True:
			if x:
				res.append('=')
			else:
				res.append('==')
	return ''.join(res)

def main():
	print('math')

if __name__ == '__main__':
	main()
