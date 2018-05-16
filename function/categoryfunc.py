#!/usr/bin/python3 -B
from function import func
from seting import categoryset

#分类集合，枚举集合的划分。例如:人划分为男人和女人
class gfunccategory(func.gfunc):
    def __init__(self, kdb, name, desc):
        func.gfunc.__init__(self, kdb, name, desc)
        self.creategset()

    #取值或者判断真假的函数
    def value(self, se):
        fn = self.getfn(se)
        if not fn:
            return None
        if not fn[2]:
            if self.name in se.fn:
                return se.fn[self.name]
            else:
                return None
        else:
            return None
    
    def judge(self, se, desp):
        return None

    def creategset(self):
        for f in self.func:
            for v in f[1][1:-1].split(' '):
                gs = categoryset.gsetcategory(self.kdb, '%s%s'%(v,f[0]))
                gs.setfn(self, v)
                
                gs.addbyname('%s的%s'%(v,f[0]))
                if self.name[0] != '(':
                    gs.addbyname('%s%s的%s'%(self.name, v,f[0]))
                    gs.addbyname('%s是%s的%s'%(self.name, v,f[0]))
                self.kdb.addgs(gs)
                

def parsefunc(kdb, fn):
    assert fn[1] == '分类'
    func = gfunccategory(kdb, fn[0], fn[2])
    kdb.addfn(func)


def main():
    print('funccategory')
    
if __name__ == '__main__':
    main()
