#!/usr/bin/python3 -B
import threading
import time
import zmath
import play 
import sys
from seting import sets
from seting import stickset
from seting import enumset
import kdb

#除input函数运行在root主进程，其他函数运行在zhd线程.
class zzd():
    inWaaClass = {}        #输入语句类型
    def __init__(self, show, friend):
        assert show and friend
        self.show = show
        self.friend = friend
        
        #知识库Knowledge DataBase
        self.KDB = kdb.ZZDKDB()
        self.player = play.player(self)
        #有限状态机Finite-state machine
        self.FSM = {'verify':False, 'work':True, 'train':False, 'play':self.player}
        
        self.root = True
        self.name = self.KDB.identify['299792458']
        self.managerid = '314159'
        
        self.waain = []
        self.id_waain = 0
        
        #大凡物不得其平则鸣
        self.desire = {}
        self.desire['verify'] = [zzd.desire_verify, True, '']        #提醒认证身份,1分钟后没认证退出
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
        cls.inWaaClass['math'] =  zzd._solve_math                        #math
        cls.inWaaClass['command'] = zzd._solve_command                    #command
        cls.inWaaClass['judge'] = zzd._solve_judge                        #judge
        cls.inWaaClass['affirm'] = zzd._solve_affirm                    #affirm
        cls.inWaaClass['query'] = zzd._solve_query                        #query
        
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
        
        se = self.KDB.getse(waa)
        if 'ask' in self.FSM:
            if self._solve_answer(se):
                return
        if not self.FSM['verify']:
            self._solve_command(se)
            return
        inclass = self.KDB.getinWaaClass(se)
        if inclass == 'other':
            self._solve_other(se)
        else:
            zzd.inWaaClass[inclass](self, se)
        
    def _solve_math(self, se):
        res = se.be('数学语句')
        print(se.s)
        if res[0] != True:
            self._solve_other(se)
        else:
            adapter = res[1]
            if '数学判断' in adapter or '数学方程' in adapter:
                self.add_desire('math',se.s)
            else:
                sen = zmath.c2math(se.ph)
                print(sen)
                if sen:
                    self.add_desire('math',sen)
                else:
                    self.say('数学语法错误')
    
    def _solve_command(self, se):
        res = se.be('命令语句')
        if res[0] != True:
            if not self.FSM['verify']:
                self.say('请先认证身份。')
                arg = self.ask(['认证参数','认证参数句'])
                if arg:
                    self.desire['verify'][1] = True
                    self.desire['verify'][2] = arg['认证参数']
            else:
                self.say('语法错误。')
            return
        adapter = res[1]
        assert 'zzd命令' in adapter
        if '命令参数' in adapter:
            arg = adapter['命令参数']
        else:
            arg = ''
        exe = self.KDB.keyword[adapter['zzd命令']][1]
        if exe:
            self.say('还在开发中')
            return
        if self.FSM['verify'] == False:
            if 'zzd认证命令' in adapter:
                self.desire['verify'][1] = True
                self.desire['verify'][2] = arg
            else:
                self.say('请先认证身份')
            return
        if 'zzd认证命令' in adapter:
            self.say('请已经认证过身份了.同时服务多人功能正在开发中')
        elif 'zzd播放命令' in adapter:
            out = self.player.play(arg)
        elif 'zzd换曲命令' in adapter:
            out = self.player.next()
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
            self._command_save()
        elif 'zzd学习命令' in adapter or 'zzd进入命令' in adapter:
            if self.FSM['train'] == False:
                self.say('好的，已进入学习模式！')
                self.FSM['train'] = True
            else:
                self.say('您已经是已学习模式了')
        elif 'zzd退出命令' in adapter:
            mode = adapter['zzd学习命令'] if 'zzd学习命令' in adapter else adapter['zzd模式定语_学习']
            if self.FSM['train'] == True:
                self.say('好的，已退出%s模式'%mode)
                self.FSM['train'] = False
            else:
                self.say('您并没有在%s模式'%mode)
        else:
            self.say('不识别的内置命令')

    def _command_save(self):
        infonum = self.KDB.getinfonum()
        if infonum == 0:
            self.say('没有信息需要写入数据库')
            return
        self.say('请输入管理员口令')
        password = self.ask(['认证参数句','认证参数'])
        if not password:
            self.say('您没有输入口令，写入取消。')
            return
        password = password['认证参数']
        if password != self.managerid:
            self.say('口令错误，写入取消。')
            return
            
        res = self.KDB.save_infomation(self.friend.name)
        if res[0] == False:
            self.say(res[1])
        else:
            self.say('成功写入%d条信息'%res[1])
            if res[1] < infonum:
                self.say('%d条信息写入失败'%res[2])
    
    def _solve_query(self, se):
        res = se.be('询问语句')
        if res[0] != True:
            self._solve_other(se)
        else:
            adapter = res[1]
            print(adapter)
            f = adapter['函数']
            x = adapter['.']
            if '一元函数询问语句' in adapter:
                res = self.KDB.getfn(f).value([self.KDB.getph(x)])
            else:
                assert '二元函数询问语句' in adapter
                assert '|' in x
                x = x.split('|')
                if '(的)' in adapter:
                    ph = [self.KDB.getph(x[0]), self.KDB.getph(x[1]), self.KDB.getph(x[2])]
                elif '反向词' in adapter:
                    ph = [self.KDB.getph(x[1]), self.KDB.getph(x[0]), None]
                else:
                    ph = [self.KDB.getph(x[0]), self.KDB.getph(x[1]), None]
                res = self.KDB.getfn(f).value(ph)
            self.say(str(res))

    def _solve_judge(self, se):
        res = se.be('判断语句')
        if res[0] != True:
            self._solve_other(se)
        else:
            adapter = res[1]
            if '集合判断语句' in adapter:
                assert '集合' in adapter
                if '.' in adapter:
                    x1 = adapter['.']
                    x2 = adapter['集合']
                else:
                    if '(包含)' in adapter:
                        x2,x1 = adapter['集合'].split('|')
                    else:
                        x1,x2 = adapter['集合'].split('|')
                        
                res = self.KDB.getse(x1).be(x2)
                print(adapter)
                print(res)
                if res[0] == True:
                    echo = adapter['集合断言语句']
                    self.say(echo)
                elif res[0] == False:
                    if res[1]:
                        echo = '不, %s'%res[1]
                    elif '系动词' in adapter:
                        echo = '%s不%s%s'%(x1,adapter['系动词'],x2)
                    elif '(属于)' in adapter:
                        echo = '%s不属于%s'%(x1,x2)
                    elif '(包含)' in adapter:
                        echo = '%s不包含%s'%(x2,x1)
                    else:
                        echo = '%s不%s'%(x1,x2)
                    self.say(echo)
                else:
                    self.say(res[1])
                    self.say('需要我上网问问吗？')
                    ok = self.ask(['选择回答语句'])
                    if ok and '肯定回答语句' in ok:
                        self.say('我还不会上网，逗你玩呢.哈哈哈')
                    elif ok and '否定回答语句' in ok:
                        self.say('好的')

    def _solve_affirm(self, se):
        res = se.be('断言语句')
        if res[0] != True:
            self._solve_other(se)
            return
        if self.FSM['train'] == False:
            self.say('对不起，您需先进入学习模式才能增加信息')
            self.say('是否进入学习模式?')
            ok = self.ask(['选择回答语句'])
            if ok and '肯定回答语句' in ok:
                self.say('好的，已进入学习模式')
                self.FSM['train'] = True
            return
        adapter = res[1]
        if '属于断言语句' in adapter:
            assert '.' in adapter
            assert '集合' in adapter
            x = self.KDB.getph(adapter['.'])
            gs = adapter['集合']
        elif '包含断言语句' in adapter:
            assert '集合' in adapter
            if '(包含)' in adapter:
                gs,x = adapter['集合'].split('|')
                x = self.KDB.getph(x)
            else:
                x,gs = adapter['集合'].split('|')
                x = self.KDB.getph(x)
        else:
            x = self.KDB.getph(adapter['.'])
            gs = adapter['集合']
        res = x.be(gs)
        if res[0] == True:
            self.say('我的知识库里已经有这条信息了')
        elif res[0] == False:
            self.say('这条信息与我的数据库冲突.因为:%s'%res[1])
        else:
            res = x.affirm(gs)
            if res[0] == True:
                self.say('好的，我记住了')
                self.KDB.add_study_info(x, gs)
            else:
                self.say(res[1])
        '''
        if '包含断言语句' in adapter:
                assert '...' in adapter
                assert '|' in adapter['...']
                x,fn=adapter['...'].split('|')
                if not self.KDB.spin(x):
                    self.say('%s是未知词。请先定义.')
                else:
                    sp = self.KDB.getsp(x)
                    res = sp.affirm(fn)
                    if res[0] == True:
                        self.say('好的，我记住了')
                        self.infomation_a_fn.append(res[1])
                    else:
                        self.say(res[1])
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
            assert self.KDB.gsin(gs)
            if self.FSM['train'] == False:
                self.say('对不起，您需进入学习模式才可以增加信息')
                return
            if '属于断言语句' in adapter:
                self._solve_set_a(x, gs)
            elif '包含断言语句' in adapter:
                self._solve_set_A(x, gs)
            else:
                if self.KDB.spin(x):
                    assert not self.KDB.getsp(x).be('集合')[0] == 0
                    self._solve_set_a(x, gs)
                else:    
                    self.say('我不知道%s是否是集合。是吗'%x)
                    ok = self.ask(['选择回答语句'])
                    if ok and '肯定回答语句' in ok:
                        self._solve_set_A(x, gs)
                    elif ok and '否定回答语句' in ok:
                        self._solve_set_a(x, gs)
                    else:
                        self.say('您没有给出肯定或否定，我将丢弃%s这条信息。'%sp[0])
'''

    def _solve_answer(self, se):
        assert 'ask' in self.FSM and not self.FSM['ask'][1]
        for question in self.FSM['ask'][0]:
            print('question:',question)
            res = se.be(question)
            if res[0] == True:
                self.FSM['ask'][1] = res[1]
                self.ask_event.set()
                return True
        self.ask_event.set()
        return False
    
    def _solve_other(self, se):
        if se.be('称呼')[0] == True:
            self.say('我在，有什么为你做的吗')
            return
        if se.be('询问语句')[0] == True:
            self._solve_query(se)
            return
        if se.be('判断语句')[0] == True:
            self._solve_query(se)
            return
        if se.be('断言语句')[0] == True:
            self._solve_affirm(se)
            return
        self._phrase_se(se)
    
    def _phrase_se(self, se):
        s = ''
        for ph in se.ph:
            s += '~%s'%ph.s
        self.say('对不起，我处理不了.分词结果是:%s'%s)
        n = ['']
        phrases = se.ph
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
            r ='我猜测:%s是新词，您可以进入学习模式进行学习'%rr
            self.say(r)
                
    def desire_verify(self, desire):
        if self.FSM['verify'] == True:
            desire[1] = False
            return
        desire[1] = False
        if not desire[2]:
            if 'verify_waiting' in self.FSM:
                self.say('您没有及时认证，我要休息了。')
                self.add_desire('goodbye', '再见')
            else:
                self.FSM['verify_waiting'] = True
                self.say('您好，我是小白，请认证身份！')
                self.add_desire('time', (desire, True, time.time()+60))
                arg = self.ask(['认证参数','认证参数句'])
                print('arg',arg)
                if arg:
                    self.desire['verify'][1] = True
                    self.desire['verify'][2] = arg['认证参数']
        else:
            if desire[2] in self.KDB.identify:
                self.friend.name = self.KDB.identify[desire[2]]
                self.FSM['verify'] = True
                self.say('%s您好，认证通过。%s很高兴为您服务。'%(self.friend.name, self.name))
                if self.desire['time'][1] == True:
                    if len(self.desire['time'][2]) == 1:
                        if self.desire['time'][2][0][0] == self.desire['verify']:
                            self.desire['time'][1] == False
                            self.desire['time'][2] = []
            else:
                self.say('认证失败。')
                arg = self.ask(['认证参数','认证参数句'])
                if arg:
                    self.desire['verify'][1] = True
                    self.desire['verify'][2] = arg['认证参数']
    
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
        infonum = self.KDB.getinfonum()
        if infonum > 0:
            self.say('您还有%d条学习信息没有写入数据库,需要写入吗？'%infonum)
            ok = self.ask(['选择回答语句'])
            if ok and '肯定回答语句' in ok:
                self._command_save()
            else:
                self.say('丢弃学习信息')
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
    
    if a == 'se':
        zhd.KDB.checkse(A)
    elif a == 'gs':
        zhd.KDB.checkgs(A, False)
    elif a == 'inw':
        res = zhd.KDB.getinWaaClass(zhd.KDB.getse(A))
        print(res)
    else:
        se = zhd.KDB.getse(a)
        res = se.be(A)
        print(res)
    
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
