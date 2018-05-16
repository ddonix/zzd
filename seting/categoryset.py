#!/usr/bin/python3 -B
from seting import sets

#分类集合，枚举集合的划分。例如:人划分为男人和女人
class gsetcategory(sets.gset):
    def __init__(self, kdb, name):
        assert '.' not in name
        assert '[' not in name
        assert ']' not in name
        assert '(' not in name
        assert ')' not in name
        sets.gset.__init__(self, kdb, name)

    def setfn(self, fn, v):
        self.fn = fn
        self.v = v
        return

    def phin(self, ph):
        res = self.fn.value(ph)
        if not res:
            return (2, '对不起，我不知道')
        if res == self.v:
            return (True, {self.name:ph.s})
        else:
            return (False, '%s是%s的'%(ph.s, res))
            
    def affirm1(self, ph):
        if self.judge1(ph)[0] == True:
            return (True, '')
        self.e.add(ph.s)
        return (True, '')
    
    def affirm2(self, gs):
        self.child.append(gs)
        gs.father.append(self)
        return (True, '')
    
    def weight(self):
        return -1

def main():
    print('gsetcategory')
    
if __name__ == '__main__':
    main()
