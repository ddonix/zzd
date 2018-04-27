#!/usr/bin/python3 -B
import threading
import gdata
import db
import time
import zmath
import play
import sys
import sets

#除input函数运行在root主进程，其他函数运行在zhd线程.
class zzd():
	inWaaClass = {}		#输入语句类型
	infomation_a = {} # 'a':'A' a属于A
	infomation_A = {} # 'A':'B' A包含B
	def __init__(self, show, friend):
		assert show and friend
		self.show = show
		self.friend = friend
		
		self.root = True
		self.name = gdata._identifyDict['299792458']
		self.managerid = '314159'
		
		self.waain = []
		self.id_waain = 0
		
		self.player = play.player(self)
		#有限状态机Finite-state machine
		self.FSM = {'verify':False, 'work':True, 'train':False, 'play':self.player}
		
		#大凡物不得其平则鸣
		self.desire = {}
		self.desire['verify'] = [zzd.desire_verify, True, [3,'']]		#提醒3次认证身份，每20秒提醒一次。
		self.desire['input'] = [zzd.desire_input, False, []]
		self.desire['time'] = [zzd.desire_time, False, []]
		self.desire['math'] = [zzd.desire_math, False, []]
		self.desire['goodbye'] = [zzd.desire_goodbye, False, []]
		self.desire['think'] = [zzd.desire_think, False, []]
	
		self.ask_event = threading.Event()
		self.ask_event.clear()
		
		self.say_event = threading.Event()
		self.say_event.set()
		
	@classmethod
	def init(cls):
		db.fninit()
		db.gsinit()
		db.spinit()
		db.coreinit()
		
		cls.inWaaClass['math'] =  zzd._solve_math						#math
		cls.inWaaClass['command'] = zzd._solve_command					#command
		cls.inWaaClass['query'] = zzd._solve_query						#query
		cls.inWaaClass['judge'] = zzd._solve_judge						#judge
		cls.inWaaClass['affirm'] = zzd._solve_affirm					#affirm
		cls.inWaaClass['query'] = zzd._solve_query						#query
		
	#运行在root进程
	def input(self, sour, waa):
		record = {'waa':waa, 'sour':sour, 'id':self.id_waain, 'time':time.time()}
		self.id_waain += 1
		self.waain.append(record)
		self.add_desire('input',record)
	
	def output(self, dest, waa):
		print('waa',waa)
		self.show(waa)
		if waa:
			dest.input(self, waa)
	
	def say(self, out):
		self.say_event.wait()
		self.say_event.clear()
		self.output(self.friend, out)
		self.say_event.set()

	def get_desire(self):
		if not self.desire:
			return None
		if self.desire['input'][1]:
			return self.desire['input']
		if self.desire['verify'][1]:
			return self.desire['verify']
		if self.desire['math'][1]:
			return self.desire['math']
		if self.desire['time'][1]:
			return self.desire['time']
		if self.desire['goodbye'][1]:
			return self.desire['goodbye']
		if self.desire['think'][1]:
			return self.desire['think']
		return None
	
	def desire_input(self, desire):
		assert desire[2]
		waain = desire[2].pop(0)
		if not desire[2]:
			desire[1] = False
		
		waa = waain['waa']
		assert self.friend == waain['sour']
		
		sep = gdata.getsp_ok(waa)
		if 'ask' in self.FSM:
			if self._solve_answer(sep):
				return
		if not self.FSM['verify']:
			self._solve_command(sep)
			return
		keyword = [x for x in sep.d if x.s in gdata._keyword_zzd]
		if sep.s in gdata._keyword_zzd:
			keyword.append(sep)
		bit = {'math':0, 'query':0, 'judge':0, 'command':0, 'affirm':0}
		for k in keyword:
			assert k.s in gdata._keyword_zzd
			weight = gdata._keyword_zzd[k.s][0].split(' ')
			for i in range(0,len(weight),2):
				if weight[i] != '':
					bit[weight[i]] += int(weight[i+1])
		bit = sorted(bit.items(),key = lambda x:x[1],reverse = True)
		if bit[0][1] == 0:
			self._solve_other(sep)
		else:
			zzd.inWaaClass[bit[0][0]](self, sep)
		
	def _solve_math(self, sep):
		res = sep.be('数学语句')
		if res[0] != 0:
			self.say('数学语法不对')
		else:
			adapter = res[1][2]
			if '数学判断' in adapter or '数学方程' in adapter:
				self.add_desire('math',res[1][0])
			else:
				sen = zmath.c2math(sep.d)
				if sen:
					self.add_desire('math',sen)
				else:
					self.say('数学语法错误')
	
	def _solve_command(self, sep):
		res = sep.be('命令语句')
		if res[0] != 0:
			if not self.FSM['verify']:
				self.say('请先认证身份。')
				arg = self.ask(['认证参数','认证参数句'])
				if arg:
					self.desire['verify'][1] = True
					self.desire['verify'][2][1] = arg[2]['认证参数']
			else:
				self.say('语法错误。')
			return
		adapter = res[1][2]
		assert 'zzd命令' in adapter
		if '命令参数' in adapter:
			arg = adapter['命令参数']
		else:
			arg = ''
		exe = gdata._keyword_zzd[adapter['zzd命令']][1]
		if exe:
			self.say('还在开发中')
			return
		if self.FSM['verify'] == False:
			if 'zzd认证命令' in adapter:
				self.desire['verify'][1] = True
				self.desire['verify'][2][1] = arg
			else:
				self.say('请先认证身份')
			return
		if 'zzd认证命令' in adapter:
			self.say('请已经认证过身份了.同时服务多人功能正在开发中')
		elif 'zzd播放命令' in adapter:
			out = self.player.play(arg)
		elif 'zzd暂停命令' in adapter:
			out = self.player.pause()
		elif 'zzd继续命令' in  adapter:
			out = self.player.con()
		elif 'zzd停止命令' in adapter:
			out = self.player.stop(True)
		elif 'zzd再见命令' in adapter:
			self.add_desire('goodbye', '%s！'%adapter['zzd再见命令'])
		elif 'zzd问候命令' in adapter:
			self.say(adapter['zzd问候命令'])
		elif 'zzd保存命令' in adapter:
			self._command_save(sp)
		elif 'zzd学习命令' in adapter or 'zzd进入命令' in adapter:
			mode = adapter['zzd学习命令'] if 'zzd学习命令' in adapter else adapter['zzd模式定语_学习']
			if self.FSM['train'] == False:
				self.say('好的，已进入%s模式！每次最多包含一条信息。'%mode)
				self.FSM['train'] = True
			else:
				self.say('您已经是已%s模式了'%mode)
		elif 'zzd退出命令' in adapter:
			mode = adapter['zzd学习命令'] if 'zzd学习命令' in adapter else adapter['zzd模式定语_学习']
			if self.FSM['train'] == True:
				self.say('好的，已退出%s模式'%mode)
				self.FSM['train'] = False
			else:
				self.say('您并没有在%s模式'%mode)
		else:
			self.say('不识别的内置命令')

	def _command_save(self, sp):
		if not (self.infomation_a or self.infomation_A):
			print(self.infomation_a)
			print(self.infomation_A)
			self.say('没有信息需要写入数据库')
			return
		if sp and '认证参数' in adapter:
			password = adapter['认证参数']
		else:
			self.say('请输入管理员口令')
			password = self.ask(['认证参数句','认证参数'])
			if not password:
				self.say('您没有输入口令，写入取消。')
				return
			else:
				password = password[2]['认证参数']
		if password != self.managerid:
			self.say('口令错误，写入取消。')
			return
		while self.infomation_a:
			info = self.infomation_a.popitem()
			if not db.add_database_a_in_A(info[0], info[1]):
				self.say('%s信息写入失败'%info[0])
				self.infomation_a[info[0]]=info[1]
				break
		else:
			self.say('元素信息写入成功')
		
		while self.infomation_A:
			info = self.infomation_A.popitem()
			if not db.add_database_A_in_B(info[1], info[0]):
				self.say('%s信息写入失败'%info[0])
				self.infomation_A[info[0]]=info[1]
				break
		else:	
			self.say('集合信息写入成功')
	
	def _solve_affirm_fn(self, x, fn):
		self.say('增加函数信息. %s是%s'%(x,fn))
	
	def _solve_set_a(self, x, gs):
		res = db.add_information_1(x, gs)
		if res[0] == 0:
			if x in self.infomation_a:
				self.infomation_a[x] += '~%s'%gs
			else:
				self.infomation_a[x] = gs
			self.say('好的，我记住了')
		elif res[0] == 1:
			self.say('该信息已在知识库。原因：%s是%s, %s是%s'%(x,res[1],res[1],gs))
		else:
			self.say('该信息与知识库冲突。原因：%s是%s, %s与%s不相容'%(x,res[1],res[1],gs))
					
	def _solve_set_A(self, x, gs):
		if not gdata.spin(x):
			db.add_information_1(x, '集合')
			self.infomation_a[x] = '集合'
		res = db.add_information_2(x, gs)
		if res[0] == 0:
			if x in self.infomation_A:
				self.infomation_A[gs] += '~%s'%x
			else:
				self.infomation_A[gs] = x
			self.say('好的，我记住了')
		elif res[0] == 1:
			if x == res[1]:
				self.say('该信息已在知识库。原因：%s是%s'%(x, gs))
			else:
				self.say('该信息已在知识库。原因：%s是%s, %s是%s'%(x, res[1], res[1], gs))
		else:
			self.say('该信息与知识库冲突。原因:%s与%s冲突'%(res[1][0],res[1][1]))
	
	def _solve_query(self, sep):
		res = sep.be('询问语句')
		if res[0] != 0:
			self.say('询问语法不对')
		else:
			adapter = res[1][2]
			for a in adapter:
				print(a,adapter[a])

	def _solve_judge(self, sep):
		res = sep.be('判断语句')
		if res[0] != 0:
			self.say('判断语法不对')
		else:
			adapter = res[1][2]
			if '集合' not in adapter:
				assert '...' in adapter
				assert '|' in adapter['...']
				x1,x2 = adapter['...'].split('|')
			else:
				assert '集合判断语句' in adapter
				assert '集合' in adapter
				if '|' not in adapter['集合']:
					assert '...' in adapter
					x1 = adapter['...']
					x2 = adapter['集合']
				else:
					if '(包含)' in adapter:
						x2,x1 = adapter['集合'].split('|')
					else:
						x1,x2 = adapter['集合'].split('|')
			if not gdata.spin(x1):
				self.say('%s是未知的词.您可以在学习模式进行学习'%x1)
				return
			res = gdata.getsp(x1).be(x2)
			if res[0] == 0:
				self.say('是的')
			elif res[0] == 1:
				self.say('错误')
			else:
				self.say('%s.需要我上网问问吗？'%res[1])
				ok = self.ask(['选择回答语句'])
				if ok and '肯定回答语句' in ok[2]:
					self.say('我还不会上网，逗你玩呢.哈哈哈')
				elif ok and '否定回答语句' in ok[2]:
					self.say('好的')

	def _solve_affirm(self, sep):
		res = sep.be('断言语句')
		if res[0] != 0:
			self.say('断言语法不对')
		else:
			adapter = res[1][2]
			if '待定断言语句' in adapter:
				assert '...' in adapter
				assert '|' in adapter['...']
				x,fn=adapter['...'].split('|')
				self._solve_affirm_fn(x,fn)
				return
			
			assert '集合断言语句' in adapter
			assert '集合' in adapter
			if '|' not in adapter['集合']:
				assert '...' in adapter
				x = adapter['...']
				gs = adapter['集合']
			else:
				if '(包含)' in adapter:
					gs,x = adapter['集合'].split('|')
				else:
					x,gs = adapter['集合'].split('|')
			assert gdata.gsin(gs)
			if self.FSM['train'] == False:
				self.say('对不起，您需进入学习模式才可以增加信息')
				return
			if '属于断言语句' in adapter:
				self._solve_set_a(x, gs)
			elif '包含断言语句' in adapter:
				self._solve_set_A(x, gs)
			else:
				if gdata.spin(x):
					assert not gdata.getsp(x).be('集合')[0] == 0
					self._solve_set_a(x, gs)
				else:	
					self.say('我不知道%s是否是集合。是吗'%x)
					ok = self.ask(['选择回答语句'])
					if ok and '肯定回答语句' in ok[2]:
						self._solve_set_A(x, gs)
					elif ok and '否定回答语句' in ok[2]:
						self._solve_set_a(x, gs)
					else:
						self.say('您没有给出肯定或否定，我将丢弃%s这条信息。'%sp[0])

	def _solve_answer(self, sep):
		assert 'ask' in self.FSM and not self.FSM['ask'][1]
		for question in self.FSM['ask'][0]:
			print('question:',question)
			res = sep.be(question)
			if res[0] == 0:
				self.FSM['ask'][1] = res[1]
				self.ask_event.set()
				return True
		self.ask_event.set()
		return False
	
	def _solve_other(self, sep):
		if sep.be('称呼')[0] == 0:
			self.say('我在，有什么为你做的吗')
			return
		for ph in sep.d:
			if ph.be('集合')[0] == 0:
				self._solve_affirm(sep)
				return
		phrases = sep.d if sep.d else [sep]
		s = phrases[0].s
		for ph in phrases[1:]:
			s += '~%s'%ph.s
		self.say('对不起，我处理不利.分词结果是:%s'%s)
		n = ['']
		while phrases:
			if len(phrases[0].s) == 1 and len(phrases[0].gs) == 1:
				n[-1] += phrases[0].s
			else:
				n.append('')
			phrases = phrases[1:]
		l = 0
		rr = ''
		for nc in n:
			if nc:
				l += 1
				rr +='%s '%nc
		if l:
			r ='我猜测：%s是新词，您可以进入学习模式进行学习:'%rr
		self.say(r)
				
	def desire_verify(self, desire):
		if self.FSM['verify'] == True:
			desire[1] = False
			return
		desire[1] = False
		if desire[2][1] == '':
			if desire[2][0] > 0:
				desire[2][0] -= 1
				self.say('您好，我是小白，请认证身份！')
				self.add_desire('time', (desire, True, time.time()+10))
				arg = self.ask(['认证参数','认证参数句'])
				if arg:
					self.desire['verify'][1] = True
					self.desire['verify'][2][1] = arg[2]['认证参数']
			else:
				self.say('您没有及时认证，我要休息了。')
				self.add_desire('goodbye', '再见')
		else:
			if desire[2][1] in gdata._identifyDict:
				self.friend.name = gdata._identifyDict[desire[2][1]]
				self.FSM['verify'] = True
				self.say('%s您好，认证通过。%s很高兴为您服务。'%(self.friend.name, self.name))
				if self.desire['time'][1] == True:
					if len(self.desire['time'][2]) == 1:
						if self.desire['time'][2][0][0] == self.desire['verify']:
							self.desire['time'][1] == False
							self.desire['time'][2] = []
			else:
				self.say('认证失败。')
				if desire[2][0] > 0:
					desire[2][1] == ''
					desire[2][0] -= 1
					self.add_desire('time', (desire, True, time.time()+20))
				arg = self.ask(['认证参数','认证参数句'])
				if arg:
					self.desire['verify'][1] = True
					self.desire['verify'][2][1] = arg[2]['认证参数']
	
	def desire_think(self, desire):
		return None
	
	def desire_time(self, desire):
		if not desire[2]:
			desire[1] = False
			return
		for i in range(len(desire[2])-1, -1, -1):
			if time.time() >= desire[2][i][2]:
				desire[2][i][0][1] = desire[2][i][1]
				desire[2].pop(i)
		if not desire[2]:
			desire[1] = False
	
	def desire_goodbye(self, desire):
		assert desire[2]
		desire[1] = False
		self.player.stop(False)
		if self.infomation_a or self.infomation_A:
			self.say('您还有学习信息没有写入数据库,需要写入吗？')
			ok = self.ask(['选择回答语句'])
			if ok and '肯定回答语句' in ok[2]:
				self._command_save(None)
			else:
				self.say('丢弃学习信息。')
		self.say(desire[2][0])
		self.desire['time'][1] == False
		self.FSM['work'] = False

	def desire_math(self, desire):
		assert desire[2]
		eq = desire[2].pop(0)
		if not desire[2]:
			desire[1] = False
		
		print(eq)
		if eq.find('x') != -1:
			eq1 = eq.replace("=","-(")+")"
			try:
				c = eval(eq1,{'x':1j})
				val = int(-c.real/c.imag)
				val = str(val)
			except:
				self.say('错误数学表达式')
		else:
			try:
				val = eval(eq)
				val = '对' if type(val) == bool and val else val
				val = '错' if type(val) == bool and not val else val
			except:
				self.say('错误数学表达式')
		self.say(val)

	#只能有一个问题被回答。如果上一个问题没有回答，则丢弃上一个问题。
	#这符合人的行为.
	def ask(self, question):
		if 'ask' in self.FSM:
			self.ask_event.set()
			while 'ask' in self.FSM:
				time.sleep(0.1)
		self.FSM['ask']=[question,'']
		self.ask_event.clear()
		self.ask_event.wait()
		res = self.FSM.pop('ask')[1]
		print(res)
		print(res[0])
		return res
	
	def live(self):
		while self.FSM['work'] and self.root:
			d = self.get_desire()
			if d:
				t = threading.Thread(target=desire_thread, args=(self, d))
				t.start()
			time.sleep(0.5)
		self.player.stop(False)
		self.ask_event.set()
				
	def add_desire(self, name, arg):
		self.desire[name][1] = True
		self.desire[name][2].append(arg)
	
def desire_thread(core, d):
	d[0](core,d)
	
def main(a,A):
	print('zzd_zzd')
	zzd.init()
	zhd = zzd(1, 1)
	
	sp = gdata.getsp_ok(a)
	res = sp.be(A)
	print(res)
	
if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
'''
	phs = db.fenci(a, False)
	for p in phs:
		print(p.s,'|')
	g = gdata.getgs(A)
	sp = g.fensp(phs,True)
	print('sp[0]:',sp[0])
	print('sp[1]:',sp[1])
	print('adapter:',adapter)
	for s in adapter:
		print(s,adapter[s])
'''	
