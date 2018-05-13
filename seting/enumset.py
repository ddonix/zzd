#!/usr/bin/python3 -B
from seting import sets

#枚举集合，集合元素可以枚举，是有限个。如:(再见 拜拜),人等
#实现addsp函数.
class gsetenum(sets.gset):
    def __init__(self, kdb, name):
        sets.gset.__init__(self, kdb, name)
        self.e = set()         #元素集合，这个集合里的元素不属于任何子集.
        self.FSM = {}
        if self.name[0] == '(' and self.name[-1] == ')':
            es = self.name[1:-1].split(' ')
            for s in es:
                self.e.add(s)
                    
    def spin(self, sp):
        if sp.s in self.e:
            return (True, {self.name:sp.s})
        elif 'over' in self.FSM:
            return (False, '')
        else:
            return (2, '')
    
    def affirm1(self, sp):
        if self.judge1(sp)[0] == True:
            return (True, '')
        self.e.add(sp.s)
        return (True, '')
    
    def affirm2(self, gs):
        self.child.append(gs)
        return (True, '')
    
    def weight(self):
        return len(self.e)
