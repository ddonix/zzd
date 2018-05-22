#!/usr/bin/python3 -B
from function import func
from seting import categoryset

#求值函数,所有可以通过python eval的表达式都可以
class fnvalue(func.fn):
    def __init__(self, gfunc, dset, vset, f):
        func.fn.__init__(self, gfunc, dset, vset, f)

    #取值或者判断真假的函数
    def _v(self, e):
        li = self.e2list(e)
        print('self.f:',self.f)
        print('e:',e)
        print('li')
        if 'f' not in e:
            ee = self.f
            if len(li) == 2:
                ee=ee.replace('x',li[1])
            else:
                for i in range(1,len(li)):
                    ee=ee.replace('x%d'%i,li[i])
            name = self.f[0:self.f.find('(')]
            gfn = self.gfunc.kdb.getfn(name)
            print('...........')
            print(ee)
            print(gfn.name)
            return gfn.v(ee)
        else:
            return '递归了'
 
def main():
    print('funccategory')
 
if __name__ == '__main__':
    main()
