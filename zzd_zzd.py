#!/usr/bin/python3 -B
import threading
import db
import time
import zmath
import play

#除input函数运行在root主进程，其他函数运行在zhd线程.
class zzd():
	inWaaClass = {}		#输入语句类型
	def __init__(self, show, friend):
		assert show and friend
		self.show = show
		self.friend = friend
		
		self.root = True
		self.name = db.database._identifyDict['299792458']
		
		self.waain = []
		self.id_waain = 0
		
		self.player = play.player(self)
		#有限状态机Finite-state machine
		self.FSM = {'verify':False, 'work':True, 'play':self.player}
		
		#大凡物不得其平则鸣
		self.desire = {}
		self.desire['verify'] = [zzd.desire_verify, True, [3,'']]		#提醒3次认证身份，每20秒提醒一次。
		self.desire['input'] = [zzd.desire_input, False, []]
		self.desire['time'] = [zzd.desire_time, False, []]
		self.desire['math'] = [zzd.desire_math, False, []]
		self.desire['think'] = [zzd.desire_think, False, []]
	
		self.ask_event = threading.Event()
		self.ask_event.clear()
		
	@classmethod
	def init(cls):
		db.database.gsinit()
		db.database.spinit()
		db.database.coreinit()
		
		cls.inWaaClass['verify'] = zzd._solve_verify					#verify
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
		if waa[0] == '再见！' or waa[0] == '拜拜！':
			self.FSM['work'] = False
	
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
		keyword = [x for x in phrases if x.s in db.database._keyword_zzd]
		bit = {'verify':0,'math':0,'define':0,'command':0,'system':0}
		for k in keyword:
			assert k.s in db.database._keyword_zzd
			weight = db.database._keyword_zzd[k.s][0].split(' ')
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
			if 'ask' in self.FSM:
				self.ask_event.set()
			zzd.inWaaClass[bit[0][0]](self, phrases)
		
	def _solve_verify(self, phrases):
		sp = db.database.gs('认证语句')._fensp(phrases, True)
		if sp == None:
			self.say('认证语法不对', '')
		else:
			self.say('', sp[0].s)
			if self.FSM['verify'] == True:
				self.say('您已经认证过身份了。服务多人功能正在开发中，请耐心等待。', '')
			else:
				if '认证参数' in sp[2]:
					self.desire['verify'][1] = True
					self.desire['verify'][2][1] = sp[2]['认证参数']
				else:
					self.say('口令是什么？', '')
					arg = self.ask('认证参数')
					if arg:
						self.desire['verify'][1] = True
						self.desire['verify'][2][1] = arg

	def _solve_math(self, phrases):
		sp = db.database.gs('数学语句')._fensp(phrases, True)
		if not sp:
			self.say('数学语法不对','')
		else:
			if '数学判断' in sp[2] or '数学方程' in sp[2]:
				self.add_desire('math',sp[0].s)
			else:
				sen = zmath.c2math(phrases)
				if sen:
					self.add_desire('math',sen)
				else:
					self.say('数学语法错误', '')
	
	def _solve_define(self, phrases):
		sp = db.database.gs('定义语句')._fensp(phrases, True)
		if sp == None:
			self.say('定义语法错误','')
		else:
			assert '定义词' in sp[2]
			sen = sp[2]['定义词']
			if sen in db.database._defineDict:
				explain = db.database._defineDict[sen]
				self.say('%s是%s'%(sen,explain), sp[0].s)
			else:
				self.say('对不起，我不知道什么是%s。请进入调教模式。'%sen, sp[0].s)
	
	def _solve_command(self, phrases):
		sp = db.database.gs('命令语句')._fensp(phrases, True)
		if sp == None:
			self.say('命令语法不对','')
		else:
			assert 'zzd命令' in sp[2]
			self.say('', sp[0].s)
			exe = db.database._keyword_zzd[sp[2]['zzd命令']][1]
			if exe == '' or exe == None:
				if '命令参数' in sp[2]:
					arg = sp[2]['命令参数']
				else:
					arg = ''
				if 'zzd播放命令' in sp[2]:
					out = self.player.play(arg)
				elif 'zzd暂停命令' in sp[2]:
					out = self.player.pause()
				elif 'zzd继续命令' in  sp[2]:
					out = self.player.con()
				elif 'zzd停止命令' in sp[2]:
					out = self.player.stop(True)
				elif 'zzd再见命令' in sp[2]:
					self.player.stop(False)
					self.say('%s！'%sp[2]['zzd再见命令'], '')
				else:
					self.say('不识别的内置命令', '')
			else:
				self.say('还在开发中', '')

	def _solve_set(self, phrases):
		sp = db.database.gs('集合语句')._fensp(phrases, True)
		if sp == None:
			self.say('集合语法不对',' ')
		else:
			assert '集合' in sp[2]
			assert '.' in sp[2]
			print(sp[2]['.'])
			print(sp[2]['集合'])
			
			ph = db.database.sp(sp[2]['.'])
			if ph.be(sp[2]['集合']):
				s = ''
				for ph in phrases[0:-1]:
					s += ph.s
				self.say(s, sp[0].s)
			else:
				self.say('对不起，我不知道', sp[0].s)

	def _solve_other(self, phrases):
		if 'ask' in self.FSM:
			sp = db.database.gs(self.FSM['ask'][0])._fensp(phrases, True)
			if sp:
				self.FSM['ask'][1]=sp[0].s
			self.ask_event.set()
		else:
			self.say('对不起，我还需要调教！','')
				
	def desire_verify(self, desire):
		if self.FSM['verify'] == True:
			desire[1] = False
			return
		desire[1] = False
		if desire[2][1] == '':
			if desire[2][0] > 0:
				desire[2][0] -= 1
				self.say('您好，我是小白，请认证身份！','')
				arg = self.ask('认证参数')
				if arg:
					self.desire['verify'][1] = True
					self.desire['verify'][2][1] = arg
				self.add_desire('time', (desire, True, time.time()+20))
			else:
				self.say('您没有及时认证，小白要休息了。','')
				self.say('再见！','')
		else:
			if desire[2][1] in db.database._identifyDict:
				self.friend.name = db.database._identifyDict[desire[2][1]]
				self.FSM['verify'] = True
				self.say('%s您好，认证通过。%s很高兴为您服务。'%(self.friend.name, self.name),'')
			else:
				self.say('认证失败。','')
				if desire[2][0] > 0:
					desire[2][1] == ''
					desire[2][0] -= 1
					self.add_desire('time', (desire, True, time.time()+20))
	
	def desire_think(self, desire):
		return None
	
	def desire_time(self, desire):
		assert desire[2]
		for i in range(len(desire[2])-1, -1, -1):
			if time.time() >= desire[2][i][2]:
				desire[2][i][0][1] = desire[2][i][1]
				desire[2].pop(i)
		if not desire[2]:
			desire[1] = False
	
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
			time.sleep(0.1)
		if 'ask' in self.FSM:
			self.ask_event.set()
			while 'ask' in self.FSM:
				time.sleep(1)
				break
				
	def add_desire(self, name, arg):
		self.desire[name][1] = True
		self.desire[name][2].append(arg)
	
def desire_thread(core, d):
	print('...%s...'%threading.currentThread().name)
	d[0](core,d)

def main():
	print('zzd_zzd')
	zzd.init()
	zhd = zzd(1, 1)
	
	a = '苏格拉底会死吗？'
	phs = db.fenci(a, False)
	g = db.database.gs('集合语句')
	sp = g._fensp(phs,True)
	print(sp[0].s)
	print(sp[1])
	print(sp[2])
	for s in sp[2]:
		print(s,sp[2][s])
	
if __name__ == '__main__':
	main()
