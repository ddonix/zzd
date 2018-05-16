#!/usr/bin/python3 -B
from seting import sets

#分类集合，枚举集合的划分。例如:人划分为男人和女人
class gsetcategory(sets.gset):
    def __init__(self, kdb, name):
        assert '.' not in name
        assert '[' not in name
        assert ']' not in name
        assert '(' not in name
        assert ')' not in name
        sets.gset.__init__(self, kdb, name)

    def setfn(self, fn):
        return

    def phin(self, ph):
        if ph.s in self.e:
            return (True, {self.name:ph.s})
        elif 'over' in self.FSM:
            return (False, '')
        else:
            return (2, '对不起，我不知道')
    
    def affirm1(self, ph):
        if self.judge1(ph)[0] == True:
            return (True, '')
        self.e.add(ph.s)
        return (True, '')
    
    def affirm2(self, gs):
        self.child.append(gs)
        gs.father.append(self)
        return (True, '')
    
    def weight(self):
        return len(self.e)

def parsefunc(kdb, func):
    for s in func:
        print(s)


class func:
    def __init__(self, kdb, name, desc):
        assert type(name) == str
        assert name
        assert 'f' in desc
        assert ':' in desc
        assert '->' in desc

        self.kdb = kdb
        assert not self.kdb.fnin(name)
        
        self.name = name
        self.kdb.addfn(self)
        
        self.func = set()
        desc = desc.split('~')
        for des in desc:
            d,f=des.split(',')
            dset = d[d.find(':')+1:d.find('-')]
            vset = d[d.find('>')+1:]
            fn = f[2:]
            self.func.add((dset,vset,fn))
            print(vset)
            if vset[0] == '(' and vset[-1] == ')':
                self.plot = {}
                for v in vset[1:-1].split(' '):
                    self.plot[v] = set()
                    self.plot[v].add('%s'%v)
                    self.plot[v].add('%s性'%v)
                    self.plot[v].add('%s类'%v)
                    self.plot[v].add('%s%s'%(v,dset))
                    self.plot[v].add('%s的%s'%(v,dset))
                    self.plot[v].add('%s%s的%s'%(self.name, v,dset))
                    self.plot[v].add('%s是%s的%s'%(self.name, v,dset))
                    self.plot[v].add('%s为%s的%s'%(self.name, v,dset))
                print(self.plot)
                
    def ds(self, sp):
        for f in self.func:
            if sp.be(f[0])[0] == 0:
                return True
        return False
    
    def vs(self, sp):
        for f in self.func:
            if sp.be(f[0])[0] == 0:
                return f[1]
        return None
    
    #取值或者判断真假的函数
    def value_a(self, sp):
        for f in self.func:
            if sp.be(f[0])[0] != 0:
                continue
            if f[1] == '数' or f[1] == 'bool':
                if f[2].find('eval(x)') != -1:
                    e = f[2].replace('eval(x)','(%s)'%sp.s)
                else:
                    e = f[2]
                return eval(e)
        return None
    
    def affirm_a(self, sp, desp):
        print('sp.s, desp', sp.s, desp)
        for f in self.func:
            if sp.be(f[0])[0] != 0:
                continue
            if f[1][0] != '(' or f[1][-1] != ')':
                continue
            print('f:',f[0],f[1],f[2])
            if not f[2]:    #没有推理
                for p in self.plot:
                    if desp in self.plot[p]:
                        if self.name in sp.fn:
                            if sp.fn[self.name] == p:
                                return (0,[],{self.name:p})
                            else:
                                return (1,[],{self.name:sp.fn[self.name]})
                        else:
                            return [2,'%s的%s未知'%(sp.s,self.name)]
                return [2,'%s是未知的词'%desp]
            else:            #有推理
                return [2,'现在还不会推理']
        return [2,'%s是未知的词'%desp]
    
    def judge_a(self, sp, desp):
        print('sp.s, desp', sp.s, desp)
        print('sp.s, desp', sp.s, desp)
        for f in self.func:
            if sp.be(f[0])[0] != 0:
                continue
            if f[1][0] != '(' or f[1][-1] != ')':
                continue
            print('f:',f[0],f[1],f[2])
            if not f[2]:    #没有推理
                for p in self.plot:
                    if desp in self.plot[p]:
                        if self.name in sp.fn:
                            if sp.fn[self.name] == p:
                                return (0,[],{self.name:p})
                            else:
                                return (1,[],{self.name:sp.fn[self.name]})
                        else:
                            return [2,'%s的%s未知'%(sp.s,self.name)]
                return [2,'%s是未知的词'%desp]
            else:            #有推理
                return [2,'现在还不会推理']
        return [2,'%s是未知的词'%desp]
    
    def value_A(self, gs):
        return None

def main():
    print('gsetcategory')
    
if __name__ == '__main__':
    main()
