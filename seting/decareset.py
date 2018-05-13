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
        return self.fensp(sp.d)
    
    def _fensp(self, phrases):
        if phrases and phrases[0] in self.sp:
            return (phrases[0].s, phrases[1:], {self.name:phrases[0].s})
        if self.child != []:
            ress = []
            for i in range(len(self.child)-1, -1, -1):
                res = self.child[i]._fensp(phrases)
                if res:
                    res[2][self.name] = res[0]
                    ress.append(res)
            if not ress:
                return None
            ress.sort(key=lambda x:len(x[1]))
            return ress[0]
        else:
            if self.name[0] == '(' and self.name[-1] == ')':
                return self.fensp_2(phrases)
            elif self.name[0] == '[' and self.name[-1] == ']':
                return self.fensp_3(phrases)
            else:
                return self.fensp_1(phrases)
    
    #只处理enum集合。没有子集，不依赖任何别的集合。
    def fensp_1(self, phrases):
        assert self.child == []
        assert self.name[0] != '(' and self.name[0] != ')'
        assert self.name[0] != '[' and self.name[0] != ']'
        if phrases:
            if phrases[0] in self.sp:
                return (phrases[0].s, phrases[1:], {self.name:phrases[0].s})
            elif phrases[0].s in gdata._mend_replace:
                for replace in gdata._mend_replace[phrases[0].s]:
                    if gdata.getsp(replace) in self.sp:
                        phrases[0] = gdata.getsp(replace)
                        return (phrases[0].s, phrases[1:], {self.name:phrases[0].s})
            return None
    
    #只处理[]集合。没有子集,但是要递归。例如[主语 谓语 句号] [上引号 ... 下引号] [认证命令 (身份)]
    def fensp_3(self, phrases):
        assert not self.child
        assert self.name[0] == '[' and self.name[-1] == ']'
        if phrases == []:
            return None
        ress = []
        key = {}
        for i, gs in enumerate(self.decare):
            if type(gs) == str:
            gdata.gsin(gram):
                g = gdata.getgs(gram)
                if g.child == []:
                    if gram[0] == '(' and gram[-1] == ')':
                        res = g.fensp_2(phrases)
                    else:
                        res = g.fensp_1(phrases)
                else:
                    res = g._fensp(phrases)
                if not res:
                    return None
                
                gset._addkey(key, gram, res[0])
                for k in res[2]:
                    gset._addkey(key, k, res[2][k])
                phrases = res[1]
                ress.append(res)
            elif gram == '.':
                if phrases == []:
                    return None
                gset._addkey(key, '.', phrases[0].s)
                ress.append((phrases[0].s, phrases[1:], {}))
                phrases = phrases[1:]
            elif gram == '...':
                tc = ''
                if i < len(frame)-1:
                    while phrases and (phrases[0].be('分隔词')[0] != 0) and (phrases[0].be(frame[i+1])[0] != 0):
                        tc += phrases[0].s
                        phrases = phrases[1:]
                else:
                    while phrases and (phrases[0].be('分隔词')[0] != 0):
                        tc += phrases[0].s
                        phrases = phrases[1:]
                gset._addkey(key, '...', tc)
                ress.append((tc, phrases, {}))
            else:
                print(gram)
                raise TypeError
        sps = ''
        for res in ress:
            sps += res[0]
        gset._addkey(key, self.name, sps)
        return (sps, ress[-1][1], key)
    
    def affirm1(self, sp):
        return (False, '不支持的操作')
    
    def affirm2(self, gs):
        return (False, '不支持的操作')
    
    def weight(self):
        r = 1
        return -1
