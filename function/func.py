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

    def getfn(self, se):
        for f in self.func:
            if se.be(f[0])[0] == True:
                return f
        return None
    
    def vs(self, se):
        for f in self.func:
            if se.be(f[1])[0] == True:
                return f[1]
        return None
    
    #取值或者判断真假的函数
    def value(self, se):
        raise NotImplementedError
    
    def judge(self, se, desp):
        raise NotImplementedError
    
def main():
    print('func')
    
if __name__ == '__main__':
    main()
