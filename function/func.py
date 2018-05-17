#!/usr/bin/python3 -B
import element

class gfunc:
    def __init__(self, kdb, name, desc):
        assert type(name) == str
        assert name
        assert 'f' in desc
        assert ':' in desc
        assert '->' in desc

        self.kdb = kdb
        assert not self.kdb.fnin(name)
        
        self.name = name
        
        self.func = set()
        desc = desc.split('~')
        for des in desc:
            d,f=des.split(',')
            dset = d[d.find(':')+1:d.find('-')]
            vset = d[d.find('>')+1:]
            fn = f[2:]
            self.func.add((dset,vset,fn))

    def getfn(self, ph):
        res = []
        for f in self.func:
            if ph.be(f[0])[0] == True:
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
    def _value(self, se, f):
        raise NotImplementedError
    
    def _judge(self, se, f, desp):
        raise NotImplementedError
    
def main():
    print('func')
    
if __name__ == '__main__':
    main()
