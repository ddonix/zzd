#!/usr/bin/python3 -B
from function import func
from seting import categoryset
#分类集合，枚举集合的划分。例如:人划分为男人和女人
class gfunccategory(func.gfunc):
    def __init__(self, kdb, name, desc):
        func.gfunc.__init__(self, kdb, name, desc)
        self.creategset()

    #取值或者判断真假的函数
    def _value(self, ph, fn):
        if len(ph) != 1:
            return None
        ph = ph[0]
        if not fn[2]:
            if self.name in ph.fn:
                return ph.fn[self.name]
            else:
                return None
        else:
            if fn[0] == '数':
                e = fn[2].replace('如果','if')
                e = e.replace('否则','else')
                e = e.replace('x','(%s)'%ph.s)
                return eval(e)
            else:
                return None
    
    def _judge(self, ph, fn, desp):
        return None

    def creategset(self):
        for f in self.func:
            for v in f[1][1:-1].split(' '):
                gs = categoryset.gsetcategory(self.kdb, '%s%s'%(v,f[0]))
                gs.setfn(self, f, v)
                
                gs.addbyname('%s的%s'%(v,f[0]))
                if self.name[0] != '(':
                    gs.addbyname('%s%s的%s'%(self.name, v,f[0]))
                    gs.addbyname('%s是%s的%s'%(self.name, v,f[0]))
                self.kdb.addgs(gs)
                self.kdb.add_information_2(gs.name, f[0])
                

def parsefunc(kdb, fn):
    assert fn[1] == '分类'
    func = gfunccategory(kdb, fn[0], fn[2])
    return func

def main():
    print('funccategory')
    
if __name__ == '__main__':
    main()
