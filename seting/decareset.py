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
            if g in kdb.mend_add:
                self.decare.append(g)
            else:
                self.decare.append(kdb.getgs(g))

    def phin(self, ph):
        for decare in self.decare:
            if type(decare) == str:
                continue
            else:
                if ph:
                    res = decare.judge1(ph)
                    ph = None
                    if res[0] != True:
                        return res
                else:
                    return (False, '')
        return res
    
    def _sein(self, phs):
        phh = phs
        sps = ''
        keys={}
       
        for i,de in enumerate(self.decare):
            if type(de) == str:
                sps += de
                continue
            if de.name == '...' and i < len(self.decare)-1 and type(self.decare[i+1]) != str:
                de.setplot(self.decare[i+1].name)
            res = de._judge3(phh)
            if not res or res[0] == False:
                break
            sps += res[0]
            phh = res[1]
            for k in res[2]:
                if k in keys:
                    keys[k] = '%s|%s'%(keys[k],res[2][k])
                else:
                    keys[k] = res[2][k]
        else:
            return (sps, phh, keys)
        return None
    
    def affirm1(self, sp):
        return (False, '不支持的操作')
    
    def affirm2(self, gs):
        return (False, '不支持的操作')
    
    def weight(self):
        return -1
