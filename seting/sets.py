#!/usr/bin/python3 -B
import sqlite3
import copy

class gset:
    def __init__(self, kdb, name):
        assert type(name) == str
        assert name
        self.kdb = kdb
        
        self.name = name        #名字
        self.byname = set()     #别名
        
        self.father = []        #父集
        self.child = []         #子集

    def weight(self):               #返回集合的元素个数，无穷集合返回-1.
        raise NotImplementedError
        
    def affirm1(self, sp):           #sp属于self
        raise NotImplementedError
    
    def affirm2(self, gs):           #gs包含于self
        raise NotImplementedError
    
    def spin(self, sp):             #判断sp是否属于self，但是不属于self的任何child
        raise NotImplementedError

    def _do_fensp(self, phrases):
        raise NotImplementedError
    
    def _fensp(self, phrases):
        if phrases and self.judge1(phrases[0])[0] == True:
            return (phrases[0].s, phrases[1:], {self.name:phrases[0].s})
        if self.child != []:
            ress = []
            for i in range(len(self.child)-1, -1, -1):
                res = self.child[i]._fensp(phrases)
                if res:
                    res[2][self.name] = res[0]
                    ress.append(res)
            if not ress:
                return None
            ress.sort(key=lambda x:len(x[1]))
            return ress[0]
        else:
            return self._do_fensp(phrases)
    
    def fensp(self, phrases):
        res = self._fensp(phrases)
        return res if res and not res[1] else None
    
    def judge1(self, sp):            #判断sp是否属于self
        res = self.spin(sp)
        if res[0] != 2:
            return res
        for child in self.child:
            res = child.judge1(sp)
            if res[0] == True:
                res[1][self.name] = sp.s
                return res
        return res
    
    def judge2(self, gs):     #判断gs是否是self的子集吗?
        if gs == self:
            return (True, self)
        res = [2]
        for child in self.child:
            res = child.judge2(gs)
            if res[0] != 2:
                return res
        return res

    def addbyname(self, name):
        for n in name:
            assert n != self.name
            assert n not in self.byname
            self.byname.add(n)

    def __str__(self):
        res = '名字:%s\n'%self.name
        if self.byname:
            res += '别名:'
            for name in self.byname:
                res += '%s '%name
            res += '\n'
        w = self.weight()
        if w == 0:
            res +='没有元素\n'
        elif w > 0:
            res +='元素个数：%s\n'%str(w)
            for s in self.e:
                res +='%s '%s
            res += '\n'
        else:
            res +='元素个数：无穷\n'
        return res
    
def main():
    print('sets')

if __name__ == '__main__':
    main()
