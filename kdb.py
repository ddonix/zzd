#!/usr/bin/python3 -B
import sqlite3
import copy
import function
import element
from seting import sets
from seting import stickset
from seting import enumset
from seting import decareset
from seting import reguset
from seting import categoryset
from function import func
from function import valuefunc
from function import basefunc
import sys

class ZZDKDB():
    def __init__(self):
        self.func = {}          #所有函数
        self.gset = {}          #所有集合
        self.vocable = {' '}    #所有字符
        self.phrases = {}        #所有语句
        self.identify = {}      #身份认证
        self.gset_key = {}      #关键集合
        self.keyword = {}       #关键语句
        self.mend_add = set()   #增加修复集合
        self.mend_replace = {}  #替换修复集合
    
        self.infomation_a = {} # 'a':'G' a属于G
        self.infomation_A = {} # 'X':'G' A包含G
        
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.execute("select * from mend")
        except:
            raise TypeError
        for mend in cursor:
            if not mend[1]:
                self.mend_add.add(mend[0])
            else:
                self.mend_replace[mend[0]] = mend
        conn.close()
        self.gsinit()
        self.fninit()
        self.phinit()
        self.coreinit()
        
    def getinWaaClass(self, se):
        keyword = [x.s for x in se.ph if x.s in self.keyword]
        if se.s in self.keyword:
            keyword.append(se.s)
        bit = {'math':0, 'query':0, 'command':0, 'affirm':0, 'talk':0}
        for k in keyword:
            weight = self.keyword[k][0].split(' ')
            for i in range(0,len(weight),2):
                bit[weight[i]] += int(weight[i+1])
        bit = sorted(bit.items(),key = lambda x:x[1],reverse = True)
        if bit[0][1] == 0:
            return 'other'
        else:
            return bit[0][0]
    
    def getgs(self, g):
        return self.gset[g] if g in self.gset else None

    def getfn(self, f):
        return self.func[f] if f in self.func else None
        
    def getph(self, s):
        if s[0] in self.phrases:
            if s in self.phrases[s[0]]:
                return self.phrases[s[0]][s]
        znumber =  '0123456789'
        cnumber =  '零一二三四五六七八九十百千万亿'
        zstr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if s[0] in znumber:
            f = znumber
        elif s[0] in cnumber:
            f = cnumber
        elif s[0] in zstr:
            f = zstr+znumber
        else:
            return None
        for e in s[1:]:
            if e not in f:
                return None
        ph = element.phrases(s)
        if f == znumber:
            ph._addgs(self.getgs('数'))
        elif f == cnumber:
            ph._addgs(self.getgs('汉语数'))
        else:
            ph._addgs(self.getgs('字符串'))
        return ph

    def getse(self, s):
        se = element.sentence(self,s)
        return se

    def legal(self, s):
        for v in s:
            if not v in self.vocable:
                print('%s中有非法字符%s'%(s,v))
                return False
        return True

    def addgs(self, gs):
        self.gset[gs.name] = gs
        for name in gs.byname:
            self.gset[name] = gs

    def addfn(self, fn):
        self.func[fn.name] = fn
        for name in fn.byname:
            self.func[name] = fn


    def addph(self, ph):
        if len(ph.s) == 1:
            self.phrases[ph.s[0]] = {ph.s:ph}
        else:
            self.phrases[ph.s[0]][ph.s] = ph
    
    def checkph(self, ph):
        print('检查PH %s'%ph)
        ph = self.getph(ph)
        if not ph:
            print('%s是未知的词')
            return
        print('1.实例信息')
        print(ph)
        if len(ph.gs) == 0:
            print('2.不属于任何集合')
        else:
            print('2.属合下列集合:')
            for gs in ph.gs:
                print(gs.name)
    
    def checkse(self, se):
        print('检查SE %s'%se)
        se = self.getse(se)
        print('1.实例信息')
        print(se)
        print('2.分词')
        for p in se.ph:
            pr = '%s|'%p.s
            for g in p.gs:
                pr += '%s '%g.name
            print(pr)
        
    def checkgs(self, gram, recursion):
        #检查gs的sp与子集的sp是否有重合
        gs = self.getgs(gram)
        assert gs
        print('检查集合 %s：'%gs.name)
        print('1.实例信息')
        print(gs)
            
        print('2.子集')
        if gs.child == []:
            print('没有子集')
        else:
            print('包含以下子集')
            for ch in gs.child:
                print(ch.name)
        
        print('3.父集')
        if gs.father == []:
            print('没有父集')
        else:
            print('包含于以下父集')
            for fa in gs.father:
                print(fa.name)

        print('4.元素')
        w = gs.weight()
        if w == 0:
            print('没有元素')
        elif w == -1:
            print('包含可数无穷元素')
        else:
            print('包含%d个元素,分别是：'%w)
            for e in gs.e:
                print(e)
        
        #递归检查gs的子集
        if recursion:
            for ch in gs.child:
                checkgs(ch.name, True)
        print('check success')
    
    #a是A的元素
    def add_local_database_a_in_G(self, user, a, G):
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.cursor()
            sql = '''select * from user_phrase where (user, s)=(?, ?)'''
            cursor.execute(sql, (user, a))
            conn.commit()
        except:
            print('读取数据库失败')
            return False
        
        info = cursor.fetchall()
        print(info)
        try:
            if not info:
                sql = '''insert into user_phrase (user, s, gs) values (?, ?, ?)'''
                cursor.execute(sql, (user, a, G))
            else:
                gs = '%s~%s'%(info[0][2],G) if info[0][2] else G
                sql = '''update user_phrase set gs=(?) where (user, s)=(?, ?)'''
                cursor.execute(sql, (gs, user, a))
        except:
            print('写入数据库失败')
            return False
            
        conn.commit()
        conn.close
        return True

    #A是G的子集
    def add_local_database_A_in_G(self, user, A, G):
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.cursor()
            sql = '''select * from user_gset_phrase where (user, name)=(?, ?)'''
            cursor.execute(sql, (user, G))
            conn.commit()
        except:
            print('读取数据库失败')
            return False
        
        info = cursor.fetchall()
        print(info)
        try:
            if not info:
                sql = '''insert into user_gset_phrase (user, name, subset) values (?, ?, ?)'''
                cursor.execute(sql, (user, G, A))
            else:
                subset = '%s~%s'%(info[0][2],A) if info[0][2] else A
                sql = '''update user_gset_phrase set subset=(?) where (user, name)=(?, ?)'''
                cursor.execute(sql, (subset, user, G))
        except:
            print('写入数据库失败')
            return False
            
        conn.commit()
        conn.close
        return True
    
    def getinfonum(self):
        return len(self.infomation_a)+len(self.infomation_A)
        
    def save_infomation(self, user):
        fail = 0
        success = 0
        allinfo = self.getinfonum()
        if allinfo == 0:
            return (False, '没有信息需要写入数据库')
        while self.infomation_a:
            info = self.infomation_a.popitem()
            if not self.add_local_database_a_in_G(user, info[0], info[1]):
                fail += 1
                self.infomation_a[info[0]]=info[1]
                break
            else:
                success += 1
        
        while self.infomation_A:
            info = self.infomation_A.popitem()
            if not self.add_local_database_A_in_G(user, info[1], info[0]):
                fail += 1
                self.infomation_A[info[0]]=info[1]
                break
            else:
                success += 1
        return (True, success, fail)
    
    def add_study_info(self, x, gs):
        if x.be('集合')[0] == True:
            x = x.s
            if gs in self.infomation_A:
                self.infomation_A[gs] += '~%s'%x
            else:
                self.infomation_A[gs] = x
        else:
            x = x.s
            if x in self.infomation_a:
                self.infomation_a[x] += '~%s'%gs
            else:
                self.infomation_a[x] = gs
    
    #增加元素a属于集合G这条信息。
    #成功返回True，错误返回False，其他返回2.
    def add_information_a_in_G(self, a, G):
        gs = self.getgs(G)
        if not gs:
            gs = enumset.gsetenum(self, G)
            self.addgs(gs)
        ph = self.getph(a)
        res = gs.affirm1(ph)
        if res[0] == True:
            ph._addgs(gs)
        return res

    #增加集合A包含于集合G这条信息。
    #成功返回True，失败返回False，其他返回2.
    def add_information_A_in_G(self, A, G):
        gs = self.getgs(G)
        assert gs
        gsA = self.getgs(A)
        if not gsA:
            if A[0] == '[' and A[-1] == ']':
                gse = A[1:-1].split(' ')
                for g in gse:
                    assert not (g[0] == '[' and g[-1] == ']')
                    if g in self.mend_add or self.getgs(g):
                        continue
                    self.addgs(enumset.gsetenum(self, g))
                gsA = decareset.gsetdecare(self, A)
            else:
                gsA = enumset.gsetenum(self, A)
            self.addgs(gsA)
        res = gs.affirm2(gsA)
        if res[0] == True and gs not in gsA.father:
            gsA.father.append(gs)
        return res

    def gsinit(self):
        self.addgs(enumset.gsetenum(self, '集合'))
        self.addgs(enumset.gsetenum(self, '函数'))
        self.addgs(stickset.gsetstick(self, '数'))
        self.addgs(stickset.gsetstick(self, '汉语数'))
        self.addgs(stickset.gsetstick(self, '字符串'))
        self.addgs(reguset.gsetregu(self, '.'))
        self.addgs(reguset.gsetregu(self, '...'))
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.execute("select * from gset_phrase")
            grammar = cursor.fetchall()
            cursor = conn.execute("select * from gset_sentence")
            grammar.extend(cursor.fetchall())
            conn.close()
        except:
            return NameError
        for v in grammar:
            if not v[0]:
                continue
            if not self.getgs(v[0]):
                self.addgs(enumset.gsetenum(self, v[0]))
            if v[1]:
                gram = prevgram(v[1])
                for g in gram:
                    self.add_information_A_in_G(g, v[0])
 
    def fninit(self):
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.execute("select * from func")
            grammar = cursor.fetchall()
            conn.close()
        except:
            return NameError
        
        basefn = {'如果否则':('[. . .]', '.')}
        basefn['与'] = ('[bool bool]', 'bool')
        basefn['或'] = ('[bool bool]', 'bool')
        basefn['非'] = ('bool', 'bool')
        basefn['大于'] = ('[数 数]', 'bool', '大')
        basefn['大于等于'] = ('[数 数]', 'bool')
        basefn['小于'] = ('[数 数]', 'bool', '小')
        basefn['小于等于'] = ('[数 数]', 'bool')
        basefn['不等于'] = ('[. .]', 'bool')
        basefn['等于'] = ('[. .]', 'bool')
        basefn['加'] = ('[数 数]', '数', '加上~和')
        basefn['减'] = ('[数 数]', '数', '减去~差')
        basefn['乘'] = ('[数 数]', '数', '乘以~乘积~积')
        basefn['除'] = ('[数 数 w(商or余数)]', '数')
        basefn['除以'] = ('[数 数 w(商or余数)]', '数')

        for name in basefn:
            if len(basefn[name]) == 3:
                gfn = function.func.gfunc(self, name, basefn[name][2])
            else:
                gfn = function.func.gfunc(self, name)
            self.addfn(gfn)
            fn = function.basefunc.fnbase(gfn, basefn[name][0], basefn[name][1])
            gfn.setfn(fn)
        
        for gfunc in grammar:
            self.add_function(gfunc[0],gfunc[1], gfunc[2], gfunc[3], gfunc[4], gfunc[5], False)

    def add_function(self, name, byname, dset, vset, define, condition, ph):
        gfn = function.func.gfunc(self, name, byname)
        self.addfn(gfn)
        fn = function.valuefunc.fnvalue(gfn, dset, vset, define, condition)
        gfn.setfn(fn)
        if ph:
            if not self.getph(name):
                self.addph(element.phrases(name))
            self.add_information_a_in_G(name, '函数')
            for name in gfn.byname:
                if not self.getph(fn):
                    self.addph(element.phrases(fn))
                self.add_information_a_in_G(fn, '函数')
            fn.createph()
        
    def phinit(self):
        element.phrases.init(self)
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.execute("select * from table_vocable")
        except:
            raise NameError
        for v in cursor:
            assert len(v[0]) == 1
            self.vocable.add(v[0][0])
            ph = element.phrases(v[0])
            self.addph(ph)
            
            for g in v[1].split('~') if v[1] else []:
                if not (g == '' or g == None):
                    self.add_information_a_in_G(v[0], g)
        try:
            cursor = conn.execute("select * from table_phrase")
        except:
            raise NameError
        for v in cursor:
            assert len(v[0]) > 1
            ph = element.phrases(v[0])
            self.addph(ph)
            
            for g in v[1].split('~') if v[1] else []:
                if not (g == '' or g == None):
                    self.add_information_a_in_G(v[0], g)
            if v[2]:
                ph.addfn(v[2])
        conn.close()
        
        #补充所有集合类元素集,例如：集合语句是集合
        #补充()类集合里面的元素
        for gram in self.gset:
            if gram[0] != '[' and gram[0] != '(':
                if not self.getph(gram):
                    self.addph(element.phrases(gram))
                self.add_information_a_in_G(gram, '集合')
                for name in self.gset[gram].byname:
                    if not self.getph(name):
                        self.addph(element.phrases(name))
                    self.add_information_a_in_G(name, '集合')
                    
            if gram[0] == '(' and gram[-1] == ')':
                item = gram[1:-1].split(' ')
                for sp in item:
                    self.add_information_a_in_G(sp, gram)
        
        #补充函数的phrases
        for fn in self.func:
            if fn[0] != '(':
                if not self.getph(fn):
                    self.addph(element.phrases(fn))
                self.add_information_a_in_G(fn, '函数')
                for name in self.func[fn].byname:
                    if not self.getph(fn):
                        self.addph(element.phrases(fn))
                    self.add_information_a_in_G(fn, '函数')
        
    def coreinit(self):
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.execute("select * from zzd_keyword")
        except:
            raise NameError
        for keyword in cursor:
            assert keyword[0] in self.gset
            self.gset_key[keyword[0]] = keyword[1:]
            for sp in self.phrases:
                for s in self.phrases[sp]:
                    if self.phrases[sp][s].be(keyword[0])[0] == True:
                        self.keyword[s] = keyword[1:]
        
        try:
            cursor = conn.execute("select * from verify")
        except:
            raise TypeError
        for guest in cursor:
            self.identify[guest[0]] = guest[1]
        conn.close()

    
