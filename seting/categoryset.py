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
        self.judge1_recursion = False
        self.judge2_recursion = False
        self.judge3_recursion = False
        self.e = set()

    def setfn(self, fn, f, v):
        self.fn = fn
        self.f = f
        self.v = v
        return

    def phin(self, ph):
        res = self.fn.value([ph])
        if res[0] == False:
            return (2, res[1])
        elif res[1] == self.v:
            return (True, {self.name:ph.s})
        else:
            return (False, '%s是%s%s'%(ph.s, res[1], self.f[0]))
            
    def affirm1(self, ph):
        if self.judge1(ph)[0] == True:
            return (True, '')
        elif self.judge1(ph)[0] == False:
            return (False, '')
        else:
            self.e.add(ph.s)
            print(self.fn.name, self.v)
            ph.addfn(self.fn.name, self.v)
            return (True, '')
    
    def weight(self):
        return -1

def main():
    print('gsetcategory')
    
if __name__ == '__main__':
    main()
