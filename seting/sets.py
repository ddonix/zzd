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
        
    def affirm1(self, ph):           #ph属于self
        raise NotImplementedError
    
    def affirm2(self, gs):           #gs包含于self
        raise NotImplementedError
    
    def affirm3(self, se):           #se包含于self
        raise NotImplementedError
    
    def phin(self, ph):             #判断ph是否属于self，不考虑子集
        raise NotImplementedError
    
    def _sein(self, phs):           #判断se是否属于self，不考虑子集
        raise NotImplementedError

    def judge1(self, ph):           #判断ph是否属于self
        keys = {}
        for child in self.child:
            res = child.judge1(ph)
            if res[0] == True:
                for k in res[1]:
                    keys[k] = res[1][k]
        res = self.phin(ph)
        if res[0] == True:
            for k in res[1]:
                keys[k] = res[1][k]
        else:
            if keys:
                keys[self.name] = ph.s

        if keys:
            return (True, keys)
        else:
            return res
    
    def judge2(self, gs):     #判断gs是否是self的子集
        if gs == self:
            return (True, self)
        res = [2]
        for child in self.child:
            res = child.judge2(gs)
            if res[0] != 2:
                return res
        return res
    
    def _judge3(self, phs):
        if not phs:
            return None
        if self.child:
            ress = []
            for i in range(len(self.child)-1, -1, -1):
                phss = []
                phss.extend(phs)
                res = self.child[i]._judge3(phss)
                if res:
                    res[2][self.name] = res[0]
                    ress.append(res)
            if ress:
                ress.sort(key=lambda x:len(x[1]))
                return ress[0]
        return self._sein(phs)

    def judge3(self, se):     #判断se是否属于self
        if len(se.ph) == 1:
            return self.judge1(se.ph[0])
        res = self._judge3(se.ph)
        if res and not res[1]:
            return (True, res[2])
        else:
            return (False, '')

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
