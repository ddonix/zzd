#!/usr/bin/python3 -B
import element

class gfunc:
    def __init__(self, kdb, name, desc, byname):
        assert type(name) == str
        assert name
        assert 'f' in desc
        assert ':' in desc
        assert '->' in desc

        self.kdb = kdb
        assert not self.kdb.getfn(name)
        
        self.name = name
        self.byname = set()     #别名
        
        self.func = set()
        desc = desc.split('~')
        for des in desc:
            d,f=des.split(',')
            dset = d[d.find(':')+1:d.find('-')]
            vset = d[d.find('>')+1:]
            fn = f[2:]
            self.func.add((dset,vset,fn))
        if byname:
            byname = byname.split('~')
            for name in byname:
                self.addbyname(name)
    
    def addbyname(self, name):
        assert name != self.name
        self.byname.add(name)

    def getfn(self, ph):
        res = []
        for f in self.func:
            d = f[0]
            if d[0] == '[':
                dset = d[1:-1].split(' ')
            else:
                dset = [d]
            if len(ph) in [len(dset), len(dset)+1]:
                for i in range(0,len(dset)):
                    if ph[i].be(dset[i])[0] == True:
                        res.append(f)
        return res
    
    def vs(self, ph):
        for f in self.func:
            if ph.be(f[1])[0] == True:
                return f[1]
        return None
    
    #取值或者判断真假的函数
    def value(self, ph):
        fn = self.getfn(ph)
        if not fn:
            return (False, '没有%s'%self.name)
        for f in fn:
            res = self._value(ph, f)
            if res != None:
                if type(res) == bool:
                    return (True, '对' if res else '错')
                else:
                    return (True, str(res))
        return (False, '%s未知'%self.name)
    
    def judge(self, ph, desp):
        fn = self.getfn(ph)
        if not fn:
            return (False, '')
        for f in fn:
            res = self._judge(ph, f, desp)
            if res != None:
                return (True, str(res))
        return (False, '')
    
    #取值或者判断真假的函数
    def _value(self, ph, f):
        raise NotImplementedError
    
    def _judge(self, ph, f, desp):
        raise NotImplementedError
    
def main():
    print('func')
    
if __name__ == '__main__':
    main()
