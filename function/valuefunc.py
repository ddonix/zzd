#!/usr/bin/python3 -B
from function import func
from seting import categoryset
from seting import boolset

#求值函数,所有可以通过python eval的表达式都可以
class fnvalue(func.fn):
    def __init__(self, gfunc, dset, vset, f, c):
        func.fn.__init__(self, gfunc, dset, vset, f, c)
        if dset[0] != '[' and (vset == 'bool' or vset[0] == '('):
            self.creategset()

    #取值或者判断真假的函数
    def _v(self, e):
        li = func.gfunc.e2list(e)
        ee = self.f
        if not ee:
            ph = self.gfunc.kdb.getph(li[1])
            return ph.fn[self.gfunc.name] if self.gfunc.name in ph.fn else '%s未知'%self.gfunc.name
        if len(li) == 2:
            ee=ee.replace('x',li[1])
        else:
            for i in range(1,len(li)):
                ee=ee.replace('x%d'%i,li[i])
        if 'f(' not in self.f:
            name = self.f[0:self.f.find('(')]
            gfn = self.gfunc.kdb.getfn(name)
            return gfn.v(ee)
        else:
            if not self.c:
                return '没有递归结束条件,请检查知识库'
            for c in self.c:
                if li[1] == c[0]:
                    return c[1]
            name = self.gfunc.name
            gfn = self.gfunc.kdb.getfn(name)
            return gfn.v(ee)
    
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
    print('funcvalue')
 
if __name__ == '__main__':
    main()
