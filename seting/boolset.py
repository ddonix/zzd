#!/usr/bin/python3 -B
from seting import sets

#分类集合，枚举集合的划分。例如:人划分为男人和女人
class gsetbool(sets.gset):
    def __init__(self, kdb, name):
        sets.gset.__init__(self, kdb, name)
        self.judge1_recursion = False
        self.judge2_recursion = False
        self.judge3_recursion = False
        self.e = set()

    def setfn(self, fn, f):
        self.fn = fn
        self.f = f
        return

    def phin(self, ph):
        res = self.fn.value([ph])
        if res == False or res == 'False':
            return (False, '%s不是%s'%(ph.s, self.name))
        elif res == True or res == 'True':
            return (True, {self.name:ph.s})
        else:
            return (False, res)
 
    def weight(self):
        return -1

def main():
    print('gsetcategory')
    
if __name__ == '__main__':
    main()
