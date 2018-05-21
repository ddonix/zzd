#!/usr/bin/python3 -B
from function import func
from seting import categoryset

#求值函数,所有可以通过python eval的表达式都可以
class fnvalue(func.fn):
    def __init__(self, gfunc, dset, vset, f):
        func.fn.__init__(self, gfunc, dset, vset, f)

    #取值或者判断真假的函数
    def _value(self, ph):
        e = self.f
        if len(ph) == 1:
            e = e.replace('x','%s'%ph[0].s)
        else:
            for i in range(0,len(ph)):
                e = e.replace('x%d'%(i+1),'%s'%ph[i].s)
        gfn = self.gfunc.kdb.getfn(e[0:e.find('(')])
        m = e[e.find('('):][1:-1]
        print(gfn.name, m)
        if '(' not in m:
            m = m.split(',')
            ph = []
            for m in m:
                ph.append(self.gfunc.kdb.getph(m))
            return gfn.value(ph)
        else:
            res = self.vvv(m)
            print(res)
        return e

    def vvv(self, ss):
        return ss
 
def main():
    print('funccategory')
 
if __name__ == '__main__':
    main()
