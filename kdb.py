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
        
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.execute("select * from mend_add")
        except:
            raise TypeError
        for mend in cursor:
            self.mend_add.add(mend[0])
        
        try:
            cursor = conn.execute("select * from mend_replace")
        except:
            raise TypeError
        for mend in cursor:
            self.mend_replace[mend[0]] = mend
        conn.close()
        
        self.fninit()
        self.gsinit()
        self.phinit()
        self.coreinit()
        
    def getinWaaClass(self, sep):
        keyword = [x for x in sep.d if x.s in self.keyword]
        if sep.s in self.keyword:
            keyword.append(sep)
        bit = {'math':0, 'query':0, 'judge':0, 'command':0, 'affirm':0}
        for k in keyword:
            weight = self.keyword[k.s][0].split(' ')
            for i in range(0,len(weight),2):
                bit[weight[i]] += int(weight[i+1])
        bit = sorted(bit.items(),key = lambda x:x[1],reverse = True)
        if bit[0][1] == 0:
            return 'other'
        else:
            return bit[0][0]
    
    def getgs(self, g):
        try:
            return self.gset[g]
        except:
            raise NameError

    def getfn(self, f):
        try:
            return self.func[f]
        except:
            raise NameError

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

    def gsin(self, g):
        return True if g in self.gset else False

    def fnin(self, f):
        return True if f in self.func else False
        
    def legal(self, s):
        for v in s:
            if not v in self.vocable:
                print('%s中有非法字符%s'%(s,v))
                return False
        return True

    def addgs(self, gs):
        self.gset[gs.name] = gs

    def addfn(self, fn):
        self.func[fn.name] = fn

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
        assert self.gsin(gram)
        #检查gs的sp与子集的sp是否有重合
        gs = self.getgs(gram)
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
    def add_database_a_in_A(self, sp_a, gs_A):
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.cursor()
            if len(sp_a) > 1:
                sql = '''select * from table_phrase where name=(?)'''
            else:
                sql = '''select * from table_vocable where name=(?)'''
            cursor.execute(sql, (sp_a,))
            conn.commit()
            info = cursor.fetchall()
            print(info)
            if not info:
                if len(sp_a) > 1:
                    sql = '''insert into table_phrase (name, gs) values (?, ?)'''
                else:
                    sql = '''insert into table_vocable (name, gs) values (?, ?)'''
                # 把数据保存到name username和 id_num中
                cursor.execute(sql, (sp_a,gs_A))
            else:
                gs = '%s~%s'%(info[0][1],gs_A) if info[0][1] else gs_A
                if len(sp_a) > 1:
                    sql = '''update table_phrase set gs=(?) where name=(?)'''
                else:
                    sql = '''update table_vocable set gs=(?) where name=(?)'''
                cursor.execute(sql, (gs, sp_a))
            conn.commit()
            conn.close
        except:
            print('写入数据库失败')
            return False
        print('写入数据库成功')
        return True

    #A是B的子集
    def add_database_A_in_B(self, gs_A, gs_B):
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.cursor()
            sql = '''select * from gset_phrase where name=(?)'''
            cursor.execute(sql, (gs_B,))
            conn.commit()
            info = cursor.fetchall()
            print(info)
            if not info:
                sql = '''insert into gset_phrase (name, subset) values (?, ?)'''
                # 把数据保存到name username和 id_num中
                cursor.execute(sql, (gs_B,gs_A))
            else:
                gs = '%s~%s'%(info[0][1],gs_A) if info[0][1] else gs_A
                sql = '''update gset_phrase set subset=(?) where name=(?)'''
                cursor.execute(sql, (gs, gs_B))
            conn.commit()
            conn.close
        except:
            print('写入数据库失败')
            return False
        print('写入数据库成功')
        return True


    #增加元素a属于集合A这条信息。
    #成功返回True，错误返回False，其他返回2.
    def add_information_1(self, a, A):
        assert self.gsin(A)
        ph = self.getph(a)
        gs = self.getgs(A)
        res = gs.affirm1(ph)
        if res[0] == True:
            ph._addgs(gs)
        return res

    #增加集合B属于集合A这条信息。
    #成功返回True，失败返回False，其他返回2.
    def add_information_2(self, B, A):
        assert self.gsin(A)
        gs = self.getgs(A)
        if self.gsin(B):
            gsB = self.getgs(B)
        else:
            if B[0] == '[' and B[-1] == ']':
                gse = B[1:-1].split(' ')
                for g in gse:
                    assert not (g[0] == '[' and g[-1] == ']')
                    if g in self.mend_add or self.gsin(g):
                        continue
                    self.addgs(enumset.gsetenum(self, g))
                gsB = decareset.gsetdecare(self, B)
            else:
                gsB = enumset.gsetenum(self, B)
            self.addgs(gsB)
        return gs.affirm2(gsB)

    def gsinit(self):
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
            if not self.gsin(v[0]):
                self.addgs(enumset.gsetenum(self, v[0]))
            if v[1]:
                gram = prevgram(v[1])
                for g in gram:
                    self.add_information_2(g, v[0])
        
    def fninit(self):
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.execute("select * from func")
            grammar = cursor.fetchall()
            conn.close()
        except:
            return NameError
        for f in grammar:
            if not f[0]:
                continue
            fn = function.func(self, f[0], f[1])
        for f in self.func:
            print(f,self.getfn(f))

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
                    self.add_information_1(v[0], g)
            if v[2]:
                ph.addfn(v[2])
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
                    self.add_information_1(v[0], g)
            if v[2]:
                ph.addfn(v[2])
        conn.close()
        
        #补充所有集合类元素集,例如：集合语句是集合
        #补充()类集合里面的元素
        for gram in self.gset:
            if gram[0] != '[' and gram[0] != '(':
                if not self.getph(gram):
                    self.addph(element.phrases(gram))
                self.add_information_1(gram, '集合')
            if gram[0] == '(' and gram[-1] == ')':
                item = gram[1:-1].split(' ')
                for sp in item:
                    self.add_information_1(sp, gram)
        
    def coreinit(self):
        try:
            conn = sqlite3.connect('./data/grammar.db')
            cursor = conn.execute("select * from zzd_keyword")
        except:
            raise NameError
        for keyword in cursor:
            if keyword[0] in self.gset:
                self.gset_key[keyword[0]] = keyword[1:]
                for sp in self.phrases:
                    for s in self.phrases[sp]:
                        if self.phrases[sp][s].be(keyword[0])[0] == 0:
                            self.keyword[s] = keyword[1:]
            elif keyword[0][0] == '(' and keyword[0][-1] == ')':
                gs = sets.gset(keyword[0])
                self.gset_key[keyword[0]] = keyword[1:]
                item = keyword[0][1:-1].split(' ')
                for sp in item:
                    add_information_1(sp, keyword[0])
                    self.keyword[sp] = keyword[1:]
            else:
                raise NameError
        
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
    kdb.checkse('一切')
        
if __name__ == '__main__':
    main()
