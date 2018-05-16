#!/usr/bin/python3 -B

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
            print(dset)
            print(vset)
    
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
    def value_a(self, se):
        raise NotImplementedError
    
    def affirm_a(self, sp, desp):
        raise NotImplementedError
    
    def judge_a(self, sp, desp):
        raise NotImplementedError
    
    def value_A(self, gs):
        raise NotImplementedError

def main():
    print('func')
    
if __name__ == '__main__':
    main()
