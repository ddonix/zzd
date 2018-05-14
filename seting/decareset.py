#!/usr/bin/python3 -B
from seting import sets

#枚举集合，集合元素可以枚举，是有限个。如:(再见 拜拜),人等
#实现addsp函数.
class gsetdecare(sets.gset):
    def __init__(self, kdb, name):
        sets.gset.__init__(self, kdb, name)
        assert self.name[0] == '[' and self.name[-1] == ']'

        self.decare = []
        gram = name[1:-1].split(' ')
        for g in gram:
            assert not (g[0] == '[' and g[-1] == ']')
            assert g in kdb.mend_add or kdb.gsin(g)
            print('kdb',g,name)
            if g in kdb.mend_add:
                self.decare.append(g)
            else:
                self.decare.append(kdb.getgs(g))

    def spin(self, sp):
        return (False,'')
    
    def affirm1(self, sp):
        return (False, '不支持的操作')
    
    def affirm2(self, gs):
        return (False, '不支持的操作')
    
    def weight(self):
        r = 1
        return -1