#对子集进行排序，子集项多的在后
#原始子集在前的在前
def prevgram(gram):
    tmp = []
    for g in gram.split('~'):
        tmp.extend(_prevgram(g))
    tmp2 = []
    for t in tmp:
        if t in tmp2:
            continue
        for i in range(0,len(tmp2),1):
            if len(t) < len(tmp2[i]):
                tmp2.insert(i, t)
                break
            if len(t) == len(tmp2[i]):
                tmp2.insert(i+1, t)
                break
        else:
            tmp2.append(t)
    res = []
    for t in tmp2:
        if type(t) == str:
            r = t
        elif len(t) == 1:
            r = t[0]
        else:
            r = '[%s'%t[0]
            for s in t[1:]:
                r += ' %s'%s
            r += ']'
        res.append(r)
    return res
    
def _prevgram(gram):
    if gram == '' or gram == None:
        return []
    if not (gram[0] == '[' and gram[-1] == ']'):
        return [gram]
    gram = gram[1:-1].split(' ')
    res = []
    __prevgram(gram, res)
    return res

def __prevgram(gram, res):
    if not gram:
        return
    if len(gram) == 1:            #[w宾语] [谓语]
        if gram[0][0] == 'w':
            res.append([])
            res.append([gram[0][1:]])
        else:
            res.append([gram[0]])
        return
    __prevgram(gram[1:], res)    #[[w宾语], [谓语]]
    if gram[0][0] == 'w':        
        res2 = []
        for g in res:
            ag = copy.deepcopy(g)
            ag.insert(0,gram[0][1:])
            res2.append(ag)
        res.extend(res2)
        return
    else:
        for g in res:
            g.insert(0,gram[0])
    return


def main():
    print('kdb')
    kdb = ZZDKDB()
    for func in kdb.func:
        print(func)
        
if __name__ == '__main__':
    main()
