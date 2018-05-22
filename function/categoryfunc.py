#!/usr/bin/python3 -B
from function import func
from seting import categoryset
from seting import boolset
#分类集合，枚举集合的划分。例如:人划分为男人和女人
class fncategory(func.fn):
    def __init__(self, gfunc, dset, vset, f):
        func.fn.__init__(self, gfunc, dset, vset, f)
        self.creategset()
    
    #取值或者判断真假的函数
    def _v(self, e):
        res = func.gfunc.e2list(e)
        ph = self.gfunc.kdb.getph(res[1])
        if not self.f:
            if self.gfunc.name in ph.fn:
                return ph.fn[self.gfunc.name]
            else:
                return '%s未知'%self.gfunc.name
        else:
            return '递归'
    
    def creategset(self):
        if self.vset == 'bool':
            if self.dset[0] != '[':
                gs = boolset.gsetbool(self.gfunc.kdb, self.gfunc.name)
                gs.setfn(self.gfunc, self)
                for byname in self.gfunc.byname:
                    gs.addbyname(byname)
                self.gfunc.kdb.addgs(gs)
                self.gfunc.kdb.add_information_A_in_G(gs.name, self.dset)
        else:
            for v in self.vset[1:-1].split(' '):
                gs = categoryset.gsetcategory(self.gfunc.kdb, '%s%s'%(v,self.dset))
                gs.setfn(self.gfunc, self, v)
                
                gs.addbyname('%s的%s'%(v,self.dset))
                if self.gfunc.name[0] != '(':
                    gs.addbyname('%s%s的%s'%(self.gfunc.name, v,self.dset))
                    gs.addbyname('%s是%s的%s'%(self.gfunc.name, v,self.dset))
                self.gfunc.kdb.addgs(gs)
                self.gfunc.kdb.add_information_A_in_G(gs.name, self.dset)
 
def main():
    print('funccategory')
    
if __name__ == '__main__':
    main()
