#!/usr/bin/python3 -B
import threading
import gdata
import db
import time
import zmath
import play

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
		
	@classmethod
	def init(cls):
		db.gsinit()
		db.spinit()
		db.coreinit()
		
		cls.inWaaClass['math'] =  zzd._solve_math						#math
		cls.inWaaClass['define'] = zzd._solve_define					#define
		cls.inWaaClass['command'] = zzd._solve_command					#command
		cls.inWaaClass['set'] = zzd._solve_set							#set
		
	#运行在root进程
	def input(self, sour, waa):
		record = {'waa':waa, 'sour':sour, 'id':self.id_waain, 'time':time.time()}
		self.id_waain += 1
		self.waain.append(record)
		self.add_desire('input',record)
	
	def output(self, dest, waa):
		print('waa[0]',waa[0])
		print('waa[1]',waa[1])
		self.show(waa[0], waa[1])
		if waa[0]:
			dest.input(self, waa[0])
	
	def say(self, out, form):
		self.output(self.friend, (out, form))

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
		
		phrases = db.fenci(waa, False)
		if 'ask' in self.FSM:
			if self._solve_answer(phrases):
				return
		if not self.FSM['verify']:
			self._solve_command(phrases)
			return
		keyword = [x for x in phrases if x.s in gdata._keyword_zzd]
		bit = {'math':0,'define':0,'command':0, 'set':0}
		for k in keyword:
			assert k.s in gdata._keyword_zzd
			weight = gdata._keyword_zzd[k.s][0].split(' ')
			for i in range(0,len(weight),2):
				if weight[i] != '':
					bit[weight[i]] += int(weight[i+1])
		bit = sorted(bit.items(),key = lambda x:x[1],reverse = True)
		if bit[0][1] == 0:
			for ph in phrases:
				if ph.be('集合'):
					self._solve_set(phrases)
					break
			else:
				self._solve_other(phrases)
		else:
			zzd.inWaaClass[bit[0][0]](self, phrases)
		
	def _solve_math(self, phrases):
		sp = gdata.getgs('数学语句').fensp(phrases, True)
		if not sp:
			self.say('数学语法不对','')
		else:
			if '数学判断' in sp[2] or '数学方程' in sp[2]:
				self.add_desire('math',sp[0])
			else:
				sen = zmath.c2math(phrases)
				if sen:
					self.add_desire('math',sen)
				else:
					self.say('数学语法错误', '')
	
	def _solve_define(self, phrases):
		sp = gdata.getgs('定义语句').fensp(phrases, True)
		if sp == None:
			self.say('定义语法错误','')
		else:
			assert '定义词' in sp[2]
			sen = sp[2]['定义词']
			if sen in gdata._defineDict:
				explain = gdata._defineDict[sen]
				self.say('%s是%s'%(sen,explain), sp[0])
			else:
				self.say('对不起，我不知道什么是%s。请进入调教模式。'%sen, sp[0])
	
	def _solve_command(self, phrases):
		sp = gdata.getgs('命令语句').fensp(phrases, True)
		if sp == None:
			if not self.FSM['verify']:
				self.say('请先认证身份。','')
				arg = self.ask(['认证参数','认证参数句'])
				if arg:
					self.desire['verify'][1] = True
					self.desire['verify'][2][1] = arg[2]['认证参数']
			else:
				self.say('语法错误。','')
			return
		assert 'zzd命令' in sp[2]
		if '命令参数' in sp[2]:
			arg = sp[2]['命令参数']
		else:
			arg = ''
		exe = gdata._keyword_zzd[sp[2]['zzd命令']][1]
		if exe:
			self.say('还在开发中', sp[0].s)
			return
		if self.FSM['verify'] == False:
			if 'zzd认证命令' in sp[2]:
				self.desire['verify'][1] = True
				self.desire['verify'][2][1] = arg
			else:
				self.say('请先认证身份', sp[0].s)
			return
		if 'zzd认证命令' in sp[2]:
			self.say('请已经认证过身份了.同时服务多人功能正在开发中', '')
		elif 'zzd播放命令' in sp[2]:
			out = self.player.play(arg)
		elif 'zzd暂停命令' in sp[2]:
			out = self.player.pause()
		elif 'zzd继续命令' in  sp[2]:
			out = self.player.con()
		elif 'zzd停止命令' in sp[2]:
			out = self.player.stop(True)
		elif 'zzd再见命令' in sp[2]:
			self.add_desire('goodbye', '%s！'%sp[2]['zzd再见命令'])
		elif 'zzd问候命令' in sp[2]:
			self.say(sp[2]['zzd问候命令'],'')
		elif 'zzd保存命令' in sp[2]:
			self._command_save(sp)
		elif 'zzd学习命令' in sp[2] or 'zzd进入命令' in sp[2]:
			if self.FSM['train'] == False:
				self.say('好的，已进入%s模式'%sp[2]['zzd学习命令'], sp[0])
				self.FSM['train'] = True
			else:
				self.say('您已经是已%s模式了'%sp[2]['zzd学习命令'], sp[0])
		elif 'zzd退出命令' in sp[2]:
			mode = sp[2]['zzd学习命令'] if 'zzd学习命令' in sp[2] else '学习'
			if self.FSM['train'] == True:
				self.say('好的，已退出%s模式'%mode, sp[0])
				self.FSM['train'] = False
			else:
				self.say('您并没有在%s模式'%mode, sp[0].s)
		else:
			self.say('不识别的内置命令', '')

	def _command_save(self, sp):
		if not (self.infomation_a or self.infomation_A):
			self.say('没有信息需要写入数据库', sp[0].s)
			return
		if sp and '认证参数' in sp[2]:
			password = sp[2]['认证参数']
		else:
			self.say('请输入管理员口令','')
			password = self.ask(['认证参数句','认证参数'])
			if not password:
				self.say('您没有输入口令，写入取消。', '')
				return
			else:
				password = password[2]['认证参数']
		if password != self.managerid:
			self.say('口令错误，写入取消。', '')
			return
		while self.infomation_a:
			info = self.infomation_a.popitem()
			if not db.add_database_a_in_A(info[0], info[1]):
				self.say('%s信息写入失败'%info[0], '')
				self.infomation_a[info[0]]=info[1]
				break
		else:
			self.say('元素信息写入成功', '')
		
		while self.infomation_A:
			info = self.infomation_a.popitem()
			if not db.add_database_A_in_B(info[1], info[0]):
				self.say('%s信息写入失败'%info[0], '')
				self.infomation_a[info[0]]=info[1]
				break
		else:	
			self.say('集合信息写入成功', '')
		
		
	def _solve_set(self, phrases):
		sp = gdata.getgs('集合语句').fensp(phrases, True)
		if sp == None:
			self.say('集合语法不对',' ')
		else:
			if '集合判断语句' in sp[2]:
				if '...' in sp[2]:
					self.say('%s是未知的词.'%sp[2]['...'], sp[0])
					return
				assert '.' in sp[2]
				ph = gdata.getsp(sp[2]['.'])
				if ph.be(sp[2]['集合']):
					s = ''
					for ph in phrases[0:-1]:
						s += ph.s
					self.say(s, sp[0])
				else:
					self.say('对不起，我不知道', sp[0])
			else:
				assert '集合断言语句' in sp[2]
				if sp[0][-1] == '？' or sp[0][-1] == '吗':
					self.say('对不起，我不知道。', sp[0])
				if self.FSM['train'] == False:
					self.say('对不起，您需进入学习模式才可以增加信息', sp[0])
				else:
					assert '...' in sp[2]
					print('...:%s'%sp[2]['...'])
					sp_a,gs_A = sp[2]['...'].split('|')
					res = db.add_information_1(sp_a, gs_A)
					if res[0] == 0:
						self.say('好的，我记住了', sp[0])
						if sp_a in self.infomation_a:
							self.infomation_a[sp_a] += '~%s'%gs_A
						else:
							self.infomation_a[sp_a] = gs_A
					elif res[0] == 1:
						self.say('您的信息已经在我的知识库里了。原因：%s'%res[1], sp[0])
					else:
						self.say('您的信息与我的知识库冲突。原因:%s'%res[1], sp[0])

	def _solve_answer(self, phrases):
		assert 'ask' in self.FSM and not self.FSM['ask'][1]
		for question in self.FSM['ask'][0]:
			print('question:',question)
			sp = gdata.getgs(question).fensp(phrases, True)
			if sp:
				self.FSM['ask'][1] = sp
				self.ask_event.set()
				return True
		self.ask_event.set()
		return False
	
	def _solve_other(self, phrases):
		if gdata.getgs('称呼').fensp(phrases, True):
			self.say('我在，有什么为你做的吗','')
		else:
			self.say('对不起，我还需要学习','')
				
	def desire_verify(self, desire):
		if self.FSM['verify'] == True:
			desire[1] = False
			return
		desire[1] = False
		if desire[2][1] == '':
			if desire[2][0] > 0:
				desire[2][0] -= 1
				self.say('您好，我是小白，请认证身份！','')
				self.add_desire('time', (desire, True, time.time()+10))
				arg = self.ask(['认证参数','认证参数句'])
				if arg:
					self.desire['verify'][1] = True
					self.desire['verify'][2][1] = arg[2]['认证参数']
			else:
				self.say('您没有及时认证，我要休息了。','')
				self.add_desire('goodbye', '再见')
		else:
			if desire[2][1] in gdata._identifyDict:
				self.friend.name = gdata._identifyDict[desire[2][1]]
				self.FSM['verify'] = True
				self.say('%s您好，认证通过。%s很高兴为您服务。'%(self.friend.name, self.name),'')
				if self.desire['time'][1] == True:
					if len(self.desire['time'][2]) == 1:
						if self.desire['time'][2][0][0] == self.desire['verify']:
							self.desire['time'][1] == False
							self.desire['time'][2] = []
			else:
				self.say('认证失败。','')
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
		print(self.infomation_a)
		print(self.infomation_A)
		if self.infomation_a or self.infomation_A:
			self.say('您还有学习信息没有写入数据库,需要写入吗？', '')
			ok = self.ask(['答复语句'])
			if ok and '肯定语句' in ok[2]:
				self._command_save(None)
			else:
				self.say('丢弃学习信息。', '')
		self.say(desire[2][0],'')
		self.desire['time'][1] == False
		self.FSM['work'] = False

	def desire_math(self, desire):
		assert desire[2]
		eq = desire[2].pop(0)
		if not desire[2]:
			desire[1] = False
		
		if eq.find('x') != -1:
			eq1 = eq.replace("=","-(")+")"
			try:
				c = eval(eq1,{'x':1j})
				val = int(-c.real/c.imag)
				val = str(val)
			except:
				self.say('错误数学表达式', '')
		else:
			try:
				val = eval(eq)
				val = '对' if type(val) == bool and val else val
				val = '错' if type(val) == bool and not val else val
			except:
				self.say('错误数学表达式', '')
		self.say(val, eq)
	
	def ask(self, question):
		self.FSM['ask']=[question,'']
		self.ask_event.clear()
		self.ask_event.wait()
		res = self.FSM.pop('ask')[1]
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
	
def main():
	print('zzd_zzd')
	zzd.init()
	zhd = zzd(1, 1)
	
	a = '鸟是哺乳动物对吗'
	phs = db.fenci(a, False)
	for p in phs:
		print(p.s,'|')
	g = gdata.getgs('集合语句')
	sp = g.fensp(phs,True)
	print('sp[0]:',sp[0])
	print('sp[1]:',sp[1])
	print('sp[2]:',sp[2])
	for s in sp[2]:
		print(s,sp[2][s])
	
if __name__ == '__main__':
	main()
